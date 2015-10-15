#go through all elements of the directory and subdirectory and move the found .rar .zip .tar.gz and .tgz files to another folder names for the source from which the plugins were obtained
from subprocess import call
import os
import sys

#get source and destination folder
file_to_search = sys.argv[1]
destination_file = sys.argv[2]

def is_plugin(f_name):
    if f_name.endswith(".zip"):
        return True
    if f_name.endswith(".rar"):
        return True
    if f_name.endswith(".tar.gz"):
        return True
    if f_name.endswith(".tgz"):
        return True

def move_downloads(file_name):
    for path, subdirs, files in os.walk(file_name):
        files.sort()
        for f_name in files:
            if(is_plugin(f_name)):
                file_path = os.path.join(path,f_name)
                call(["cp", file_path, destination_file])

#call proceeding methods
move_downloads(file_to_search)
