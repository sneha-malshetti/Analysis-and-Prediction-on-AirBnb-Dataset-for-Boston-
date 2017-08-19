# coding: utf-8

# In[ ]:




import os
import boto3
from boto.s3.connection import S3Connection
import json
import boto.s3
import sys
import datetime
from boto.s3.key import Key
import pandas as pd
import urllib
import numpy as np
import gzip
import requests
import sys
# import urllib2
import os
import errno
from time import sleep
import threading
from threading import Thread
import zipfile
import csv
# import vlc
import time
from playsound import playsound
import matplotlib as plt
import matplotlib.pyplot as plt
import pandas as pd
import urllib
import zipfile
import json
from pprint import pprint
import re
from bs4 import BeautifulSoup as BS, BeautifulSoup
import io
import requests
import glob
import logging
import logging.handlers
# from urllib.request import urlopen
import urllib.request

import time
from pygame import mixer  # Load the required library

## Importing JSON File contents
with open('config.json') as data_file:
    data = json.load(data_file)

DIR_NAME = data["DIR_NAME"]
# verbose = data["VERBOSE"]

## Getting the City Names from the JSON File
city1 = data["CITY1"]
city2 = data["CITY2"]
print (city1, city2)

AWSAccess = data["AWSAccess"]
AWSSecret = data["AWSSecret"]

# Generating date string

datestr2 = time.strftime("%d%m%Y%H%M%S")
datestr2 = datestr2[0:4] + datestr2[-8:-6]

# log generation of files on local directory

LOG_FILENAME = datestr2 + '.log'
# Set up a specific logger with our desired output level
my_logger = logging.getLogger('MyLogger')

if not my_logger.handlers:
    my_logger.setLevel(logging.DEBUG)

    # Add the log message handler to the logger
    handler = logging.handlers.TimedRotatingFileHandler(filename=LOG_FILENAME, when='d', interval=1,
                                                        backupCount=120)

    my_logger.addHandler(handler)
    # create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# add formatter to handler
handler.setFormatter(formatter)

# See what files are created
logfiles = glob.glob('%s*' % LOG_FILENAME)

for filename in logfiles:
    print (filename)


# .............................................Log file generated..........................................................


def log(arg):
    my_logger.info(arg)


def logprint(arg):
    print (arg)


def create_directory(dir_name):
    curr_dir = os.getcwd()
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


def remove_file(file_path):
    os.remove(file_path)


def convertstring(city):
    city = city.lower()
    city = city.replace(".", "")
    print (city)
    city = re.sub(' ', '-', city)
    print (city)
    city = re.sub(',', '-', city)
    print (city)

    logprint(city)
    return city


def getfileurls(city, filetype):

    listname = filetype+"list"
    r = requests.get("http://insideairbnb.com/get-the-data.html")
    soup = BeautifulSoup(r.content)
    links = soup.find_all("a")

    tablename = "table table-hover table-striped " + city
    logprint(tablename)
    g_data = soup.find_all("table", {"class": tablename})
    if len(g_data) == 0:
        logprint("Please Enter Proper City Name")
        my_logger.error("Invalid City Name Entered!")
        exit()

    extractedlist = []
    extratfile = filetype+".csv.gz"
    for items in g_data:
        links2 = items.find_all("a")
        for alllinks in links2:
            if extratfile in alllinks.get("href"):
                if "/united-states/" in alllinks.get("href"):
                    givenlinks = alllinks.get("href")
                    # logprint(givenlistingslink)
                    extractedlist.append(givenlinks)
                else:
                    logprint("Please Enter cities in US only !")
                    my_logger.error("Invalid Country city Entered!")
                    exit()

    for listitems in extractedlist:
        logprint(listitems)
    return extractedlist
    # logprint (listingslist)



def getmergeddata(scrapedlist, filetype, city):
    mergeddf = pd.DataFrame()
    filename = filetype+".csv.gz"
    for listitems in scrapedlist:
        logprint(listitems)
        # download = urllib.urlretrieve(listitems, 'listings.csv.gz')
        download = urllib.request.urlretrieve(listitems, filename)

        data = pd.read_csv(filename, compression='gzip', error_bad_lines=False, low_memory=False)
        # print(data)
        logprint(data.shape)
        # print (data.dtypes)

        mergeddf = pd.concat([mergeddf, data], axis=0).drop_duplicates().reset_index(drop=True)
        logprint("Shape of merged file is :" + str(mergeddf.shape))
        mergeddf = mergeddf.drop_duplicates(['id'], keep='first')
        if filetype == "listings":
            mergeddf[["city"]] = city
            logprint(mergeddf[["city"]].head(15))
        # logprint(mergeddf.head(15))
        logprint("Shape of merged file with duplicates removed is :" + str(mergeddf.shape))
        remove_file(filename)
        return mergeddf



def mergefiles(data1, data2):
    print("First File Shape : ", data1.shape)

    print("Second File Shape : ", data2.shape)

    mergeddf = pd.concat([data1, data2], axis=0)  # .drop_duplicates().reset_index(drop=True)
    logprint("Shape of merged file is :" + str(mergeddf.shape))
    mergeddf = mergeddf.drop_duplicates(['id'], keep='first')
    logprint("Shape of merged file with duplicates removed is :" + str(mergeddf.shape))
    return mergeddf


def converttocsv(df, filename):
    df.to_csv(filename, index=False)


def uploadfilestos3(filetype):
    ############Connection variables for S3
    filetype
    c = boto.connect_s3(AWSAccess, AWSSecret)
    conn = S3Connection(AWSAccess, AWSSecret)
    bucket = c.get_bucket('adsteam8finalairbnb')
    b = c.get_bucket(bucket, validate=False)

    b = c.get_bucket(bucket, validate=False)

    k = Key(bucket)
    k.key = "RawData/"+filetype+".csv"
    url = "https://s3.amazonaws.com/adsteam8finalairbnb/"
    r = requests.get(url)

    k = Key(b)
    k.key = "RawData/"+filetype+".csv"

    k.content_type = r.headers['content-type']
    k.set_contents_from_filename(filetype+'.csv')
    print('successfully uploaded '+filetype+'.csv to s3')



def startexecution(city1, city2):
    # create_directory(DIR_NAME)
    log("Program Execution Begins!")
    logprint("Program Execution Begins!")

    cstring1 = convertstring(city1)
    cstring2 = convertstring(city2)
    log("Getting the files by Scraping!")
    logprint("Getting the files by Scraping!")

    filetype1 = "listings"
    filetype2 = "reviews"
    filetype3 = "calendar"

    city1listingurllist = getfileurls(cstring1, filetype1)
    city2listingurllist = getfileurls(cstring2, filetype1)
    city1reviewurllist = getfileurls(cstring1, filetype2)
    city2reviewurllist = getfileurls(cstring2, filetype2)
    # city1calendarurllist = getfileurls(cstring1, filetype3)
    # city2calendarurllist = getfileurls(cstring2, filetype3)
    log("Retrieving Data!")
    logprint("Retrieving Data!")

    dfcity1listing = getmergeddata(city1listingurllist, filetype1, cstring1)
    dfcity2listing = getmergeddata(city2listingurllist, filetype1,cstring2)
    dfcity1review = getmergeddata(city1reviewurllist, filetype2, cstring1)
    dfcity2review = getmergeddata(city2reviewurllist, filetype2, cstring2)
    # dfcity1calendar = getmergeddata(city1calendarurllist, filetype3, cstring1)
    # dfcity2calendar = getmergeddata(city2calendarurllist, filetype3, cstring2)
    log("Merging Files!")
    logprint("Merging Files!")




    mergedfile = pd.DataFrame(mergefiles(dfcity1listing, dfcity2listing))
    logprint("Final listing.csv shape : " + str(mergedfile.shape))
    converttocsv(mergedfile, "listings.csv")
    logprint("listing.csv Created at " + time.strftime("%d/%m/%Y %H:%M:%S"))
    log("listing.csv Created at " + time.strftime("%d/%m/%Y %H:%M:%S"))
    mergedfile = pd.DataFrame(mergefiles(dfcity1review, dfcity2review))
    logprint("Final review.csv shape : " + str(mergedfile.shape))
    converttocsv(mergedfile, "reviews.csv")
    logprint("review.csv Created at " + time.strftime("%d/%m/%Y %H:%M:%S"))
    log("review.csv Created at " + time.strftime("%d%m%Y%H%M%S"))
    # mergedfile = pd.DataFrame(mergefiles(dfcity1calendar, dfcity2calendar))
    # logprint("Final calendar.csv shape : " + str(mergedfile.shape))
    # converttocsv(mergedfile, "calendar.csv")
    # logprint("calendar.csv Created at " + time.strftime("%d/%m/%Y %H:%M:%S"))
    # log("calendar.csv Created at " + time.strftime("%d%m%Y%H%M%S"))
    log("Uploading Files to S3!")
    logprint("Uploading Files to S3!")

    uploadfilestos3(filetype1)
    uploadfilestos3(filetype2)
    # uploadfilestos3(filetype3)

    log("Files Uploaded to S3!")
    logprint("YAY ! Files Uploaded to S3!")




def playsuccess():
    playsound('success.mp3')
    # mixer.init()
    # mixer.music.load('success.mp3')
    # mixer.music.play()


startexecution(city1, city2)
logprint("Program Complete")
log("Program Executed Successfully")
playsuccess()














