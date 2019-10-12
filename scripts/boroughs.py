#
# boroughs.py   - select 311 call data for 2017 to present, and 
#                 filter out requests that lack lat/lng 
#                 coordinates (about 3%)
#
# preconditions:  (none)
#
# usage:  python3 boroughs.py  <your-database-name>
#
import sys
import os

if (len(sys.argv) != 2):
    print("usage: python3 boroughs.py  <your-database-name>")
    exit()

cmd = 'mongoimport --db=' + sys.argv[1] + ' --collection=boroughs ' \
            ' --type=json --file=../data/boroughs.json --drop'
os.system(cmd)
print("done")