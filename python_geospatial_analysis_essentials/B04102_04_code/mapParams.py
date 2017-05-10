""" mapParams.py

    This Python module defines various constants used by the generateMap.py
    program to generate a map.  For documentation about these constants, please
    refer to the docstring at the top of the generateMap.py program.
"""

#############################################################################

BACKGROUND_COLOR = "#a0c0ff"

OVERRIDE_MIN_LAT  = 35.26
OVERRIDE_MAX_LAT  = 71.39
OVERRIDE_MIN_LONG = -10.90
OVERRIDE_MAX_LONG = 41.13

LAYERS = [
    {'sourceFile' : "TM_WORLD_BORDERS-0.3/TM_WORLD_BORDERS-0.3.shp",
     'lineColor'  : "black",
     'lineWidth'  : 0.4,
     'fillColor'  : "#709070",
     'labelField' : None,
     'labelSize'  : None,
     'labelColor' : None,
    },
    {'sourceFile' : "TM_WORLD_BORDERS-0.3/TM_WORLD_BORDERS-0.3.shp",
     'lineColor'  : None,
     'lineWidth'  : None,
     'fillColor'  : None,
     'labelField' : "NAME",
     'labelSize'  : 12,
     'labelColor' : "black"
    }
]

