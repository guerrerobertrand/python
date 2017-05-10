import osgeo.ogr
import shapely.wkt

#############################################################################

def main():
    """ Our main program.
    """
    shapefile = osgeo.ogr.Open("TM_WORLD_BORDERS-0.3.shp")
    layer = shapefile.GetLayer(0)

    countries = {} # Maps country name to Shapely geometry.

    for i in range(layer.GetFeatureCount()):
        feature = layer.GetFeature(i)
        country = feature.GetField("NAME")
        outline = shapely.wkt.loads(feature.GetGeometryRef().ExportToWkt())

        countries[country] = outline

    print "Loaded %d countries" % len(countries)

    for country in sorted(countries.keys()):
        outline = countries[country]
        for other_country in sorted(countries.keys()):
            if country == other_country: continue
            other_outline = countries[other_country]
            if outline.touches(other_outline):
                print "%s borders %s" % (country, other_country)

#############################################################################

if __name__ == "__main__":
    main()

