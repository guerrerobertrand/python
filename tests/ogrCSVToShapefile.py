# -*- coding: utf-8 -*-
# Parse a delimited text file and create a shapefile
import osgeo.ogr as ogr
import osgeo.osr as osr
import csv
import time
import codecs

start_time = time.clock()

# def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
#     csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
#     for row in csv_reader:
#         yield [str(cell, 'utf-8') for cell in row]

#reader = unicode_csv_reader(open("C:\\Users\\Bertrand\\Downloads\\stops.txt","r"))
# use a dictionary reader so we can access by field name
reader = csv.DictReader(codecs.open("C:\\Users\\Bertrand\\Downloads\\stops.txt","r",encoding='utf-8'),delimiter=',',quoting=csv.QUOTE_NONE)

# set up the shapefile driver
driver = ogr.GetDriverByName("ESRI Shapefile")

# create the data source
outDir = "C:\\Users\\Bertrand\\Downloads\\out"
# if os.path.exists(outDir):
#         os.remove(outDir)
data_source = driver.CreateDataSource(outDir)

# create the spatial reference, WGS84
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

# create the layer
layer = data_source.CreateLayer("stops_out", srs, ogr.wkbPoint)


# Add the fields we're interested in
field_iden = ogr.FieldDefn("stop_id", ogr.OFTString)
field_iden.SetWidth(24)
field_name = ogr.FieldDefn("stop_name", ogr.OFTString)
field_name.SetWidth(24)

layer.CreateField(field_iden)
layer.CreateField(field_name)
layer.CreateField(ogr.FieldDefn("stop_lat", ogr.OFTReal))
layer.CreateField(ogr.FieldDefn("stop_lon", ogr.OFTReal))


# unique x/y list
for row in reader:
	# create the feature
	feature = ogr.Feature(layer.GetLayerDefn())
	# Set the attributes using the values from the delimited text file
	feature.SetField("stop_id", row['stop_id'])
	feature.SetField("stop_name", row['stop_name'])
	feature.SetField("stop_lat", float(row['stop_lat']))
	feature.SetField("stop_lon", float(row['stop_lon']))
	print(row['stop_id'],row['stop_name'],row['stop_lat'],row['stop_lon'])
	# create the WKT for the feature using Python string formatting
	wkt = "POINT(%f %f)" %  (float(row['stop_lon']) , float(row['stop_lat']))
	
	# Create the point from the Well Known Txt
	point = ogr.CreateGeometryFromWkt(wkt)
	
	# Set the feature geometry using the point
	feature.SetGeometry(point)

	# Create the feature in the layer (shapefile)
	layer.CreateFeature(feature)
	
	# Destroy the feature to free resources
	feature.Destroy()

# Destroy the data source to free resources
data_source.Destroy()

elapsed_time = time.clock() - start_time
print ("Time elapsed: {} seconds".format(elapsed_time))