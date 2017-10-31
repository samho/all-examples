from pymongo import MongoClient
import datetime


#client = MongoClient('localhost', 27017)

src_client = MongoClient("mongodb://localhost:27017/gizwits_data")

src_db = src_client['gizwits_data']

src_collection = src_db['device_status']

src_set = set()

target_client = MongoClient("mongodb://localhost:27018/gizwits_data")

target_db = target_client["gizwits_data"]

target_collection = target_db['device_status']

target_set = set()

#for item in src_collection.find():
#    print item['_id']


#for item in target_collection.find():
#    print item.cursor_id

#print("Test %s") % collection.find({"username": "Sam"})[0]

#collection.update({"username":"Sam"},{"$set":{"country":"China"}})


def get_dbs(client):
    dbs_list = []
    for db in client.database_names():
        dbs_list.append(db)

    return dbs_list


def get_collections(db):
    col_list = []
    for col in db.collection_names(include_system_collections=False):
        col_list.append(db['%s' % col])

    return col_list


def get_items(col):
    tmp_set = set()
    for item in col.find():
       tmp_set.add(item['_id'])

    return tmp_set


def diff_item_set(src_col, target_col):
    pass


def diff_col(src_db, target_db):
    pass


def generate_diff_item(diff_item_liste):
    pass


if __name__ == '__main__':
    for db in get_dbs(src_client):
        if db == 'local':
            continue
        col_list = get_collections(src_client['%s' % db])
        for col in col_list:
            src_set = get_items(col)
            for i in src_set:
                print i