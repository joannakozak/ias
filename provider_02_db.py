import sqlite3
from enum import IntEnum
import uuid

filename = 'provider_02.db'

class Sex(IntEnum):
    male = 1
    female = 2
    kids = 3

class Category(IntEnum):
    shoes = 1
    pants = 2
    hats = 3

items = [
    {
        'id': str(uuid.uuid1()),
        'name': u"Pants no 1234",
        'price': 88.90,
        'sex': [Sex.male],
        'category': [Category.pants],
        'description': u'Ugly pants',
        'photos': ["adres1.com", "adres2.org"],
        'materials': ["cotton"]
    },
    {
        'id': str(uuid.uuid1()),
        'name': u"Pants no 1235",
        'price': 98.90,
        'sex': [Sex.male],
        'category': [Category.pants],
        'description': u'Ugly pants',
        'photos': ["adres4.com", "adres2.org"],
        'materials': ["wool"]
    },
    {
        'id': str(uuid.uuid1()),
        'name': u"Pants no 1236",
        'price': 188.90,
        'sex': [Sex.female],
        'category': [Category.shoes],
        'description': u'Ugly pants',
        'photos': ["adres6.com", "adres2.org"],
        'materials': ["wool", "cotton"]
    },
]

conn = sqlite3.connect(filename)

c = conn.cursor()

c.execute("CREATE TABLE items \
          (uuid char(50), \
           price real, \
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

c.execute("CREATE TABLE photos \
        (id int, \
         url char(250) \
        ) \
        ")

c.execute("CREATE TABLE materials \
       (id int, \
        material char(50) \
       ) \
       ")

for item in items:
    c.execute("INSERT INTO items (uuid, price, name, description) VALUES (?, ?, ?, ?)", (item['id'], item['price'], item['name'], item['description']))
    for sex in item['sex']:
        c.execute("INSERT INTO sex (id, sex) VALUES (?, ?)", (item['id'], sex))
    for category in item['category']:
        c.execute("INSERT INTO category (id, category) VALUES (?, ?)", (item['id'], category))
    for photo in item['photos']:
        c.execute("INSERT INTO photos (id, url) VALUES (?, ?)", (item['id'], photo))
    for material in item['materials']:
        c.execute("INSERT INTO materials (id, material) VALUES (?, ?)", (item['id'], material))

conn.commit()
conn.close()
