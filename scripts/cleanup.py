#
# cleanup.py -    remove unnecessary mongo collection  
#
# preconditions:  all scripts run to build database
#
# usage:  python3 cleanup.py  <your-database-name>
#
import sys
import pymongo

if (len(sys.argv) != 2):
    print("usage: python3 call311upd.py  <your-database-name>")
    exit()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client[sys.argv[1]]
col = db["requests"]
col.drop()
print("done")