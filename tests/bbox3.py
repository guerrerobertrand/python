from osgeo import ogr
import osgeo.osr as osr

import os

# Get a Layer's Extent
inShapefile = "C:\\Users\\Bertrand\\Downloads\\out\\stops_out.shp"
inDriver = ogr.GetDriverByName("ESRI Shapefile")
inDataSource = inDriver.Open(inShapefile, 0)
inLayer = inDataSource.GetLayer()
extent = inLayer.GetExtent()

# Create a Polygon from the extent tuple
ring = ogr.Geometry(ogr.wkbLinearRing)
ring.AddPoint(extent[0],extent[2])
ring.AddPoint(extent[1], extent[2])
ring.AddPoint(extent[1], extent[3])
ring.AddPoint(extent[0], extent[3])
ring.AddPoint(extent[0],extent[2])
poly = ogr.Geometry(ogr.wkbPolygon)
poly.AddGeometry(ring)

# Save extent to a new Shapefile
outShapefile = "C:\\Users\\Bertrand\\Downloads\\out\\stops_extent.shp"
outDriver = ogr.GetDriverByName("ESRI Shapefile")

# Remove output shapefile if it already exists
if os.path.exists(outShapefile):
    outDriver.DeleteDataSource(outShapefile)

# https://pcjericks.github.io/py-gdalogr-cookbook/vector_layers.html

# create the spatial reference, WGS84
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

# Create the output shapefile
outDataSource = outDriver.CreateDataSource(outShapefile)
outLayer = outDataSource.CreateLayer("stops_extent", srs, geom_type=ogr.wkbPolygon)

# Add an ID field
idField = ogr.FieldDefn("id", ogr.OFTInteger)
outLayer.CreateField(idField)

# Create the feature and set values
featureDefn = outLayer.GetLayerDefn()
feature = ogr.Feature(featureDefn)
feature.SetGeometry(poly)
feature.SetField("id", 1)
outLayer.CreateFeature(feature)

# Close DataSource
inDataSource.Destroy()
outDataSource.Destroy()