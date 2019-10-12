#
# sumcall311.py - summarize requests by neighborhood and 
#                 complaint type to produce a collection of
#                 summary counts
#
# preconditions:  these scripts have been run:
#                 dropdb.py     download     select311.py     
#                 neighborhoods.py   call311upd.py
#
# usage:  python3 sumcall311.py  <your-database-name>
#
import sys
import pymongo

if (len(sys.argv) != 2):
    print("usage: python3 sumcall311.py  <your-database-name>")
    exit()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client[sys.argv[1]]
col = db['requests']
colOut = db["nhoodcounts"]
colOut.drop()

pipeline = [
    {"$group": {"_id": {"complaint": "$complaint", "neighborhood": "$neighborhood"}, "count": {"$sum": 1}}},
    {"$project": {"neighborhood": "$_id.neighborhood", 
        "complaint": "$_id.complaint", "count": 1, "_id": 0}},
    {"$out": "nhoodcounts"}
]
col.aggregate(pipeline)
print("done")

