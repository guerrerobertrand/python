# calc_areas.py
#
# This program calculates the area of each country.  It is intended as an
# example for Chapter 5 of the book Python Geospatial Analysis.

import osgeo.ogr
import shapely.wkt
import shapely.ops
import pyproj

#############################################################################

shapefile = osgeo.ogr.Open("TM_WORLD_BORDERS-0.3/TM_WORLD_BORDERS-0.3.shp")
layer = shapefile.GetLayer(0)

def latlong_to_mollweide(longitude, latitude):
    src_proj = pyproj.Proj("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")
    dst_proj = pyproj.Proj("+proj=moll +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 " +
                           "+datum=WGS84 +units=m +no_defs")
    return pyproj.transform(src_proj, dst_proj, longitude, latitude)

for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    geometry = shapely.wkt.loads(feature.GetGeometryRef().ExportToWkt())

    transformed = shapely.ops.transform(latlong_to_mollweide, geometry)
    area = int(transformed.area/1000000)

    print feature.GetField("NAME"), area

