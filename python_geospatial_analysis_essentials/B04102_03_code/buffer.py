""" buffer.py

    This program is intended to accompany chapter 3 of Python Geospatial
    Analysis.  It manipulates the data in our database to calculate a buffered
    geometry.
"""
import math
import psycopg2

#############################################################################

def main():
    """ Our main program.
    """
    # Open a connection to the database.

    connection = psycopg2.connect(database="world_borders",
                                  user="postgres")
    cursor = connection.cursor()

    # Add a new column to the database:

    try:
        cursor.execute("ALTER TABLE borders ADD COLUMN " +
                       "buffered_outline GEOGRAPHY")
        cursor.execute("CREATE INDEX buffered_border_index ON borders " +
                       "USING GIST(buffered_outline)")
    except psycopg2.ProgrammingError:
        connection.rollback()

    # Calculate the buffered outline.

    cursor.execute("UPDATE borders SET buffered_outline=ST_Buffer(outline, 1000)")

    connection.commit()

    # Finally, compare the area of each outling with its buffered equivalent.

    cursor.execute("SELECT name, ST_Area(outline), ST_Area(buffered_outline) " +
                   "FROM borders ORDER BY name")
    for name, area1, area2 in cursor:
        if not math.isnan(area1):
            area1 = int(area1/1000000)
        else:
            area1 = "n/a"
        if not math.isnan(area2):
            area2 = int(area2/1000000)
        else:
            area2 = "n/a"
        print name, area1, area2

#############################################################################

if __name__ == "__main__":
    main()

