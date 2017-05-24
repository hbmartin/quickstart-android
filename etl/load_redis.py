#!/usr/bin/env python3

"""Roll up the geo6 json to produce a tree suitable for sub9 query"""

__author__ = "H. Martin"
__version__ = "0.1.0"

import json
import math
from random import randint
import redis


data = {}
r = redis.StrictRedis(host='localhost', port=6379, db=0)

with open('full_map.json', encoding='utf-8') as data_file:
    data = json.loads(data_file.read())

for geo4, geo4_data in data.items():
    r.set(geo4 + '.count', geo4_data['count'])
    del geo4_data['count']
    for geo5, geo5_data in geo4_data.items():
        r.set(geo5 + '.count', geo5_data['count'])
        del geo5_data['count']
        for geo6, geo6_data in geo5_data.items():
            r.set(geo6 + '.count', geo6_data['count'])
