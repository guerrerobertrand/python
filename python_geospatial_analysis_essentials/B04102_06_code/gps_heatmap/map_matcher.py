import os
import osgeo.ogr
import shapely.geometry
import shapely.wkt
import psycopg2
import pyproj

#############################################################################

def calc_circle_with_radius(center_point, radius):
    geod = pyproj.Geod(ellps="WGS84")

    sLong,sLat = center_point
    eLong,eLat,iHeading = geod.fwd(sLong, sLat, 0, radius)

    lat_delta = abs(sLat - eLat)

    return shapely.geometry.Point(sLong, sLat).buffer(lat_delta)

#############################################################################

def calc_distance(point, geometry):
    return shapely.geometry.Point(point).distance(geometry)

#############################################################################

def calc_score(route_segments):
    total = 0
    for segment in route_segments:
        total = total + sum(segment['gps_distances'])
    return total

#############################################################################

def point_at_start_of_segment(next_point, segment):
    num_points = len(segment['gps_points'])
    if num_points > 0:
        average_distance = sum(segment['gps_distances']) / num_points

        startpoint_coord = segment['linestring'].coords[0]
        startpoint = shapely.geometry.Point(startpoint_coord)

        endpoint_coord = segment['linestring'].coords[-1]
        endpoint = shapely.geometry.Point(endpoint_coord)

        distance_to_start = calc_distance(next_point, startpoint)
        distance_to_end   = calc_distance(next_point, endpoint)

        if distance_to_start < 2 * average_distance:
            if distance_to_end > 2 * average_distance:
                return True
    return False

#############################################################################

def point_in_route_segment(point, segment):
    endpoint = shapely.geometry.Point(segment['linestring'].coords[-1])

    distance_to_linestring = calc_distance(point, segment['linestring'])
    distance_to_endpoint   = calc_distance(point, endpoint)

    if distance_to_linestring == distance_to_endpoint:
        return False

    gps_coords = []
    gps_coords.extend(segment['gps_points'])
    gps_coords.append(point)

    gps_length = shapely.geometry.LineString(gps_coords).length

    segment_length = segment['linestring'].length

    if gps_length > segment_length:
        return False

    return True

#############################################################################

def route_is_valid(route, route_candidates, new_candidates):
    route_roads = route['directed_segment_ids']

    for other_route in route_candidates:
        if route_roads == other_route['directed_segment_ids']:
            return False

    for other_route in new_candidates:
        if route_roads == other_route['directed_segment_ids']:
            return False

    if len(route['segments']) >= 2:
        last_segment = route['segments'][-1]
        prev_segment = route['segments'][-2]

        last_segment_end   = last_segment['linestring'].coords[-1]
        prev_segment_start = prev_segment['linestring'].coords[0]

        if last_segment_end == prev_segment_start:
            # This route doubles back on itself -> not valid.
            return False

    directed_segment_ids = set()
    for segment in route['segments']:
        directed_segment_id = segment['directed_segment_id']
        if directed_segment_id in directed_segment_ids:
            # This route uses the same section of road twice -> not valid.
            return False
        else:
            directed_segment_ids.add(directed_segment_id)

    return True

#############################################################################

def develop_route(next_point, route, route_candidates, cursor):
    if len(route['segments']) == 1:
        if point_at_start_of_segment(next_point, route['segments'][0]):
            return []

    last_segment = route['segments'][-1]

    if point_in_route_segment(next_point, last_segment):
        next_distance = calc_distance(next_point, last_segment['linestring'])
        last_segment['gps_points'].append(next_point)
        last_segment['gps_distances'].append(next_distance)
        route['score'] = calc_score(route['segments'])
        return [route]

    last_point = last_segment['linestring'].coords[-1]
    endpoint = shapely.geometry.Point(last_point)

    cursor.execute("SELECT id FROM endpoints " +
                   "WHERE endpoint=ST_GeomFromText(%s)", (endpoint.wkt,))
    endpoint_id = cursor.fetchone()[0]

    possible_segment_ids = []
    cursor.execute("SELECT directed_segment_id FROM endpoint_segments " +
                   "WHERE endpoint_id=%s", (endpoint_id,))
    for row in cursor:
        possible_segment_ids.append(row[0])

    new_candidates = []
    for directed_segment_id in possible_segment_ids:
        cursor.execute("SELECT road_segment_id,ST_AsText(centerline) " +
                       "FROM directed_segments " +
                       "WHERE id=%s", (directed_segment_id,))
        road_segment_id,wkt = cursor.fetchone()
        linestring = shapely.wkt.loads(wkt)

        next_distance = calc_distance(next_point, linestring)

        new_segment = {}
        new_segment['directed_segment_id'] = directed_segment_id
        new_segment['linestring'] = linestring
        new_segment['gps_points'] = [next_point]
        new_segment['gps_distances'] = [next_distance]

        new_candidate = {}
        new_candidate['segments'] = []
        new_candidate['segments'].extend(route['segments'])
        new_candidate['segments'].append(new_segment)
        new_candidate['directed_segment_ids'] = []
        new_candidate['directed_segment_ids'].extend(
                            route['directed_segment_ids'])
        new_candidate['directed_segment_ids'].append(directed_segment_id)

        if not route_is_valid(new_candidate, route_candidates, new_candidates):
            continue

        new_candidate['score'] = calc_score(new_candidate['segments'])
        new_candidates.append(new_candidate)

    return new_candidates

#############################################################################

gps_tracks = []
for fName in os.listdir("gps-data"):
    if fName.endswith(".gpx"):
        print "Loading GPS tracks from " + fName + "..."
        srcFile = osgeo.ogr.Open("gps-data/" + fName)
        layer = srcFile.GetLayerByName("tracks")

        for feature_num in range(layer.GetFeatureCount()):
            feature = layer.GetFeature(feature_num)
            geometry = feature.GetGeometryRef()

            if geometry.GetGeometryName() == "MULTILINESTRING":
                for geom_num in range(geometry.GetGeometryCount()):
                    wkt = geometry.GetGeometryRef(geom_num).ExportToWkt()
                    gps_tracks.append((fName, wkt))
            elif geometry.GetGeometryName() == "LINESTRING":
                wkt = geometry.ExportToWkt()
                gps_tracks.append((fName, wkt))

connection = psycopg2.connect(database="gps_heatmap", user="postgres")
cursor = connection.cursor()

cursor.execute("UPDATE road_segments SET tally=0")
connection.commit()

for fName,track_wkt in gps_tracks:

    print "Processing " + fName

    gps_track  = shapely.wkt.loads(track_wkt)
    gps_points = list(gps_track.coords)

    while len(gps_points) > 0:
        circle = calc_circle_with_radius(gps_points[0], 10)

        cursor.execute("SELECT count(*) FROM road_segments " +
                       "WHERE ST_INTERSECTS(ST_GeomFromText(%s), " +
                       "centerline)", (circle.wkt,))
        if cursor.fetchone()[0] == 0:
            del gps_points[0]
        else:
            break

    while len(gps_points) > 0:
        circle = calc_circle_with_radius(gps_points[-1], 10)

        cursor.execute("SELECT count(*) FROM road_segments " +
                       "WHERE ST_INTERSECTS(ST_GeomFromText(%s), " +
                       "centerline)", (circle.wkt,))
        if cursor.fetchone()[0] == 0:
            del gps_points[-1]
        else:
            break

    search_distance = 750
    while True:
        circle = calc_circle_with_radius(gps_points[0], search_distance)

        cursor.execute("SELECT id FROM endpoints " +
                       "WHERE ST_CONTAINS(ST_GeomFromText(%s), endpoint)",
                       (circle.wkt,))
        possible_endpoints = []
        for row in cursor:
            possible_endpoints.append(row[0])

        possible_road_segments = []
        for endpoint_id in possible_endpoints:
            cursor.execute("SELECT directed_segment_id " +
                           "FROM endpoint_segments WHERE endpoint_id=%s",
                           (endpoint_id,))
            for row in cursor:
                directed_segment_id = row[0]
                possible_road_segments.append((directed_segment_id,
                                               endpoint_id))

        route_candidates = []
        for directed_segment_id,endpoint_id in possible_road_segments:
            cursor.execute("SELECT ST_AsText(centerline) " +
                           "FROM directed_segments WHERE id=%s",
                           (directed_segment_id,))
            wkt = cursor.fetchone()[0]

            linestring = shapely.wkt.loads(wkt)

            gps_distance = calc_distance(gps_points[0], linestring)

            segment = {'directed_segment_id' : directed_segment_id,
                       'linestring'          : linestring,
                       'gps_points'          : [gps_points[0]],
                       'gps_distances'       : [gps_distance]}
            route_segments = [segment]

            score = calc_score(route_segments)

            candidate = {'segments'             : route_segments,
                         'directed_segment_ids' : [directed_segment_id],
                         'score'                : score}
            route_candidates.append(candidate)

        if len(route_candidates) >= 25:
            break
        else:
            search_distance = search_distance + 100
            continue

    for next_point in gps_points[1:]:
        num_routes_to_process = len(route_candidates)
        for i in range(num_routes_to_process):
            route = route_candidates.pop(0)
            new_candidates = develop_route(next_point, route,
                                           route_candidates, cursor)
            route_candidates.extend(new_candidates)

        while len(route_candidates) > 40:
            highest = None
            for index,route in enumerate(route_candidates):
                if highest == None:
                    highest = index
                elif route['score'] > route_candidates[highest]['score']:
                    highest = index
            del route_candidates[highest]

    best_route = None
    for route in route_candidates:
        if len(route['segments']) >= 2:
            if best_route == None:
                best_route = route
            elif route['score'] < best_route['score']:
                best_route = route

    if best_route == None:
        continue

    for segment in best_route['segments']:
        cursor.execute("SELECT road_segment_id FROM directed_segments " +
                       "WHERE id=%s", (segment['directed_segment_id'],))
        road_segment_id = cursor.fetchone()[0]
        cursor.execute("UPDATE road_segments SET tally=tally+1 WHERE id=%s",
                       (road_segment_id,))

connection.commit()
