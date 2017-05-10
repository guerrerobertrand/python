""" shapeToMap.py

    This example program displays the contents of a shapefile.  It is intended
    to be used as part of Chapter 4 of the book Python Geospatial Analysis.
"""
import mapnik
import os

LAYERS = [
    {'shapefile'  : "TM_WORLD_BORDERS-0.3/TM_WORLD_BORDERS-0.3.shp",
     'lineColor'  : "black",
     'lineWidth'  : 0.4,
     'fillColor'  : "#709070",
     'labelField' : None,
     'labelSize'  : None,
     'labelColor' : None,
    },
    {'shapefile'  : "TM_WORLD_BORDERS-0.3/TM_WORLD_BORDERS-0.3.shp",
     'lineColor'  : None,
     'lineWidth'  : None,
     'fillColor'  : None,
     'labelField' : "NAME",
     'labelSize'  : 12,
     'labelColor' : "black"
    }
]

BACKGROUND_COLOR = "#a0c0ff"

BOUNDS_MIN_LAT  = 35.26
BOUNDS_MAX_LAT  = 71.39
BOUNDS_MIN_LONG = -10.90
BOUNDS_MAX_LONG = 41.13

MAX_WIDTH  = 1600
MAX_HEIGHT = 800

#############################################################################

def main():
    """ Our main program.
    """
    # Calculate the size of the map image, based on the specified bounds.

    extent = mapnik.Envelope(BOUNDS_MIN_LONG, BOUNDS_MIN_LAT,
                             BOUNDS_MAX_LONG, BOUNDS_MAX_LAT)
    aspectRatio = extent.width() / extent.height()

    mapWidth = MAX_WIDTH
    mapHeight = int(mapWidth / aspectRatio)

    if mapHeight > MAX_HEIGHT:
        # Scale the map to fit.
        scaleFactor = float(MAX_HEIGHT) / float(mapHeight)
        mapWidth = int(mapWidth * scaleFactor)
        mapHeight = int(mapHeight * scaleFactor)

    # Create our map.

    map = mapnik.Map(mapWidth, mapHeight)
    map.background = mapnik.Color(BACKGROUND_COLOR)

    # Define the styles used to show the contents of each shapefile.

    for i,src in enumerate(LAYERS):
        style = mapnik.Style()
        rule = mapnik.Rule()

        if src.get("filter") != None:
            rule.filter = mapnik.Filter(src['filter'])

        if src['fillColor'] != None:
            symbol = mapnik.PolygonSymbolizer(mapnik.Color(src['fillColor']))
            rule.symbols.append(symbol)
        if src['lineColor'] != None:
            symbol = mapnik.LineSymbolizer(mapnik.Color(src['lineColor']),
                                           src['lineWidth'])
            rule.symbols.append(symbol)
        if src['labelField'] != None:
            symbol = mapnik.TextSymbolizer(mapnik.Expression(
                            "[" + src['labelField'] + "]"),
                            "DejaVu Sans Bold",
                            src['labelSize'],
                            mapnik.Color(src['labelColor']))
            if src.get("labelHalo") != None:
                symbol.halo_radius = src['labelHalo']
            if src.get("labelPlacement") == "line":
                symbol.label_placement = mapnik.label_placement.LINE_PLACEMENT
            symbol.allow_overlap = True
            rule.symbols.append(symbol)

        style.rules.append(rule)

        map.append_style("style-"+str(i+1), style)

    # Setup our various map layers.

    for i,src in enumerate(LAYERS):
        layer = mapnik.Layer("layer-"+str(i+1))
        layer.datasource = mapnik.Shapefile(file=src['shapefile'])
        layer.styles.append("style-"+str(i+1))
        map.layers.append(layer)

    # Finally, render the map.

    map.zoom_to_box(extent)
    mapnik.render_to_file(map, "map.png", "png")

    os.system("open map.png")

#############################################################################

if __name__ == "__main__":
    main()

