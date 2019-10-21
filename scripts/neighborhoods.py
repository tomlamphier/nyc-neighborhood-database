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
colNeighborhoods = db["neighborhoods"]
colNeighborhoods.drop()
colNhoodbounds = db["nhoodbounds"]
colNhoodbounds.drop()
colNhoodgeo    = db["nhoodgeo"]
colNhoodgeo.drop() 

def trm(num):
    return math.floor(num * 1000000) / 1000000

nhoods = {}

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
        #rec = {"neighborhood": nh, "geodata": n}
        rec = {"neighborhood": nh, "borough": n['properties']['borough'],
           "minlng": trm(bb.minx), "maxlng": trm(bb.maxx),
           "minlat": trm(bb.miny), "maxlat": trm(bb.maxy),
           "area": ar}

        if nh in nhoods:
            rec2 = nhoods[nh]
            if (rec2['minlng'] < rec['minlng']):
                rec['minlng'] = rec2['minlng']
            if (rec2['maxlng'] > rec['maxlng']):
                rec['maxlng'] = rec2['maxlng']
            if (rec2['minlat'] < rec['minlat']):
                rec['minlat'] = rec2['minlat']
            if (rec2['maxlat'] > rec['maxlat']):
                rec['maxlat'] = rec2['maxlat']
            rec['area'] += rec2['area']
        nhoods[nh] = rec

        recNhoodgeo = {"neighborhood": nh, 
            "geodata": {"type": "Feature", 
               "properties": {
               "neighborhood": nh, "borough": n['properties']['borough'],
               "area": ar, "minlng": rec['minlng'],
               "maxlng": rec['maxlng'],
               "minlat": rec['minlat'],
               "maxlat": rec['maxlat']},
            "geometry": {
               "type": "Polygon",
               "coordinates": cor}}}
        colNhoodgeo.insert_one(recNhoodgeo)
                       
        #rec1 = {"neighborhood": nh, "borough": n['properties']['borough']}
        #col1.insert_one(rec1)

    for elem in nhoods:
        val = nhoods[elem]
        recNeighborhood = {"neighborhood": elem, "borough": val['borough']}
        colNeighborhoods.insert_one(recNeighborhood)

        recNhoodbounds = {"neighborhood": elem, "minlng": val['minlng'],
          "maxlng": val['maxlng'], "minlat": val['minlat'],
          "maxlat": val['maxlat'], "area": val['area']}
        colNhoodbounds.insert_one(recNhoodbounds)
client.close()
print("done")
