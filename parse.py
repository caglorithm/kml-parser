#!/usr/bin/python

# GOOGLE LOCATION SERVICE KML PARSER (0.1)
# This was tested only with the kml's that are produced by Google from your
# Android phones location data.
# If you have enabled the location reporting on your phone you can view
# the location data on an interactive map at
# https://maps.google.com/locationhistory/
#
# You can download the kml file of your location data using this link
# https://maps.google.com/locationhistory/b/0/kml?startTime=0&endTime=2383260400000
# It will request the location saved from the beginning of time until a very
# far timestamp in the future, so everything you ever submitted should be included.
#
#
# Contact: sevensirk@gmail.com


# Name or path to the kml file to parse
docname = 'big.kml'
#docname = 'medium.kml'

# Save your custom locations here
# Format is [(x-coord), (y-cood), (radius), name]
# Coordinates have to be put in decimals! For exmaple 49.006033 instead of something
# like 49    0'21.72". 
# A radius of 0.004 has proven to be reasonable for a place like a home or workplace.
# (Python beginners: don't forget to add a colon (,) at the end of the old last line
# and don't forget to shift the new line that you add properly to match the other lines)
locations = [
    [11.373078, 33.490044, 0.004, 'Home'], 
    [13.436339, 62.43989, 0.004, 'Gym'], 
    [43.224808, 83.777223, 0.004, 'Uni'],  
    [76.321394, 12.520386, 0.004, 'Work'],  
    [11.679979, 10.132989, 0.004, 'Someplace'],
    [9.104267, 49.186033, 0.05, 'Disneyland']
]

import requests
from xml.etree import ElementTree
import sys, getopt
from math import *
import xml.dom.minidom as XM
import datetime as dt

#import matplotlib.pyplot as plt
if (len(sys.argv)>1):
    docname = sys.argv[1]
    
def get_google_loc(x,y):
    url = "https://maps.googleapis.com/maps/api/geocode/xml?latlng=%f,%f&sensor=true"%(y,x)
    #print "GET ", url
    response = requests.get(url)
    tree = ElementTree.fromstring(response.content)
    return tree[1][1].text

print "parsing %s ... (this may take a while)" %docname
document = XM.parse(docname)

numlocations = len(locations)
locdays = []
notlocdays = 0
locdate = []
lastdate = dt.date(1,1,1)
when = []
date = [] #datetime object
day = []
month = []
year = []
rawtime = []
time = [] #datetime object
xpos = []
ypos = []
where = []

foo = document.getElementsByTagName("gx:coord")
nrelements = len(foo)

    
for i in range(0,nrelements):
    wob = foo[i].childNodes
    where.append(wob[0].data)
    xpos.append(float(where[i].split(" ")[0]))
    ypos.append(float(where[i].split(" ")[1]))

print "> coordinates parsed ..."

wob = []    
foo = document.getElementsByTagName("when")

for i in range(0,nrelements):
    wob = foo[i].childNodes
    when.append(wob[0].data) 
    rawtime.append(when[i].split("T")[1].split("-")[0])
    year.append(int(when[i].split("-")[0]))
    month.append(int(when[i].split("-")[1]))    
    day.append(int(when[i].split("-")[2][:2]))
    date.append(dt.date(year[i],month[i],day[i],))
    time.append(dt.time(int(rawtime[i].split(":")[0]) , int(rawtime[i].split(":")[1]) , int(rawtime[i].split(":")[2][:2]))) #int(rawtime[i].split(":")[2][3:])*1000 )) 
    
print "> dates and times parsed ..."

# set default fromdate, todate
#fromdate = date[0]
#todate = date[nrelements-1]
fromdate = dt.date(2014,3,6)
todate = dt.date(2014,3,9)

for a in range(0,numlocations):
    locdate.append(fromdate-dt.timedelta(1))
    locdays.append(0)
    
delta = todate-fromdate    
print "> Locations from %s to %s (%s days)"%(fromdate, todate,delta.days)

for a in range(0,nrelements-1):
    if (fromdate < date[a] < todate):
        for b in range(0,numlocations):
            if (fabs(xpos[a]-locations[b][0])<locations[b][2] and fabs(ypos[a]-locations[b][1])<locations[b][2] and date[a] != locdate[b]):
                #print "%s on %s at %s pos: %f %f"%(locations[b][3],date[a],time[a],ypos[a],xpos[a])
                locdate[b] = date[a]
                locdays[b] += 1
                lastdate = locdate[b]
            for c in range(0,numlocations):
                if (locdate[c]>lastdate):
                    lastdate = locdate[c]
            if (date[a]>lastdate+dt.timedelta(1)): # haven't been there any known location yesterday?
                print "unknown location @%s pos: %f %f"%(lastdate+dt.timedelta(1),ypos[a],xpos[a])
                lastdate += dt.timedelta(1)
                notlocdays += 1
                
                # THIS IS EXPERIMENTAL CODE TO DETERMINE THE LOCATION OF A GPS COORDINATE
                
                print get_google_loc(xpos[a],ypos[a])

        #plt.scatter(x=[xpos[a]], y=[ypos[a]], s = 5, c='r') #plot each point

print "> results from", delta.days, "days (", fromdate, "-", todate, "):"
for a in range(0,numlocations):
    if (locdays[a]):
        print "     %dx at %s" %(locdays[a],locations[a][3])
print "     %dx no location" %(notlocdays)

# graphing...
#plt.xlabel('Longitude')
#plt.ylabel('Latitude')
#plt.title('POSITION from %s to %s'%(fromdate, todate)) 
#implot = plt.imshow(im,extent=[BLX, TRX, BLY, TRY])
#plt.show()

