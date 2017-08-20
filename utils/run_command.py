import subprocess
from pymongo import MongoClient

domain_list = [""]
output = "domain_users.csv"


def run(command):
    p = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)


def read_file(file_path):
    client = MongoClient('localhost', 27017)
    db = client['gizwits_data']
    f = file(file_path, "r")
    for line in f:
        # command = '/data/mongodb/bin/mongoexport --port 27018 -d gizwits_core -c domain.%(domain_id)s.user --type=csv -f "created_at,updated_at,uid,is_anonymous,password,phone,email,phone_id,mac" >> test.csv' % {"domain_id": line.strip()}
        collection = db['domain.%(domain_id)s.user' % {"domain_id":line}]
        items = collection.find()
        for item in items:


if __name__ == '__main__':
    read_file("domain.csv")
