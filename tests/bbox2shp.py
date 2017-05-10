'''
Created on 7 déc. 2015

@author: Bertrand
'''


##################
#     Imports    #
##################
import sys, getopt
import os, codecs
import time
import csv
from codecs import open
import sqlite3
import math
from datetime import datetime, timedelta, date
import ogr
import shapely
from shapely.geometry import mapping, Polygon
import fiona
import osgeo.osr as osr

print ("\n Get Bounding Box for this GTFS \n")

start_time = time.clock()
print ("BEGIN")

file = "C:\\Users\\Bertrand\\Downloads\\stops.txt"

print("Process file : " + file)

longitudes = []
latitudes = []

# Loop over files and remove Columns for each case
with open(file,"r") as infile:
    #print("agency query")
    dr = csv.DictReader(infile) # comma is default delimiter
    for i in dr:
        #print(i["stop_lon"], i["stop_lat"])
        longitudes.append(i["stop_lon"])
        latitudes.append(i["stop_lat"])

xMin = min(longitudes)
xMax = max(longitudes)
yMin = min(latitudes)
yMax = max(latitudes)

print(xMin, yMin, " et ", xMax, yMax)

print ("END")

elapsed_time = time.clock() - start_time
print ("Time elapsed: {} seconds".format(elapsed_time))

print ("\n Create Polygon shapefile  \n")

start_time = time.clock()
print ("BEGIN")

# envelope
leftOrigin = xMin
rightOrigin = xMax
topOrigin = yMax
bottomOrigin = yMin

# create output file

# set up the shapefile driver
driver = ogr.GetDriverByName("ESRI Shapefile")

# create the data source
data_source = driver.CreateDataSource("C:\\Users\\Bertrand\\Downloads\\out")

# create the spatial reference, WGS84
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)


layer = data_source.CreateLayer("gtfsPolyBBox", srs, ogr.wkbPolygon)
#poly = Polygon([(xMin, yMin), (xMin, yMax), (xMax, yMin), (xMax, yMax)])

# create the feature
feature = ogr.Feature(layer.GetLayerDefn())

#####
#temp
# layer = ds.CreateLayer(ds.GetName(), geom_type = ogr.wkbPolygon, srs =t_srs)
# geom = ogr.Geometry(type = layer.GetLayerDefn().GetGeomType())
# geom.AssignSpatialReference(t_srs)
# wkt = 'POLYGON('+x0+','+y0+','+ x0+','+ y1+','+ x1+',' +y1+','+ x1+',' +y0+','+ x0+',' +y0+')

#####



# create the WKT for the feature using Python string formatting
wkt = "POLYGON(%f %f %f %f)" %  (float(xMin), float(yMin),float(xMax), float(yMax))
print(xMin, yMin, " et ", xMax, yMax)

# Create the point from the Well Known Txt
polygon = ogr.CreateGeometryFromWkt(wkt)

# Set the feature geometry using the point
feature.SetGeometry(polygon)
# Create the feature in the layer (shapefile)
layer.CreateFeature(feature)
# Destroy the feature to free resources
feature.Destroy()

# Destroy the data source to free resources
data_source.Destroy()
print ("END")

elapsed_time = time.clock() - start_time
print ("Time elapsed: {} seconds".format(elapsed_time))