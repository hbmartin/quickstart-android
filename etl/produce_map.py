#!/usr/bin/env python3

"""Roll up the geo6 json to produce a tree suitable for sub9 query"""

__author__ = "H. Martin"
__version__ = "0.1.0"

import json
import math
from random import randint


data = {}
transformed = {}


with open('geohash_counter_6.json', encoding='utf-8') as data_file:
    data = json.loads(data_file.read())

for geo6 in data:
    geohash_info = {}
    count = math.ceil(data[geo6] * 0.1)
    geohash_info['count'] = count

    geo4 = geo6[:4]
    if geo4 not in transformed:
        transformed[geo4] = {"count":0}
    transformed[geo4]["count"] += count
    geo5 = geo6[:5]
    if geo5 not in transformed[geo4]:
        transformed[geo4][geo5] = {"count":0}
    transformed[geo4][geo5]["count"] += count
    transformed[geo4][geo5][geo6] = geohash_info

with open('full_map.json', 'w', encoding='utf-8') as outfile:
    json.dump(transformed, outfile, indent=2)