#
# neighborhoods.py - augment neighborhoods geojson with bounding box 
#                    and area (square meters)
#
# preconditions:   - uses nhoodraw.json from github repo
#
# usage:  python3 neighborhoods.py  <your-database-name>
#
import sys
import json
import pymongo
from area import area
import numpy as np
from UliEngineering.Math.Coordinates import BoundingBox
import math

if (len(sys.argv) != 2):
    print("usage: python3 neighborhoods.py  <your-database-name>")
    exit()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client[sys.argv[1]]
col = db["neighborhoods"]
col.drop()

def trm(num):
    return math.floor(num * 1000000) / 1000000

with open('../data/nhoodraw.json') as json_in:
    data = json.load(json_in)
    for n in data['neighborhoods']:
        nh = n['properties']['neighborhood']
        cor = n['geometry']
        ar = round(area(cor), 0)
        n['properties']['area'] = ar
        cor = n['geometry']['coordinates']
        cor2 = np.asarray(cor[0])
        bb = BoundingBox(cor2)
        n['properties']['minlng'] = trm(bb.minx)
        n['properties']['maxlng'] = trm(bb.maxx)
        n['properties']['minlat'] = trm(bb.miny)
        n['properties']['maxlat'] = trm(bb.maxy)
        #have area at this point in properties
        rec = {"neighborhood": nh, "geodata": n}
        col.insert_one(rec)

print("done")