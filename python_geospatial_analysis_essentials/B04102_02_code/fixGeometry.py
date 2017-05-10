# Example Python code to repair an invalid Shapely Polygon or MultiPolygon.

def fix_geometry(geometry):
    buffer_worked = True
    try:
        geometry = geometry.buffer(0)
    except:
        buffer_worked = False

    if buffer_worked:
        return geometry

    polygons = []
    if geometry.geom_type == "Polygon":
        polygons.append(geometry)
    elif geometry.geom_type == "MultiPolygon":
        polygons.extend(geometry.geoms)

    fixed_polygons = []
    for n,polygon in enumerate(polygons):
        if not linear_ring_is_valid(polygon.exterior):
            continue # Unable to fix.

        interiors = []
        for ring in polygon.interiors:
            if linear_ring_is_valid(ring):
                interiors.append9ring)

        fixed_polygon = shapely.geometry.Polygon(polygon.exterior,
                                                 interiors)

        try:
            fixed_polygon = fixed_polygon.buffer(0)
        except:
            continue

        if fixed_polygon.geom_type == "Polygon":
            fixed_polygons.append(fixed_polygon)
        elif fixed_polygon.geom_type == "MultiPolygon":
            fixed_polygons.extend(fixed_polygon.geoms)

    if len(fixed_polygons) > 0:
        return shapely.geometry.MultiPolygon(fixed_polygons)
    else:
        return None # Unable to fix.


def linear_ring_is_valid(ring):
    points = set() # Set of (x,y) tuples.

    for x,y in ring.coords:
        points.add((x,y))

    if len(points) < 3:
        return False
    else:
        return True

