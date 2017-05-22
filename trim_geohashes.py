#!/usr/bin/env python3

__author__ = "H. Martin"
__version__ = "0.1.0"

import io
import json

geohash_counter = {}
total_counter = 0

with open("geohash_counter.csv", "r", buffering=1, encoding="utf-8") as f:
    for line in f:
        size = 6
        total_counter += 1
        data = line.rstrip().split(",")
        geohash = data[0][:size]
        count = int(data[1])
        if geohash not in geohash_counter:
            geohash_counter[geohash] = 0
        geohash_counter[geohash] += count

        
        if total_counter % 1000000 == 0:
            print(str(total_counter))

with open('geohash_counter_'  + str(size) + '.json', 'w', encoding='utf-8') as outfile:
    json.dump(geohash_counter, outfile, indent=2)