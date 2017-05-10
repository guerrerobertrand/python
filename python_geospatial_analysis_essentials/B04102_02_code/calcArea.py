# Sample program to calculate area of WGS-84 data.

from osgeo import ogr
from osgeo import osr

import shapely.wkt
wkt = "POLYGON((-73.973057 40.764356, -73.981898 40.768094, -73.958209 40.800621, -73.949282 40.796853, -73.973057 40.764356))"

polygon = ogr.CreateGeometryFromWkt(wkt)

src_spatialReference = osr.SpatialReference()
src_spatialReference.ImportFromEPSG(4326)

dst_spatialReference = osr.SpatialReference()
dst_spatialReference.ImportFromEPSG(54009)

transform = osr.CoordinateTransformation(src_spatialReference,
                                         dst_spatialReference)

polygon.Transform(transform)

outline = shapely.wkt.loads(polygon.ExportToWkt())
print outline.area

