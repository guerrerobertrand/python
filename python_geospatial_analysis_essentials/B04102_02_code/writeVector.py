# Sample program to write vector-format data.

from osgeo import ogr
from osgeo import osr

driver = ogr.GetDriverByName("ESRI Shapefile")
dstFile = driver.CreateDataSource("test-shapefile")

spatialReference = osr.SpatialReference()
spatialReference.SetWellKnownGeogCS("WGS84")

layer = dstFile.CreateLayer("layer", spatialReference)

field = ogr.FieldDefn("NAME", ogr.OFTString)
field.SetWidth(100)
layer.CreateField(field)

wkt = "POLYGON((23.4 38.9, 23.5 38.9, 23.5 38.8, 23.4 38.9))"
polygon = ogr.CreateGeometryFromWkt(wkt)

feature = ogr.Feature(layer.GetLayerDefn())
feature.SetGeometry(polygon)
feature.SetField("NAME", "My Polygon")

layer.CreateFeature(feature)
feature.Destroy()

dstFile.Destroy()
