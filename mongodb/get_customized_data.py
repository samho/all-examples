from pymongo import MongoClient
import datetime

client = MongoClient('localhost', 27017)

db = client['gizwits_data']

collection = db['device_status']


#print("Test %s") % collection.find({"username":"Sam"})[0]

#collection.update({"username":"Sam"},{"$set":{"country":"China"}})


items = collection.find({"$and": [{"product_key": "eda2ed8e1597428fa3fb5f62a23ccd3d"}, {"is_online": {"$exists": True}}]})

print "ID, IP, Mac, Did, City, Created At, Updated At, Online First, Online Latest, Online Count"

count = 1

for item in items:
    print "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (str(count),
                                                      str(item['ip']),
                                                      str(item['mac']),
                                                      str(item['did']),
                                                      str(item['city']),
                                                      datetime.datetime.fromtimestamp(int(item['created_at'])).strftime(
                                                          '%Y-%m-%d %H:%M:%S'),
                                                      datetime.datetime.fromtimestamp(int(item['updated_at'])).strftime(
                                                          '%Y-%m-%d %H:%M:%S'),
                                                      str(item['online_1st']),
                                                      str(item['online_latest']),
                                                      str(item['online_cnt'])
                                                      )
    count += 1





# print items[0]['ip']
# print collection.find({"product_key": "eda2ed8e1597428fa3fb5f62a23ccd3d"})[0]['mac']
# print collection.find({"product_key": "eda2ed8e1597428fa3fb5f62a23ccd3d"})[0]['updated_at']
# print collection.find({"product_key": "eda2ed8e1597428fa3fb5f62a23ccd3d"})[0]['city']
# print collection.find({"product_key": "eda2ed8e1597428fa3fb5f62a23ccd3d"})[0]['online_1st']
# print collection.find({"product_key": "eda2ed8e1597428fa3fb5f62a23ccd3d"})[0]['dev2app_at']
# print collection.find({"product_key": "eda2ed8e1597428fa3fb5f62a23ccd3d"})[0]['created_at']
# print collection.find({"product_key": "eda2ed8e1597428fa3fb5f62a23ccd3d"})[0]['online_latest']
# print collection.find({"product_key": "eda2ed8e1597428fa3fb5f62a23ccd3d"})[0]['did']
# print collection.find({"product_key": "eda2ed8e1597428fa3fb5f62a23ccd3d"})[0]['online_cnt']
