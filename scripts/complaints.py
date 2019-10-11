#
# complaints.py - roll up complaint types into a summary, 
#                 output result as a collection
#
# preconditions:  download and select311 scripts have been run
#
# usage:  python3 complaints.py  <your-database-name>
#
import sys
import pymongo

if (len(sys.argv) != 2):
    print("usage: python3 complaints.py  <your-database-name>")
    exit()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client[sys.argv[1]]
col = db["requests"]
colTemp = db["tempcomplaints"]
colTemp.drop()

pipeline = [
    {"$group": {"_id": "$complaint", "count": {"$sum": 1}}},
    {"$out": "tempcomplaints"}
]
col.aggregate(pipeline)

maxpipeline = [
    {"$sort": {"count": -1}},
    {"$limit": 1}
]

res = list(db.tempcomplaints.aggregate(maxpipeline))
maxcount = res[0]["count"]
lvl1 = maxcount / 5
lvl2 = lvl1 * 2
lvl3 = lvl1 * 3
lvl4 = lvl1 * 4
colFinal = db["complaints"]
colFinal.drop()
temprecs = db.tempcomplaints.find()
for row in temprecs:
    level = ""
    if (row["count"] < lvl1):
        level = "Very Low"
    elif(row["count"] < lvl2):
        level = "Low"
    elif(row["count"] < lvl3):
        level = "Moderate"
    elif(row["count"] < lvl4):
        level = "High"
    else:
        level = "Very High"

    rec = {"type": row["_id"], "level": level}
    colFinal.insert_one(rec)

db.tempcomplaints.drop()
print("done")