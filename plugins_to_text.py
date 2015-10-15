#see what reports are already in the database to compare to spreadsheet and lists of other files
from pymongo import MongoClient #why must this be specified this way
import sys

#specify database and collection
database_to_use = sys.argv[1]
reports_collection = sys.argv[2]
file_to_create = sys.argv[3]

#open file to write output to
f = open(file_to_create, 'w')

#create MongoClient and connect to the db and use the appropriate collection
client = MongoClient()
db = client[database_to_use]
collection = db[reports_collection]

#iterate over every document in the collection and print the name of the report to the file
for plugin in collection.find({}, {'name': 1}):
    str_plugin = str(plugin['name'])
    strip_plugin1 = str_plugin.replace("[u'","")
    strip_plugin2 = strip_plugin1.replace("', u'"," ")
    pretty_plugin = strip_plugin2.replace("']","")
    print pretty_plugin

