# vue311-database
Database scripts for NYC Neighborhood project

Software Requirements
 
1. python 3.6+
2. pymongo module for python mongodb client
3. mongodb

The inputs to this project are:

1. Raw file of NYC 311 calls from 2010 to present.
2. Geojson file of NYC borough boundaries.
3. Geojson file of NYC neighborhoods.

The above inputs are processed mainly by short python scripts, and the data
gets loaded to a mongodb database. 

Scripts (in scripts directory):

1. runmefirst.py     - verifies that all required python modules are installlled
2. dropdb.py         - drop any previously created call311 database
3. download          - manual procedure to download 311 call data from NYC site
4. select311.py      - select data for 2017 - present, filter out calls that are missing lat/lng, load to mongo db
5. complaints.py     - summarize 311 calls by complaint type, put output in a new collection.
6. neighborhoods.py  - read neighborhood file, augment it with bounding box and area, write to new collection.
7. call311upd.py     - do a geojoin with neighborhoods and 311 calls and assign a neighborhood to each request.
8. sumcall311.py     - compute complaint counts by neighborhood and store in a new collection. 
9. boroughs.py       - load borough boundaries to database 
10. cleanup.py        - remove requests collection (not needed once summary collections are created).

Final call311 Database

  |collection   | description                                  |
  |------------ |--------------------------------------------- |
  |complaints   | complaint types                              |
  |boroughs     | NYC borough boundaries                       |
  |neighborhoods| NYC neighborhood boundaries                  |
  |nhoodcounts  | Counts by complaint type and neighborhood    |

