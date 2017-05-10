#Open Source Python 1 : Reading & writing vector data
####################################################

# hw_1b : Copy selected features from one shapefile to another.

#1. Import needed modules
import ogr, os, sys

#1. set the working directory
os.chdir('/Users/bertrand/Documents/gis/programmation/Python/opensource_python_GIS/ospy_data1')

#2. Get the shapefile driver
driver = ogr.GetDriverByName('ESRI Shapefile')

#3. Open sites.shp
datasource = driver.Open('sites.shp',0)
if datasource is None:
	print 'Could not open file'
	sys.exit(1)

#3. Get the data layer
inLayer = datasource.GetLayer()

#4. Create an output Shapefile and get its layer
if os.path.exists('test_1b.shp'): 
	driver.DeleteDataSource('test_1b.shp')

datasource2 = driver.CreateDataSource('test_1b.shp')

if datasource2 is None:
	print 'Could not create file'
	sys.exit(1)

outLayer = datasource2.CreateLayer('test_1b', geom_type=ogr.wkbPoint)


#5. Copy the 'id' and 'cover' fields from the input layer to the output layer

	#a. Get a feature from the input layer
feature = inLayer.GetFeature(0)

	#b. Get the FieldDefn's for the id and cover fields in the input shapefile
idFieldDefn = feature.GetFieldDefnRef('id')
coverFieldDefn = feature.GetFieldDefnRef('cover')

	#c. Create new fields (id and cover) in the output shapefile
outLayer.CreateField(idFieldDefn)
outLayer.CreateField(coverFieldDefn)

#6. Get the FeatureDefn for the output layer
featureDefn = outLayer.GetLayerDefn()

#7. Loop through the input features
inFeature = inLayer.GetNextFeature()
while inFeature:

  #a. Get the cover attribute for the input feature
  cover = inFeature.GetField('cover')

  #b. Check to see if a feature field have a value (ex: cover == grass)
  if cover == 'trees':

    #i. create a new feature
    outFeature = ogr.Feature(featureDefn)

    #ii. set the geometry
    geom = inFeature.GetGeometryRef()
    outFeature.SetGeometry(geom)

    #iii. Get the attributes
    id = inFeature.GetField('id')
    
    #iv. Set the attributes to the output features
    outFeature.SetField('id', id)
    outFeature.SetField('cover', cover)

    #v. add the feature to the output layer
    outLayer.CreateFeature(outFeature)

    #vi. destroy the output feature
    outFeature.Destroy()

  #c. Destroy the input feature and get a new one
  inFeature.Destroy()
  inFeature = inLayer.GetNextFeature()

#8. Close the data sources
datasource.Destroy()
datasource2.Destroy()	