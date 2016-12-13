import sqlite3
from enum import IntEnum

filename = 'provider_01.db'

class Sex(IntEnum):
    male = 1
    female = 2
    kids = 3

class Category(IntEnum):
    shoes = 1
    pants = 2
    hats = 3

class Collection(IntEnum):
    winter = 1
    spring = 2
    summer = 3
    autumn = 4

items = [
    {
        'name': u"Pants no 1234",
        'sex': [Sex.male,
            {'category': [Category.pants]}
            ],
        'collection': [Collection.spring],
        'price': 288.90,
        'previous_prices': [{1480944384: 399}, {1480844384: 499}],
        'description': u'Ugly pants',
    },
    {
        'name': u"Hat no 234",
        'sex': [Sex.male, Sex.female,
            {'category': [Category.hats]}
            ],
        'collection': [Collection.winter],
        'price': 88.90,
        'previous_prices': [{1480944884: 309}, {1480844584: 299}],
        'description': u'Nice hat',
    },
    {
        'name': u"Hat no 235",
        'sex': [Sex.female,
            {'category': [Category.hats]}
            ],
        'collection': [Collection.winter],
        'price': 948.90,
        'previous_prices': [{1480944884: 309}, {1480844584: 299}],
        'description': u'Nice hat 3',
    }
]

conn = sqlite3.connect(filename)

c = conn.cursor()

c.execute("CREATE TABLE items \
          (price real, \
           name char(50), \
           description char(250) \
          ) \
          ")

c.execute("CREATE TABLE sex \
          (id int, \
          sex int \
          ) \
          ")

c.execute("CREATE TABLE category \
         (id int, \
          category int \
          ) \
          ")

c.execute("CREATE TABLE collection \
          (id int, \
           collection int \
           ) \
          ")

c.execute("CREATE TABLE prices \
          (id int, \
           price real, \
           timestamp int \
           ) \
          ")

for item in items:
    c.execute("INSERT INTO items (price, name, description) VALUES (?, ?, ?)", (item['price'], item['name'], item['description']))
    last_row = c.lastrowid
    for sex in item['sex']:
        if isinstance(sex, Sex):
            c.execute("INSERT INTO sex (id, sex) VALUES (?, ?)", (last_row, sex))
        else:
            for category in sex['category']:
                c.execute("INSERT INTO category (id, category) VALUES (?, ?)", (last_row, category))
    for collection in item['collection']:
        c.execute("INSERT INTO collection (id, collection) VALUES (?, ?)", (last_row, collection))
    for price in item['previous_prices']:
        for key in price:
            c.execute("INSERT INTO prices (id, price, timestamp) VALUES (?, ?, ?)", (last_row, price[key], key))

conn.commit()
conn.close()
