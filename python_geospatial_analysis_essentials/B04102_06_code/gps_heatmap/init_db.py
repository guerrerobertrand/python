import psycopg2

connection = psycopg2.connect(database="gps_heatmap", user="postgres")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS roads")
cursor.execute("CREATE TABLE roads (" +
                   "id SERIAL PRIMARY KEY," +
                   "name VARCHAR," + 
                   "centerline GEOMETRY)")
cursor.execute("CREATE INDEX ON roads USING GIST(centerline)")

cursor.execute("DROP TABLE IF EXISTS road_segments")
cursor.execute("CREATE TABLE road_segments (" +
               "id SERIAL PRIMARY KEY," +
               "name VARCHAR," + 
               "centerline GEOMETRY," +
               "tally INTEGER)")
cursor.execute("CREATE INDEX ON road_segments USING GIST(centerline)")

cursor.execute("DROP TABLE IF EXISTS directed_segments")
cursor.execute("CREATE TABLE directed_segments (" +
               "id SERIAL PRIMARY KEY," +
               "road_segment_id INTEGER," +
               "centerline GEOMETRY)")
cursor.execute("CREATE INDEX ON directed_segments USING GIST(centerline)")

cursor.execute("DROP TABLE IF EXISTS endpoints")
cursor.execute("CREATE TABLE endpoints (" +
               "id SERIAL PRIMARY KEY," +
               "endpoint GEOMETRY)")
cursor.execute("CREATE INDEX ON endpoints USING GIST(endpoint)")

cursor.execute("DROP TABLE IF EXISTS endpoint_segments")
cursor.execute("CREATE TABLE endpoint_segments (" +
               "id SERIAL PRIMARY KEY," +
               "directed_segment_id INTEGER," +
               "endpoint_id INTEGER)")
cursor.execute("CREATE INDEX ON endpoint_segments(directed_segment_id)")
cursor.execute("CREATE INDEX ON endpoint_segments(endpoint_id)")

connection.commit()
