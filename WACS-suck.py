#!/usr/bin/env python3
# coding=<UTF-8>

"""
#version 0.2
# by John Wood -- for Tech Advance
# This script takes a Wycliffe Associates Content Service (WACS) username and downloads all repos for that user
# into the current directory (creating subdirectories for each repo as normal).
#
# It uses command-line git on the system, so that should be installed.
# Usage python3 WACS-suck.py <username>
"""

#Import necessary python components

import argparse
import requests
import json
import os
import sys

parser = argparse.ArgumentParser(description="Download all repositories from a given user on WACS")
parser.add_argument("username", help="Username on WACS")
#parser.add_argument('--lang', dest='lang')

args = parser.parse_args()

BASEURL = "https://content.bibletranslationtools.org"

arguments=sys.argv[1:]
count_args=len(arguments)
print("WACS-suck - to pull down all repos from a WACS user. © 2020\n")
if count_args!=1: #If there is not exactly one argument, fail with a usage remark.
    if count_args == 0:
        print ("WACS-suck.py script to download all repos from a WACS user")
        print("Usage: python3 WACS-suck.py <username>")
    elif count_args > 1:
        print ("WACS-suck.py currently only handles one username at a time.")
        print ("If you are trying to specify a destination, please run this command")
        print ("    from the destination directory")
    sys.exit(1)

userName=sys.argv[1]

userURL = BASEURL + "/api/v1/users/search?q=" + userName

userResponse = requests.get(userURL)

userID = json.loads(userResponse.content)["data"][0]["id"]

print("WACS user ",userName," has user ID ",userID,"\n")

pageNumber = 1
pleaseLoop = True

while pleaseLoop:
    cloneURLRequest = BASEURL+"/api/v1/repos/search?uid="+str(userID)+"&page="+str(pageNumber)
    newResponse = requests.get(cloneURLRequest)
    newContent = (json.loads(newResponse.content))
    if len(newContent["data"]) == 0:
        break
    for record in newContent["data"]:
        cloneCommand = 'git clone ' + record["clone_url"]
        os.system(cloneCommand)
    pageNumber += 1