""" generateMap.py

    This Python program loads a set of map-generation parameters from a given
    named module, and then generates a map using those parameters.

    This program is provided as an extended example of the "shapeToMap.py"
    program used in Chapter 4 of the book Python Geospatial Analysis.
"""
import os

import mapnik
import osgeo.ogr
import osgeo.osr

#############################################################################

# The following import statement should load a Python module containing the
# map-generation parameters.  The following global constants should be defined
# in the imported module:
#
#     BACKGROUND_COLOR
#
#         A string containing an HTML color code to use as the background for
#         the entire map.
#
#     OVERRIDE_MIN_LAT
#     OVERRIDE_MAX_LAT
#     OVERRIDE_MIN_LONG
#     OVERRIDE_MAX_LONG
#
#         These constants define an override boundary to use for the map.  If
#         these are set to None, the map will cover all the features in the
#         map's data sources.
#
#     BOUNDS_FILTER
#
#         If this is defined, it should be a dictionary mapping field names to
#         values.  When calculating the boundary of the map, only those
#         features which have field values matching this filter will be
#         included.  Note that this is only used if the various OVERRIDE_XXX
#         constants are set to None.
#
#     BOUNDS_MARGIN
#
#         If this is defined, it should be an angular distance (ie, a distance
#         measured as a lat/long value) that gets added to the bounds
#         calculated by the BOUNDS_FILTER parameter, above.  This lets you
#         place a simple "margin" around the calculated bounds.

#     PRINT_BOUNDS
#
#         If defined and True, the map generator will print the calculated
#         bounds to stdout.  This can be usedful when setting up OVERRIDE_XXX
#         values for later use.
#
#     LAYERS
#
#         A list of layers to display on the map.  Each list item should be a
#         dictionary with the following entries:
#
#            'sourceFile'
#
#                The name of the file to get the layer's data from.  If this
#                ends in ".shp", we will open a shapefile.  Otherwise, we will
#                use OGR to load whatever data is in the file.
#
#            'layer'
#
#                If defined, the name of a layer to pass to the OGR reader.
#                This only applies to non-shapefile data sources.
#
#            'filter'
#
#                If defined, a string filtering the features to draw.
#
#            'lineColor'
#
#                The HTML color code to use for drawing the lines, or None if
#                no lines are to be drawn.
#
#            'lineWidth'
#
#                The width of the lines, in pixels.
#
#            'lineJoin'
#
#                How to join the lines.  One of: "miter", "round", "bevel".  If
#                not defined, defaults to "miter".
#
#            'lineCap'
#
#                How to cap the end of the lines.  One of: "round", "butt" or
#                "square".  If not defined, defaults to "round".
#
#            'lineDash'
#
#                A line dash length, in pixels.  If this is not defined, the
#                line will be drawn solid.
#
#            'fillColor'
#
#                The HTML color code to use for filling the polygons, or None
#                if the polygons are not to be filled.
#
#            'labelField'
#
#                The name of the field to display as a label, or None if no
#                labels are to be displayed.
#
#            'labelSize'
#
#                The size of label's text, in points.  This should be None if
#                the labels are not displayed.
#
#            'labelColor'
#
#                The HTML color code to use for drawing the labels.  This
#                should be None if the labels are not displayed.
#
#            'labelHalo'
#
#                If defined, this should be a radius, in points, to draw a
#                white "halo" around the text.
#
#            'labelPlacement'
#
#                How to place the label onto the feature.  One of: "point" or
#                "line".  If this is not defined, defaults to "point".
#
#            'labelAllowOverlap'
#
#                If defined, this should be a boolean indicating whether or not
#                the label's text can overlap other laps.  If this is not
#                defined the label overlap will be set to True.
#
#            'printAttrs'
#
#                If defined and True, the data source's feature's attributes
#                will be printed to stdout.  This is useful for figuring out
#                which field(s) to display on the map.

from mapParams import *

#############################################################################

# The maximum width and height of each map, in pixels.  Note that the actual
# width or height of each map is likely to be smaller than these maximum
# values, depending on the map's aspect ratio.

MAX_WIDTH  = 1600
MAX_HEIGHT = 800

#############################################################################

def main():
    """ Our main program.
    """

    # Open up each layer's data source, remember the projection, and calculate
    # the overall boundary for all the displayed data that matches our bounds
    # filter.

    projections = []
    minLong     = None
    maxLong     = None
    minLat      = None
    maxLat      = None

    try:
        boundsFilter = BOUNDS_FILTER
    except NameError:
        boundsFilter = {}

    for i in range(len(LAYERS)):
        src = LAYERS[i]

        print "Processing " + src['sourceFile'] + "..."

        shapefile  = osgeo.ogr.Open(src['sourceFile'])
        layer      = shapefile.GetLayer(0)
        spatialRef = layer.GetSpatialRef()
        if spatialRef != None:
            projection = spatialRef.ExportToProj4()
        else:
            if len(projections) > 0:
                projection = projections[0]
            else:
                spatialRef = osgeo.osr.SpatialReference()
                spatialRef.SetWellKnownGeogCS('WGS84')
                projection = spatialRef.ExportToProj4()

        for i in range(layer.GetFeatureCount()):
            feature = layer.GetFeature(i)

            matches = True
            for key,value in boundsFilter.items():
                if feature.GetField(key) != value:
                    matches = False
                    break

            if not matches:
                continue

            if src.get("printAttrs") == True:
                print "  " + repr(feature.items().items())

            bounds = feature.GetGeometryRef().GetEnvelope()

            if minLong == None:
                minLong,maxLong,minLat,maxLat = bounds
            else:
                if bounds[0] < minLong: minLong = bounds[0]
                if bounds[1] > maxLong: maxLong = bounds[1]
                if bounds[2] < minLat:  minLat  = bounds[2]
                if bounds[3] > maxLat:  maxLat  = bounds[3]

        projections.append(projection)

    # Adjust the calculated bounds by the bounds margin, if any.

    try:
        minLong = minLong - BOUNDS_MARGIN
        maxLong = maxLong + BOUNDS_MARGIN
        minLat  = minLat  - BOUNDS_MARGIN
        maxLat  = maxLat  + BOUNDS_MARGIN
    except NameError:
        pass

    # If we've been asked to do so, print out the calculated bounds.

    try:
        if PRINT_BOUNDS:
            print "MIN_LAT  = %0.4f" % minLat
            print "MAX_LAT  = %0.4f" % maxLat
            print "MIN_LONG = %0.4f" % minLong
            print "MAX_LONG = %0.4f" % maxLong
    except NameError:
        pass

    # Calculate the size of the map image, based on the calculated boundaries.

    if OVERRIDE_MIN_LAT  != None: minLat  = OVERRIDE_MIN_LAT
    if OVERRIDE_MAX_LAT  != None: maxLat  = OVERRIDE_MAX_LAT
    if OVERRIDE_MIN_LONG != None: minLong = OVERRIDE_MIN_LONG
    if OVERRIDE_MAX_LONG != None: maxLong = OVERRIDE_MAX_LONG

    mapBounds = mapnik.Envelope(minLong, minLat, maxLong, maxLat)
    aspectRatio = mapBounds.width() / mapBounds.height()

    mapWidth = MAX_WIDTH
    mapHeight = int(mapWidth / aspectRatio)

    if mapHeight > MAX_HEIGHT:
        # Scale the map to fit.
        scaleFactor = float(MAX_HEIGHT) / float(mapHeight)
        mapWidth = int(mapWidth * scaleFactor)
        mapHeight = int(mapHeight * scaleFactor)

    # Create our map.

    m = mapnik.Map(mapWidth, mapHeight, projections[0])
    m.background = mapnik.Color(BACKGROUND_COLOR)

    # Setup the stylesheets to show the contents of each shapefile.

    for i in range(len(LAYERS)):
        src = LAYERS[i]

        s = mapnik.Style()
        r = mapnik.Rule()

        if src.get("filter") != None:
            r.filter = mapnik.Filter(src['filter'])

        if src['fillColor'] != None:
            ps = mapnik.PolygonSymbolizer(mapnik.Color(src['fillColor']))
            r.symbols.append(ps)
        if src['lineColor'] != None:
            stroke = mapnik.Stroke(mapnik.Color(src['lineColor']),
                                   src['lineWidth'])

            if src.get("lineJoin") == "miter":
                stroke.line_join = mapnik.line_join.MITER_JOIN
            elif src.get("lineJoin") == "round":
                stroke.line_join = mapnik.line_join.ROUND_JOIN
            elif src.get("linJoin") == "bevel":
                stroke.line_join = mapnik.line_join.BEVEL_JOIN

            if src.get("lineCap") == "round":
                stroke.line_cap = mapnik.line_cap.ROUND_CAP
            elif src.get("lineCap") == "square":
                stroke.line_cap = mapnik.line_cap.SQUARE_CAP
            elif src.get("lineCap") == "butt":
                stroke.line_cap = mapnik.line_cap.BUTT_CAP

            if src.get("lineDash") != None:
                stroke.add_dash(src['lineDash'], src['lineDash']*2)

            ls = mapnik.LineSymbolizer(stroke)
            r.symbols.append(ls)
        if src['labelField'] != None:
            ts = mapnik.TextSymbolizer(mapnik.Expression("[" +
                                                         src['labelField'] +
                                                         "]"),
                                       "DejaVu Sans Bold",
                                       src['labelSize'],
                                       mapnik.Color(src['labelColor']))
            if src.get("labelHalo") != None:
                ts.halo_radius = src['labelHalo']
            if src.get("labelPlacement") == "line":
                ts.label_placement = mapnik.label_placement.LINE_PLACEMENT
            if src.get("labelAllowOverlap") != None:
                ts.allow_overlap = src['labelAllowOverlap']
            else:
                ts.allow_overlap = True
            r.symbols.append(ts)

        s.rules.append(r)

        m.append_style("style-"+str(i+1), s)

    # Setup our various map layers.

    for i in range(len(LAYERS)):
        src = LAYERS[i]

        l = mapnik.Layer("layer-"+str(i+1), projections[i])
        if src['sourceFile'].endswith(".shp"):
            l.datasource = mapnik.Shapefile(file=src['sourceFile'])
        else:
            l.datasource = mapnik.Ogr(file=src['sourceFile'],
                                      layer=src.get("layer"))
        l.styles.append("style-"+str(i+1))
        m.layers.append(l)

    # Finally, render the map.

    m.zoom_to_box(mapBounds)
    mapnik.render_to_file(m, "map.png", "png")

    os.system("open map.png")

#############################################################################

if __name__ == "__main__":
    main()

