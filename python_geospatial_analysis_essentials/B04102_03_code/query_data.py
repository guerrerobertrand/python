""" query_data.py

    This program is intended to accompany chapter 3 of Python Geospatial
    Analysis.  It performs various database queries against the PostGIS
    database imported by the import_data.py program.
"""
import psycopg2

#############################################################################

def main():
    """ Our main program.
    """
    # Open a connection to the database.

    connection = psycopg2.connect(database="world_borders",
                                  user="postgres")
    cursor = connection.cursor()

    # A simple non-spatial query:

    cursor.execute("SELECT id,name FROM borders ORDER BY name")
    for row in cursor:
        print row

    # A spatial query to find all countries within 1,000 kilometres of Paris:

    lat    = 48.8567
    long   = 2.3508
    radius = 1000000

    cursor.execute("SELECT name FROM borders WHERE ST_DWITHIN(" +
                   "ST_MakePoint(%s, %s), outline, %s)", (long, lat, radius))
    for row in cursor:
        print row[0]

#############################################################################

if __name__ == "__main__":
    main()

