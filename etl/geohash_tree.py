#!/usr/bin/env python3

"""Roll up the geo6 json to produce a tree suitable for sub9 query"""

__author__ = "H. Martin"
__version__ = "0.1.0"

import json

max_depth = 4
alphabet = "0123456789bcdefghjkmnpqrstuvwxyz"

def get_tree(prefix, current_depth):
    t = {}
    for a in alphabet:
        if current_depth < max_depth:
            t[prefix + a] = get_tree(prefix + a, current_depth + 1)
        else:
            t[prefix + a] = {}
    return t

tree = get_tree("", 0)
# print(tree)
with open('tree5.json', 'w', encoding='utf-8') as outfile:
    json.dump(tree, outfile, indent=2)