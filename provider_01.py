from flask import Flask, jsonify, abort, make_response
import sqlite3

PORT = 5000

app = Flask(__name__)

filename = 'provider_01.db'

@app.route('/')
def index():
    return "Asia Kozak"

@app.route('/api/v1.0/items', methods=['GET'])
def get_items():
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    items = []
    for item in c.execute("SELECT rowid, * FROM items"):
        items.append(item[0])
    conn.close()
    if len(items) == 0:
        abort(404)
    return jsonify({'data': {'items': items}})

@app.route('/api/v1.0/item/<int:id>', methods=['GET'])
def get_item(id):
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    item = {}
    for i in c.execute("SELECT rowid, * FROM items WHERE rowid = ?", (id,)):
        item['id'] = i[0]
        item['price'] = i[1]
        item['name'] = i[2]
        item['description'] = i[3]
        item['previous_prices'] = []
        item['sex'] = []
        item['sex'].append({'category': []})
        for category in c.execute("SELECT rowid, * FROM category WHERE id = ?", (item['id'],)):
            item['sex'][0]['category'].append((category[2]))
        for sex in c.execute("SELECT rowid, * FROM sex WHERE id = ?", (item['id'],)):
            item['sex'].append(sex[2])
        for price in c.execute("SELECT rowid, * FROM prices WHERE id = ?", (item['id'],)):
            item['previous_prices'].append({price[3]: price[2]})
    conn.close()
    if len(item) == 0:
        abort(404)
    return jsonify({'data': {'item': item}})

@app.route('/api/v1.0/sex/<int:id>', methods=['GET'])
def get_sex(id):
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    items = []
    for item in c.execute("SELECT rowid, * FROM sex WHERE sex = ?", (id,)):
        items.append(item[1])
    conn.close()
    if len(items) == 0:
        abort(404)
    return jsonify({'data': {'items': items}})

@app.route('/api/v1.0/price/more/<int:amount>', methods=['GET'])
def price_more(amount):
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    items = []
    for item in c.execute("SELECT rowid, * FROM items WHERE price >= ?", (amount,)):
        items.append(item[0])
    conn.close()
    if len(items) == 0:
        abort(404)
    return jsonify({'data': {'items': items}})

@app.route('/api/v1.0/price/less/<int:amount>', methods=['GET'])
def price_less(amount):
    #reuse price_more
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    items = []
    for item in c.execute("SELECT rowid, * FROM items WHERE price < ?", (amount,)):
        items.append(item[0])
    conn.close()
    if len(items) == 0:
        abort(404)
    return jsonify({'data': {'items': items}})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(port=PORT, debug=True)
