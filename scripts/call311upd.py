#
# call311upd.py - geojoin requests and neighborhoods to assign 
#                 a neighborhood name to each request
#
# preconditions:  these scripts have been run:
#                 dropdb.py     download     select311.py     
#                 neighborhoods.py
#
# usage:  python3 call311upd.py  <your-database-name>
#
import sys
import pymongo

if (len(sys.argv) != 2):
    print("usage: python3 call311upd.py  <your-database-name>")
    exit()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client[sys.argv[1]]
colNhoods = db["nhoodgeo"]
colRequests = db['requests']
cur = colNhoods.find()
updCount = 0
for rec in cur:
    #print(rec['geodata']['properties']['neighborhood'])
    geo = rec['geodata']['geometry']
    nh  = rec['neighborhood']
    print(nh)

    filter = {"location": {"$geoWithin": {"$geometry": geo}}}
    upd    = {"$set": {"neighborhood": nh}}
    res    = colRequests.update_many(filter, upd)
   # print(res.modified_count)
print("{} request rows updated with neighborhood".format(updCount))
print("done")
