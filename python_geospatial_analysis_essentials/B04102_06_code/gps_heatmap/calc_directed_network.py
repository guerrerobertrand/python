import networkx
import psycopg2
import shapely.wkt
import shapely.geometry

connection = psycopg2.connect(database="gps_heatmap", user="postgres")
cursor = connection.cursor()

network = networkx.Graph()

cursor.execute("SELECT id,ST_AsText(centerline) FROM road_segments")
for row in cursor:
    road_segment_id,wkt = row
    linestring = shapely.wkt.loads(wkt)

    first_pt = linestring.coords[0]
    last_pt  = linestring.coords[-1]

    network.add_edge(first_pt, last_pt, {'road_segment_id' : road_segment_id})

sub_graphs = list(networkx.connected_component_subgraphs(network))
largest = sub_graphs[0]

cursor.execute("DELETE FROM endpoints")

endpoint_ids = {} # Maps (long,lat) coordinate to record ID in database.
for node in largest.nodes():
    point = shapely.geometry.Point(node)
    wkt = shapely.wkt.dumps(point)

    cursor.execute("INSERT INTO endpoints (endpoint) " +
                   "VALUES (ST_GeomFromText(%s)) RETURNING id", (wkt,))
    endpoint_id = cursor.fetchone()[0]

    endpoint_ids[node] = endpoint_id

cursor.execute("DELETE FROM directed_segments")
cursor.execute("DELETE FROM endpoint_segments")

for node1,node2 in largest.edges():
    endpoint_id_1 = endpoint_ids[node1]
    endpoint_id_2 = endpoint_ids[node2]
    road_segment_id = largest.get_edge_data(node1, node2)['road_segment_id']

    cursor.execute("SELECT ST_AsText(centerline) " +
                   "FROM road_segments WHERE id=%s",
                   (road_segment_id,))
    wkt = cursor.fetchone()[0]
    linestring = shapely.wkt.loads(wkt)

    reversed_coords = list(reversed(linestring.coords))

    if node1 == linestring.coords[0]:
        forward_linestring = linestring
        reverse_linestring = shapely.geometry.LineString(reversed_coords)
    else:
        reverse_linestring = linestring
        forward_linestring = shapely.geometry.LineString(reversed_coords)

    cursor.execute("INSERT INTO directed_segments " +
                   "(road_segment_id,centerline) VALUES " +
                   "(%s, ST_GeomFromText(%s)) RETURNING id",
                   (road_segment_id, forward_linestring.wkt))
    forward_segment_id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO directed_segments " +
                   "(road_segment_id,centerline) VALUES " +
                   "(%s, ST_GeomFromText(%s)) RETURNING id",
                   (road_segment_id, reverse_linestring.wkt))
    reverse_segment_id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO endpoint_segments " +
                   "(directed_segment_id, endpoint_id) VALUES (%s, %s)",
                   (forward_segment_id, endpoint_id_1))

    cursor.execute("INSERT INTO endpoint_segments " +
                   "(directed_segment_id, endpoint_id) VALUES (%s, %s)",
                   (reverse_segment_id, endpoint_id_2))

connection.commit()
