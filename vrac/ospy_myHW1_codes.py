#Open Source Python 1 : Reading & writing vector data
####################################################

# hw_1a : Read coordinates & attibutes from a shapefile

#1. Import needed modules
import ogr, os, sys

#1. set the working directory
os.chdir('/Users/bertrand/Documents/gis/programmation/Python/opensource_python_GIS/ospy_data1')

#2. Open the output text file
file = open('output_coord_attr.txt', 'w')

#3. Get the shapefile driver
driver = ogr.GetDriverByName('ESRI Shapefile')

#4. Open sites.shp
datasource = driver.Open('sites.shp',0)
if datasource is None:
	print 'Could not open file'
	sys.exit(1)

#4. Get the data layer
layer = datasource.GetLayer()

#5. Loop through the features in the layer
feature = layer.GetNextFeature()
while feature:

	#a. Get attributes for the current feature
	id = feature.GetFieldAsString('id')
  	cover = feature.GetFieldAsString('cover')

	#b. Get the geometry and x,y coordinates
	geom = feature.GetGeometryRef()
	x = str(geom.GetX())
	y = str(geom.GetY())

	#c. write info out to the text file
	file.write(id + ' ' + x + ' ' + y + ' ' + cover + '\n')

	# destroy the feature and get the next feature
	feature.Destroy()
	feature = layer.GetNextFeature()

#6. Destroy the datasource
datasource.Destroy()

#6. Close the output text file
file.close()