from pymongo import MongoClient
import datetime


#client = MongoClient('localhost', 27017)

client = MongoClient("mongodb://localhost:27017/gizwits_data")

db = client['gizwits_data']

collection = db['device_status']

for item in collection.find():
    print item

#print("Test %s") % collection.find({"username": "Sam"})[0]

#collection.update({"username":"Sam"},{"$set":{"country":"China"}})


def get_collections(db):
    pass


def get_items(col):
    pass


def diff_item_set(src_col, target_col):
    pass


def diff_col(src_db, target_db):
    pass


def generate_diff_item(diff_item_liste):
    pass



