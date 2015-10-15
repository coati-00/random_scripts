#go through all elements of file and get the md5, sha1 and the name and insert with a tag which is name of the directory
#currently does not account for subdirs


from pymongo import Connection
from gridfs import GridFS
from subprocess import *
import os
import sys

sha1sum = ''
plugin_name = ''

#take care of set up - get appropriate info from user to get files from the specified folder
download_path = sys.argv[1]
download_origin = sys.argv[2]


#establish connection
db = Connection().my_re_tools
gfs = GridFS(db, 'practice_ida_downloads')

def get_sha1(sha_file):
    sha1sum = Popen(["sha1sum", sha_file], stdout=PIPE)
    sha1_found = sha1sum.stdout.read()
    sha_split = sha1_found.split()
    sha1_final = sha_split[0]
    return sha1_final

def get_plugin_name(f_name):
    if f_name.endswith(".zip"):
        p_name = f_name[:-4]
    if f_name.endswith(".rar"):
        p_name = f_name[:-4]
    if f_name.endswith(".tar.gz"):
        p_name = f_name[:-7]
    if f_name.endswith(".tgz"):
        p_name = f_name[:-4]
    return p_name

def get_downloads(file_name):
    for path, subdirs, files in os.walk(file_name):
        files.sort()
        for f_name in files:
            file_path = os.path.join(path,f_name)
            sha1 = get_sha1(os.path.join(path,f_name))
            plugin_name = get_plugin_name(f_name)
            test = f_name + " " + download_origin + " " + plugin_name + " " + str(sha1)
            print test
            with open(file_path) as insert_db:
                oid = gfs.put(file_path, name=plugin_name, sha1=sha1, origin=download_origin)



#call proceeding methods
get_downloads(download_path)
