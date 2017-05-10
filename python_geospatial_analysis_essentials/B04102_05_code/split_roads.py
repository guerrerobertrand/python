# split_roads.py
#
# This program converts the downloaded road data into a planar graph, allowing
# it to be used to calculate the shortest path between two points.  It is
# intended as an example for Chapter 5 of the book Python Geospatial Analysis.

import os
import os.path
import shutil
import osgeo.ogr
import osgeo.osr
import shapely.wkt

#############################################################################

print "Loading shapefile..."

SRC_SHAPEFILE = "tl_2014_06_prisecroads/tl_2014_06_prisecroads.shp"

all_roads = []
shapefile = osgeo.ogr.Open(SRC_SHAPEFILE)
layer = shapefile.GetLayer(0)
for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    geometry = shapely.wkt.loads(feature.GetGeometryRef().ExportToWkt())
    all_roads.append(geometry)

print "Loaded %d roads" % len(all_roads)
print "Splitting roads..."

split_roads = []

for i in range(len(all_roads)):
    print i
    cur_road = all_roads[i]
    crossroads = []
    for j in range(len(all_roads)):
        if i == j: continue
        other_road = all_roads[j]
        if cur_road.crosses(other_road):
            crossroads.append(other_road)
    if len(crossroads) > 0:
        for other_road in crossroads:
            cur_road = cur_road.difference(other_road)
        if cur_road.geom_type == "MultiLineString":
            for split_road in cur_road.geoms:
                split_roads.append(split_road)
        elif cur_road.geom_type == "LineString":
            split_roads.append(cur_road)
    else:
        split_roads.append(cur_road)

print "Saving results to split_roads.shp..."

driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
if os.path.exists("split_roads"):
    shutil.rmtree("split_roads")
os.mkdir("split_roads")
dstFile = driver.CreateDataSource("split_roads/split_roads.shp")

spatialReference = osgeo.osr.SpatialReference()
spatialReference.SetWellKnownGeogCS("WGS84")

layer = dstFile.CreateLayer("Layer", spatialReference)

for road in split_roads:
    wkt = shapely.wkt.dumps(road)
    linestring = osgeo.ogr.CreateGeometryFromWkt(wkt)

    feature = osgeo.ogr.Feature(layer.GetLayerDefn())
    feature.SetGeometry(linestring)
    
    layer.CreateFeature(feature)
    feature.Destroy()

dstFile.Destroy()

