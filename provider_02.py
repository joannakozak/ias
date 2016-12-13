from flask import Flask, jsonify, abort, make_response
import sqlite3
import binascii as bi
import provider_02_pb2

PORT = 5001

app = Flask(__name__)

filename = 'provider_02.db'

@app.route('/')
def index():
    return "Asia Kozak"

@app.route('/api/v1.0/get_items', methods=['GET'])
def get_items():
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    response = provider_02_pb2.Response()
    for item in c.execute("SELECT * FROM items"):
        new = response.items.id.append(item[0])
    conn.close()
    if len(response.items.id) == 0:
        abort(404)
    print(bi.hexlify(response.SerializeToString()))
    return bi.hexlify(response.SerializeToString())

@app.route('/api/v1.0/get_item/<string:id>', methods=['GET'])
def get_item(id):
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    response = provider_02_pb2.Response()
    for i in c.execute("SELECT * FROM items WHERE uuid = ?", (id,)):
        response.item.id = id
        response.item.price = i[1]
        response.item.name = i[2]
        response.item.description = i[3]
        for category in c.execute("SELECT * FROM category WHERE id = ?", (response.item.id,)):
            response.item.category.append((category[1]))
        for photo in c.execute("SELECT * FROM photos WHERE id = ?", (response.item.id,)):
            response.item.photos.append(photo[1])
        for material in c.execute("SELECT * FROM materials WHERE id = ?", (response.item.id,)):
            response.item.material = material[1]
        for sex in c.execute("SELECT * FROM sex WHERE id = ?", (response.item.id,)):
            response.item.sex.append(sex[1])
    conn.close()
    if response.item.id == "":
        abort(404)
    return bi.hexlify(response.SerializeToString())

@app.route('/api/v1.0/get_sex/<int:id>', methods=['GET'])
def get_sex(id):
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    response = provider_02_pb2.Response()
    for item in c.execute("SELECT  * FROM sex WHERE sex = ?", (id,)):
        new = response.items.id.append(item[0])
    conn.close()
    if len(response.items.id) == 0:
        abort(404)
    return bi.hexlify(response.SerializeToString())

@app.route('/api/v1.0/get_material/<string:id>', methods=['GET'])
def get_material(id):
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    response = provider_02_pb2.Response()
    for item in c.execute("SELECT  * FROM materials WHERE material = ?", (id,)):
        new = response.items.id.append(item[0])
    conn.close()
    if len(response.items.id) == 0:
        abort(404)
    return bi.hexlify(response.SerializeToString())

@app.route('/api/v1.0/price/more/<int:amount>', methods=['GET'])
def price_more(amount):
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    response = provider_02_pb2.Response()
    for item in c.execute("SELECT * FROM items WHERE price >= ?", (amount,)):
        new = response.items.id.append(item[0])
    conn.close()
    if len(response.items.id) == 0:
        abort(404)
    return bi.hexlify(response.SerializeToString())

@app.route('/api/v1.0/price/less/<int:amount>', methods=['GET'])
def price_less(amount):
    #reuse price_more
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    response = provider_02_pb2.Response()
    for item in c.execute("SELECT * FROM items WHERE price < ?", (amount,)):
        new = response.items.id.append(item[0])
    conn.close()
    if len(response.items.id) == 0:
        abort(404)
    return bi.hexlify(response.SerializeToString())

@app.errorhandler(404)
def not_found(error):
    response = provider_02_pb2.Response()
    response.error.message = "Not found"
    response.error.code = 404
    return make_response(bi.hexlify(response.SerializeToString()), 404)

if __name__ == '__main__':
    app.run(port=PORT, debug=True)
