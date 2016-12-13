from flask import Flask, jsonify, abort, make_response
import binascii as bi
import provider_02_pb2
import requests
import json

PORT = 5002

app = Flask(__name__)

class Provider:
    def __init__(self, address):
        self.address = address
        self.end_points = []

    def make_request(self, args):
        if args[0] in self.end_points.keys():
            if len(args) == 1:
                response = requests.get(self.address + self.end_points[args[0]])
            else:
                response = requests.get(self.address + self.end_points[args[0]] +  "/" + str(args[1]))
            if args[0] == "get_item":
                items = self.convert_item(response)
            else:
                items = self.convert_items(response)
            return items
        else:
            return {'error': {'message': "Method not supported", 'provider': self.provider}}

class Provider_01(Provider):
    def __init__(self, address):
        Provider.__init__(self, address)
        self.provider = self.__class__.__name__
        self.end_points = {"get_item": "item",
                           "get_items": "items",
                           "get_sex": "sex",
                           "price_more": "price/more",
                           "price_less": "price/less"}

    def convert_items(self, response):
        data = json.loads(response.content.decode('utf-8'))
        if 'error' in data.keys():
            return {'error': {'message': data['error'], 'provider': self.provider}}
        converted = {}
        converted['items'] = []
        for item in data['data']['items']:
            converted['items'].append({'provider': self.provider, 'id': item})
        return converted

    def convert_item(self, response):
        data = json.loads(response.content.decode('utf-8'))
        if 'error' in data.keys():
            return {'error': {'message': data['error'], 'provider': self.provider}}
        data = data['data']['item']
        converted = {}
        converted['item'] = {}
        converted['item']['provider'] = self.provider
        converted['item']['description'] = data['id']
        converted['item']['description'] = data['description']
        converted['item']['price'] = data['price']
        converted['item']['name'] = data['name']
        converted['item']['sex'] = []
        converted['item']['category'] = []
        for sex in data['sex']:
            if isinstance(sex, int):
                converted['item']['sex'].append(sex)
            else:
                converted['item']['category'] += (sex['category'])
        converted['item']['provider_specific'] = {}
        converted['item']['provider_specific']['price_history'] = data['previous_prices']
        return converted

class Provider_02(Provider):
    def __init__(self, address):
        Provider.__init__(self, address)
        self.provider = self.__class__.__name__
        self.end_points = {"get_item": "get_item",
                           "get_items": "get_items",
                           "get_sex": "get_sex",
                           "get_material": "get_material",
                           "price_more": "price/more",
                           "price_less": "price/less"}

    def convert_items(self, response):
        data = provider_02_pb2.Response()
        data.ParseFromString(bi.unhexlify(response.content))
        if data.HasField('error'):
            return {'error': {'message':  str(data.error.code), 'provider': self.provider}}
        converted = {}
        converted['items'] = []
        for item in data.items.id:
            converted['items'].append({'provider': self.provider, 'id': item})
        return converted

    def convert_item(self, response):
        data = provider_02_pb2.Response()
        data.ParseFromString(bi.unhexlify(response.content))
        if data.HasField('error'):
            return {'error': {'message':  str(data.error.code), 'provider': self.provider}}
        converted = {}
        converted['item'] = {}
        converted['item']['provider'] = self.provider
        converted['item']['id'] = data.item.id
        converted['item']['description'] = data.item.description
        converted['item']['price'] = data.item.price
        converted['item']['name'] = data.item.name
        converted['item']['sex'] = []
        converted['item']['category'] = []
        for sex in data.item.sex:
            converted['item']['sex'].append(sex)
        for category in data.item.category:
            converted['item']['category'].append(category)
        #TODO: kolor
        converted['item']['provider_specific'] = {}
        converted['item']['provider_specific']['photos'] = []
        for photo in data.item.photos:
            converted['item']['provider_specific']['photos'].append(photo)
        converted['item']['provider_specific']['material'] = data.item.material
        return converted

provider_1 = Provider_01("http://localhost:5000/api/v1.0/")
provider_2 = Provider_02("http://localhost:5001/api/v1.0/")

providers = [provider_1, provider_2]

def ask_providers(*args):
    data = {}
    data['errors'] = []
    data['items'] = []
    for provider in providers:
        response = provider.make_request(args)
        if 'error' in response.keys():
            data['errors'].append(response['error'])
        if 'items' in response.keys():
            data['items'] += response['items']
    return jsonify({'errors': data['errors'], 'data': {'items': data['items']}})

@app.route('/')
def index():
    return "Asia Kozak"

@app.route('/api/v1.0/get_item/<string:provider_name>/<string:id>', methods=['GET'])
def get_item(provider_name, id):
    data = {}
    data['errors'] = []
    data['item'] = []
    for provider in providers:
        if provider.__class__.__name__ == provider_name:
            response = provider.make_request(["get_item", id])
    if 'error' in response.keys():
        data['errors'].append(response['error'])
    if 'item' in response.keys():
        data['item'].append(response['item'])
    return jsonify({'errors': data['errors'], 'data': {'item': data['item']}})

@app.route('/api/v1.0/get_items', methods=['GET'])
def get_items():
    return ask_providers("get_items")

@app.route('/api/v1.0/get_sex/<int:id>', methods=['GET'])
def get_sex(id):
    return ask_providers("get_sex", id)

@app.route('/api/v1.0/get_material/<string:material>', methods=['GET'])
def get_material(material):
    return ask_providers("get_material", material)

@app.route('/api/v1.0/price/more/<int:amount>', methods=['GET'])
def price_more(amount):
    return ask_providers("price_more", amount)

@app.route('/api/v1.0/price/less/<int:amount>', methods=['GET'])
def price_less(amount):
    return ask_providers("price_less", amount)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(port=PORT, debug=True)
