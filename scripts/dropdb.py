#
# dropdb.py - drop a mongo database, with name supplied as 
#             command line argument 
#
# usage:      python3 dropdb.py <your-database-name>
#
import sys
import pymongo

def confirm(dbname):
    while True:
        prompt = '%s %s? %s|%s: ' % ("delete db ", sys.argv[1],  "y", "n")
        answer = input(prompt)
        if (answer == "y" or answer == "Y"):
            return True
        elif (answer == "n" or answer == "N"):
            return False
        else:
            print("y or n?")
       

if (len(sys.argv) != 2):
    print("usage: python3 dropdb.py <dbname>")
    exit()

if (confirm("call311-test") == False):
    exit()

client = pymongo.MongoClient("mongodb://localhost:27017/")
client.drop_database(sys.argv[1])

print("done")