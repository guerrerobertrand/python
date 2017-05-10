import psycopg2
import shapely.wkt
import shapely

connection = psycopg2.connect(database="gps_heatmap", user="postgres")
cursor = connection.cursor()

cursor.execute("DELETE FROM road_segments")

all_road_ids = []
cursor.execute("SELECT id FROM roads")
for row in cursor:
    all_road_ids.append(row[0])

for road_id in all_road_ids:
    cursor.execute("SELECT name,ST_AsText(centerline) " +
                   "FROM roads WHERE id=%s", (road_id,))
    name,wkt = cursor.fetchone()
    cur_road = shapely.wkt.loads(wkt)

    crossroads = [] # List of Shapely geometry objects.
    cursor.execute("SELECT ST_AsText(centerline) FROM ROADS " +
                   "WHERE ST_Touches(roads.centerline, " +
                   "ST_GeomFromText(%s)) OR ST_Crosses(" +
                   "roads.centerline, ST_GeomFromText(%s))",
                   (wkt, wkt))
    for row in cursor:
        crossroad = shapely.wkt.loads(row[0])
        crossroads.append(crossroad)

    for crossroad in crossroads:
        cur_road = cur_road.difference(crossroad)

    segments = [] # List of Shapely geometry objects.
    if cur_road.geom_type == "MultiLineString":
        for segment in cur_road.geoms:
            segments.append(segment)
    elif cur_road.geom_type == "LineString":
        segments.append(cur_road)

    for segment in segments:
        centerline_wkt = shapely.wkt.dumps(segment)
        cursor.execute("INSERT INTO road_segments (name, " +
                       "centerline, tally) VALUES (%s, " +
                       "ST_GeomFromText(%s), %s)",
                       (name, centerline_wkt, 0))

connection.commit()

