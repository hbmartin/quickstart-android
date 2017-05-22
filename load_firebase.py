#!/usr/bin/env python3

"""Roll up the geo6 json to produce a tree suitable for sub9 query"""

__author__ = "H. Martin"
__version__ = "0.1.0"

import math
from random import randint
import pyrebase

email = ""
password = ""
data = {}

with open('data.json', encoding='utf-8') as data_file:
    data = json.loads(data_file.read())

for geohash6 in data:
    geohash_info = {}
    count = math.ceil(data[geohash6] * 0.5)
    geohash_info['count'] = count
    geohash_info['ids'] = {}
    for i = 1 to count:
        new_id = str(randint(0, 922337203685477580))
        geohash_info[new_id] = True

firebase_config = {}
with open('sub9-client/app/google-services.json ', encoding='utf-8') as data_file:
    firebase_config = json.loads(data_file.read())
pyrebase_config = {
    "apiKey": firebase_config["client"][0]["api_key"][0]["current_key"],
    "authDomain": firebase_config["project_info"]["storage_bucket"],
    "databaseURL": firebase_config["project_info"]["firebase_url"],
    "storageBucket": firebase_config["project_info"]["storage_bucket"]
}
firebase = pyrebase.initialize_app(pyrebase_config)
auth = firebase.auth()
auth.create_user_with_email_and_password(email, password)
db = firebase.database()

geo4 = db.child(geohash6[4:])
count4 = geo4.child("count")
if not count4.get():
    count4.put(0)
geo5 = geo4.child(geohash6[5:])
count5 = geo5.child("count")
if not count5.get():
    count5.put(0)
geo5.child(geohash6).put(geohash_info)
count5.increment(count)
count4.increment(count)