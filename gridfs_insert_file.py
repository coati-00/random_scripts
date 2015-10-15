#first version of script very manual --> entering individual files while analyzing them
import sys
from pymongo import Connection
from gridfs import GridFS

download_path = sys.argv[1]
download_name = sys.argv[2]
download_origin = sys.argv[3]

db = Connection().db_name
fs = GridFS(db, 'collection_name')

with open(download_path) as put_download:
    oid = fs.put(put_download, name=download_name, origin=download_origin)
