# calc_shortest_path.py
#
# This program calculates the shortest path between two points.  It is intended
# as an example for Chapter 5 of the book Python Geospatial Analysis.

import shapely.wkt
import pyproj
import networkx

#############################################################################

def calc_distance(lat1, long1, lat2, long2):
    """ Return the distance between two points, in meters.
    """
    geod = pyproj.Geod(ellps="WGS84")
    heading1,heading2,distance = geod.inv(long1, lat1, long2, lat2)
    return distance

#############################################################################

def calc_length(linestring):
    """ Return the length of the given EPSG 4326 linestring, in meters.
    """
    tot_length = 0
    prev_long,prev_lat = linestring.coords[0]
    for cur_long,cur_lat in linestring.coords[1:]:
        distance = calc_distance(prev_lat, prev_long, cur_lat, cur_long)
        tot_length = tot_length + distance
        prev_long,prev_lat = cur_long,cur_lat
    return int(tot_length)

#############################################################################

def get_coord(prompt):
    """ Prompt the user to enter a lat/long value.
    """
    while True:
        s = raw_input(prompt + " (lat,long): ")
        if "," not in s: continue
        s1,s2 = s.split(",", 1)
        try:
            latitude = float(s1.strip())
        except ValueError:
            continue
        try:
            longitude = float(s2.strip())
        except ValueError:
            continue
        return latitude,longitude

#############################################################################

def find_closest_node(graph, latitude, longitude):
    """ Find the node in the graph closest to the given point.
    """
    closest_node = None
    min_distance = None
    for node in graph.nodes():
        distance = calc_distance(node[1], node[0], latitude, longitude)
        if closest_node == None:
            closest_node = node
            min_distance = distance
        elif distance < min_distance:
            closest_node = node
            min_distance = distance
    return closest_node

#############################################################################

print "Loading road network into memory..."

graph = networkx.read_shp("split_roads/split_roads.shp")
print "graph has %d nodes and %d edges" % (len(graph.nodes()),
                                           len(graph.edges()))

graph = networkx.connected_component_subgraphs(graph.to_undirected()).next()

print "Calculating road lengths..."

num_roads = len(graph.edges())
num_done = 0
for node1,node2 in graph.edges():
    if num_done % 1000 == 0:
        print "  %d%% done" % int(100 * float(num_done) / float(num_roads))
    num_done = num_done + 1

    wkt = graph[node1][node2]['Wkt']
    linestring = shapely.wkt.loads(wkt)
    length = calc_length(linestring)
    graph.edge[node1][node2]['length'] = length

print

start_lat, start_long = get_coord("Starting Coordinate")
end_lat, end_long = get_coord("Ending Coordinate")

start_node = find_closest_node(graph, start_lat, start_long)
end_node   = find_closest_node(graph, end_lat, end_long)

print "start node = " + str(start_node)
print "end node = " + str(end_node)

path = networkx.shortest_path(graph, start_node, end_node, "length")

tot_length = 0
prev_node = path[0]
for cur_node in path[1:]:
    edge = graph.edge[prev_node][cur_node]
    print (str(prev_node) + " -> " + str(cur_node) +
           ", length = " + str(edge['length']))
    tot_length = tot_length + edge['length']
    prev_node = cur_node

print "Total length = " + str(tot_length)

# Oakland to San Luis Obespo:
# Starting Coordinate (lat,long): 37.794189, -122.276469
# Ending Coordinate (lat,long): 35.281107, -120.661211

