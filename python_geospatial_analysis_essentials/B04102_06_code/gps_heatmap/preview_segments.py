import psycopg2
import mapnik

connection = psycopg2.connect(database="gps_heatmap", user="postgres")
cursor = connection.cursor()

cursor.execute("SELECT ST_XMIN(ST_EXTENT(centerline)), " +
               "ST_YMIN(ST_EXTENT(centerline)), " +
               "ST_XMAX(ST_EXTENT(centerline)), " +
               "ST_YMAX(ST_EXTENT(centerline)) " +
               "FROM road_segments")
min_long,min_lat,max_long,max_lat = cursor.fetchone()

min_long = min_long
min_lat = min_lat
max_long = max_long
max_lat = max_lat

extent = mapnik.Envelope(min_long, min_lat,  max_long, max_lat)
aspectRatio = extent.width() / extent.height()

mapWidth = 1200
mapHeight = int(mapWidth / aspectRatio)
if mapHeight > 800:
    scaleFactor = float(800) / float(mapHeight)
    mapWidth = int(mapWidth * scaleFactor)
    mapHeight = int(mapHeight * scaleFactor)

map = mapnik.Map(mapWidth, mapHeight)
map.background = mapnik.Color("white")

layer = mapnik.Layer("roads")
layer.datasource = mapnik.PostGIS(host='localhost',
                                  user='postgres',
                                  password='',
                                  dbname='gps_heatmap',
                                  table='road_segments')
layer.styles.append("road_style")
map.layers.append(layer)

line_symbol = mapnik.LineSymbolizer(mapnik.Color("black"), 0.5)

rule = mapnik.Rule()
rule.symbols.append(line_symbol)

style = mapnik.Style()
style.rules.append(rule)

map.append_style("road_style", style)

map.zoom_to_box(extent)
mapnik.render_to_file(map, "map.png", "png")
