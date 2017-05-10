""" import_data.py

    This program is intended to accompany chapter 3 of Python Geospatial
    Analysis.  It imports the contents of the "TM_WORLD_BORDERS-0.3.shp"
    shapefile into a Postgres database.
"""
import osgeo.ogr
import psycopg2

#############################################################################

def main():
    """ Our main program.
    """
    # Open a connection to the database.

    connection = psycopg2.connect(database="world_borders",
                                  user="postgres")
    cursor = connection.cursor()

    # Delete the existing records, if any.

    cursor.execute("DELETE FROM borders")

    # Process the contents of the shapefile.

    shapefile = osgeo.ogr.Open("TM_WORLD_BORDERS-0.3/TM_WORLD_BORDERS-0.3.shp")
    layer = shapefile.GetLayer(0)

    for i in range(layer.GetFeatureCount()):
        feature  = layer.GetFeature(i)
        name     = feature.GetField("NAME")
        iso_code = feature.GetField("ISO3")
        geometry = feature.GetGeometryRef()
        wkt      = geometry.ExportToWkt()

        cursor.execute("INSERT INTO borders (name, iso_code, outline) VALUES (%s, %s, ST_GeogFromText(%s))", (name, iso_code, wkt))

    connection.commit()

#############################################################################

if __name__ == "__main__":
    main()

