from bs4 import BeautifulSoup
from subprocess import call
import urllib
import os
import sys
import fileinput
import re


htmlfile = "case_id_110_id_754.html"
htmldoc = open(htmlfile, 'rw')


'''Remove leading empty lines from files with leading empty lines'''


# problem with this is that it checks everyline - want to check beginning lines
# short cut - check first two lines only
# later - check all lines UNTIL first non empty line... while not empty?
f = open(htmlfile, 'r+')
temphold = f.readlines()
f.seek(0)
for line in temphold:
    if line !='\n':
        f.write(line)
f.truncate()
f.close()

'''clean up bottom of document so beautiful soup doesn't
get confused and start formatting it further...'''
f = open(htmlfile, 'r+')
temphold = f.readlines()
f.seek(0)
for line in temphold:
    if line !='\n':
        f.write(line)
f.truncate()
f.close()



'''finally - make the html human friendly...'''
# clean up formatting of html...
htmldoc = open(htmlfile, 'rw')
soup = BeautifulSoup(htmldoc, 'html.parser')

soup = soup.prettify()

print(soup)



#file_to_search = sys.argv[1]


# def search_folders(file_name):
#     for path, subdirs, files in os.walk(file_name):
#         files.sort()
#         for f_name in files:
#             '''Remove duplicate html files ending with _pid_0.html'''
#             if "_pid_0" in f_name:
#                 print "Removing file : " + str(f_name)
#                 file_path = os.path.join(path, f_name)
#                 call(["git", "rm", file_path])
# 
#     # go over directory second time - # of files
#     # to update should be smaller
#     for path, subdirs, files in os.walk(file_name):
#         files.sort()
#         for f_name in files:
#             if "case_id_" in f_name:
#                 print "Updating file " + str(f_name)
#                 file_path = os.path.join(path, f_name)
#                 old_string = "_pid_0.html"
#                 new_string = ".html"
#                 newfile = open(file_path, 'r+')
#                 for line in fileinput.input(file_path):
#                     newfile.write(line.replace(old_string, new_string))
#                 newfile.close()
# 
# search_folders(file_to_search)

