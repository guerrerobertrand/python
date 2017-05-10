# calc_lengths.py
#
# This program calculates the length of each road in the USA.  It is intended
# as an example for Chapter 5 of the book Python Geospatial Analysis.

import osgeo.ogr
import shapely.wkt
import pyproj

#############################################################################

geod = pyproj.Geod(ellps="WGS84")

shapefile = osgeo.ogr.Open("tl_2014_06_prisecroads/" +
                           "tl_2014_06_prisecroads.shp")
layer = shapefile.GetLayer(0)

for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    geometry = shapely.wkt.loads(feature.GetGeometryRef().ExportToWkt())

    lineStrings = []
    if geometry.geom_type == "LineString":
        lineStrings.append(geometry)
    elif geometry.geom_type == "MultiLineString":
        for lineString in geometry:
            lineStrings.append(lineString)

    tot_length = 0

    for lineString in lineStrings:
        prev_long,prev_lat = lineString.coords[0]
        for cur_long,cur_lat in lineString.coords[1:]:
            heading1,heading2,distance = geod.inv(prev_long, prev_lat,
                                                  cur_long, cur_lat)
            tot_length = tot_length + distance
            prev_long,prev_lat = cur_long,cur_lat

    print feature.GetField("FULLNAME"), int(tot_length)

