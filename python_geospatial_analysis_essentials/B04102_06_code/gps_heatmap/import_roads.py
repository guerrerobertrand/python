import psycopg2
from osgeo import ogr

connection = psycopg2.connect(database="gps_heatmap", user="postgres")
cursor = connection.cursor()

cursor.execute("DELETE FROM roads")

shapefile = ogr.Open("roads/improved-nz-road-centrelines-august-2011.shp")
layer = shapefile.GetLayer(0)

for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    geometry = feature.GetGeometryRef()

    if feature.GetField("descr") != None:
        name = feature.GetField("descr")
    elif feature.GetField("label") != None:
        name = feature.GetField("label")
    else:
        name = None

    centerline_wkt = geometry.ExportToWkt()

    cursor.execute("INSERT INTO roads (name, centerline) " +
                   "VALUES (%s, ST_GeomFromText(%s))",
                   (name, centerline_wkt))

connection.commit()

