import mapnik
import psycopg2

#############################################################################

MAX_WIDTH = 1200
MAX_HEIGHT = 800
MIN_TALLY = 3

#############################################################################

def calc_stroke(value, max_value):
    """ Return the mapnik.Stroke to use for drawing a given heatmap value.

        'value' will be between 0 and 'max_value'.
    """
    fraction = float(value) / float(max_value) # 0..1.

    def interpolate(start_value, end_value, fraction):
        return start_value + (end_value - start_value) * fraction

    r = interpolate(0.7, 0.0, fraction)
    g = interpolate(0.7, 0.0, fraction)
    b = interpolate(1.0, 0.4, fraction)

    color = mapnik.Color(int(r*255), int(g*255), int(b*255))
    width = max(4.0 * fraction, 1.5)

    return mapnik.Stroke(color, width)

#############################################################################

# Open the database, and get the maxium tally value in our database.  We'll
# use this to calculate the bands to use to color the streets on the
# heatmap.

connection = psycopg2.connect(database="gps_heatmap", user="postgres")
cursor = connection.cursor()

cursor.execute("SELECT max(tally) FROM road_segments")
max_tally = cursor.fetchone()[0]

cursor.execute("SELECT ST_XMIN(ST_EXTENT(centerline)), " +
               "ST_YMIN(ST_EXTENT(centerline)), " +
               "ST_XMAX(ST_EXTENT(centerline)), " +
               "ST_YMAX(ST_EXTENT(centerline)) " +
               "FROM road_segments WHERE tally >= %s" % MIN_TALLY)
min_long,min_lat,max_long,max_lat = cursor.fetchone()

# Calculate the dimensions of the map.

extent = mapnik.Envelope(min_long, min_lat,  max_long, max_lat)
aspectRatio = extent.width() / extent.height()

mapWidth = MAX_WIDTH
mapHeight = int(mapWidth / aspectRatio)
if mapHeight > MAX_HEIGHT:
    scaleFactor = float(MAX_HEIGHT) / float(mapHeight)
    mapWidth = int(mapWidth * scaleFactor)
    mapHeight = int(mapHeight * scaleFactor)

# Create our map object.

map = mapnik.Map(mapWidth, mapHeight)
map.background = mapnik.Color("white")

# Define our unused road layer.

layer = mapnik.Layer("unused_roads")
layer.datasource = mapnik.PostGIS(host='localhost',
                                  user='postgres',
                                  password='',
                                  dbname='gps_heatmap',
                                  table='road_segments')
layer.styles.append("unused_road_style")
map.layers.append(layer)

# Set up our unused road layer style.

line_symbol = mapnik.LineSymbolizer(mapnik.Color("#c0c0c0"), 1.0)

rule = mapnik.Rule()
rule.filter = mapnik.Filter("[tally] = 0")
rule.symbols.append(line_symbol)

style = mapnik.Style()
style.rules.append(rule)
map.append_style("unused_road_style", style)

# Define our used road layer.

layer = mapnik.Layer("used_roads")
layer.datasource = mapnik.PostGIS(host='localhost',
                                  user='postgres',
                                  password='',
                                  dbname='gps_heatmap',
                                  table='road_segments')
layer.styles.append("used_road_style")
map.layers.append(layer)

# Set up our used road layer style.

style = mapnik.Style()

for tally in range(1, max_tally+1):
    line_symbol = mapnik.LineSymbolizer()
    line_symbol.stroke = calc_stroke(tally, max_tally)

    rule = mapnik.Rule()
    rule.filter = mapnik.Filter("[tally] = %d" % tally)
    rule.symbols.append(line_symbol)

    style.rules.append(rule)

map.append_style("used_road_style", style)

# Render the map.

map.zoom_to_box(extent)
mapnik.render_to_file(map, "heatmap.png", "png")

