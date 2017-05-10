# Parse a delimited text file and create a shapefile
import osgeo.ogr as ogr
import osgeo.osr as osr
import csv
import time

start_time = time.clock()


# use a dictionary reader so we can access by field name
reader = csv.DictReader(open("C:\_Tools\Python_BG\shiftPointswork\stops_new.txt","rb"),delimiter=',',quoting=csv.QUOTE_NONE)

# set up the shapefile driver
driver = ogr.GetDriverByName("ESRI Shapefile")

# create the data source
data_source = driver.CreateDataSource("C:\_Tools\Python_BG\shiftPointswork\stops_out.shp")

# create the spatial reference, WGS84
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

# create the layer
layer = data_source.CreateLayer("stops_new", srs, ogr.wkbPoint)

# Add the fields we're interested in
field_iden = ogr.FieldDefn("stop_id", ogr.OFTString)
field_iden.SetWidth(24)
field_name = ogr.FieldDefn("stop_name", ogr.OFTString)
field_name.SetWidth(24)

layer.CreateField(field_iden)
layer.CreateField(field_name)
layer.CreateField(ogr.FieldDefn("stop_lat", ogr.OFTReal))
layer.CreateField(ogr.FieldDefn("stop_lon", ogr.OFTReal))

# empty list 
duplicates = []	#duplicates x/y to shift
coordinates = [] #unique x/y to keep


# unique x/y list
for row in reader:
	#print(float(row['stop_lon']),float(row['stop_lat']))
	x = float(row['stop_lon'])
	y = float(row['stop_lat'])
	point =(x,y)
	coordinates.append(point)
	coordinates = list(set(coordinates))

	print("uniques are =")
	for idx, coord in enumerate(coordinates):
		print idx, coord[0], coord[1]

	print("shift duplicates")	
	# Process the text file and add the attributes and features to the shapefile
	
	# create the feature
	feature = ogr.Feature(layer.GetLayerDefn())
	# Set the attributes using the values from the delimited text file
	feature.SetField("stop_id", row['stop_id'])
	feature.SetField("stop_name", row['stop_name'])
	
	test =(float(row['stop_lon']),float(row['stop_lat']))
	if test not in coordinates:
		# shift
		feature.SetField("stop_lat", float(row['stop_lat'])+0.000001)
		feature.SetField("stop_lon", float(row['stop_lon'])+0.000001)
	else:	
		feature.SetField("stop_lat", row['stop_lat'])
		feature.SetField("stop_lon", row['stop_lon'])
  
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




# # Parse a delimited text file and create a shapefile
# import csv
# import time
# from shapely.geometry import Point, mapping
# from fiona import collection


# start_time = time.clock()

# schema = { 'geometry': 'Point', 'properties': { 'stop_id': 'str', 'stop_name': 'str', 'stop_lon': 'float', 'stop_lat': 'float' } }
# with collection("C:\_Tools\Python_BG\shiftPointswork\stops_new.shp", "w", "ESRI Shapefile", schema) as output:

	# # use a dictionary reader so we can access by field name
	# reader = csv.DictReader(open("C:\_Tools\Python_BG\shiftPointswork\stops_new.txt","r"),delimiter=',',quoting=csv.QUOTE_NONE)

	# for row in reader:
		# #print (row)
		# point = Point(float(row['stop_lon']), float(row['stop_lat']))
		# uniques = (list(point.coords))
		
		# prev_point = None
		# for point in uniques:
			# #print (point.coords)
			# if prev_point is not None and point.coords == prev_point.coords:
				# # do something with prev_point
				# prev_point.x = float(point.x)+0.000001
				# prev_point.y = float(point.y)+0.000001
			# else:
				# print("nothing to do")
				# # do something different
		# prev_point = point
		
		# # output.write({
			# # 'properties': {
				# # 'stop_name': row['stop_name']
			# # },
			# # 'geometry': mapping(point)
		# # })
# print("Let's process duplicates")	
# '''
	# Read the doc : http://toblerity.org/shapely/manual.html
	# like : objet1.equals(objet2) avec 2 points successifs ?
# '''


# elapsed_time = time.clock() - start_time
# print ("Time elapsed: {} seconds".format(elapsed_time))