""" create_table.py

    This program is intended to accompany chapter 3 of Python Geospatial
    Analysis.  It creates the database table used to store our spatial data.
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

    # Delete the existing table, if it exists.

    cursor.execute("DROP TABLE IF EXISTS borders")

    # Create our table.

    cursor.execute("CREATE TABLE borders (" +
                   "id SERIAL PRIMARY KEY," +
                   "name VARCHAR NOT NULL," +
                   "iso_code VARCHAR NOT NULL," +
                   "outline GEOGRAPHY)")

    cursor.execute("CREATE INDEX border_index ON borders USING GIST(outline)")

    connection.commit()

#############################################################################

if __name__ == "__main__":
    main()

