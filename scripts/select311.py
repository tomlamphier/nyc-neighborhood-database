#
# select311.py  - select 311 call data for 2017 to present, and 
#                 filter out requests that lack lat/lng 
#                 coordinates (about 3%)
#
# preconditions:  311 call rewuests have been downloaded to the 
#                 data folder as per the download script
#
# usage:  python3 select311.py  <your-database-name>
#         note: the database will be created if it does not exist
#
import sys
import csv
from decimal import Decimal
from math import floor
import pymongo
import os

#col.drop()

if (len(sys.argv) != 2):
    print("usage: python3 select311.py  <your-database-name>")
    exit()

with open('../data/call311.csv', newline='') as csvfile:
    with open('../data/call311temp.json', 'w') as tempjson:
        rdr = csv.reader(csvfile)
        ctr = 0
        nolatlng = 0
        ctrsel = 0
        for row in rdr:
            ctr += 1
            if ctr == 1:
                continue
            if ctr % 20000 == 0:
                print("{} rows processed so far".format(ctr))
            year = row[1][6:10]
            #print(year)
            if not (year >= "2017"):
                #print("dropping " + year)
                continue
            complaint = row[5]
            lat = row[38]
            lng = row[39]
            try:
                lat = Decimal(row[38])
                lng = Decimal(row[39])
            except:
                nolatlng += 1
                continue
            lat2 = float(row[38])
            lat2 = floor(lat2 * 1000000) / 1000000
            lng2 = float(row[39])
            lng2 = floor(lng2 * 1000000) / 1000000
            ctrsel += 1
            rec = '{"year": "' + year + '", "complaint": "' + complaint + '", '
            rec = rec + '"location": {"coordinates": '
            rec = rec + "[{}, {}]".format(lng2, lat2) + ', "type": "Point"}}'
            #rec = '"year": {}, "complaint": {}, "location": {"coordinates": [{}, {}], "type": "Point"}}'.format(year, type, lng2, lat2)
            #rec = '{"year": year, "complaint": complaint, "location": {"coordinates": [lng2, lat2], "type": "Point"}}'
            #col.insert_one(rec)
            tempjson.write(rec + "\n")

        cmd = 'mongoimport --db=' + sys.argv[1] + ' --collection=requests ' \
            ' --type=json --file=../data/call311temp.json --drop'
        os.system(cmd)


        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client[sys.argv[1]]
        col = db["requests"]
        #db.col.create_index( { "location": pymongo.GEO2D } )
        #db.col.create_index([("location", pymongo.GEOSPHERE)])
        col.create_index([("location", pymongo.GEOSPHERE)])
        client.close()

        print("run totals:")
        print("   records read:                 ", ctr)
        print("   missing lat / lng:            ", nolatlng)
        print("   valid recs within date range: ", ctrsel)

