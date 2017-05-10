# Sample program to write raster-format data.

import random
import numpy

from osgeo import gdal
from osgeo import osr

driver = gdal.GetDriverByName("EHdr")
dstFile = driver.Create("Example Raster", 180, 360, 1, gdal.GDT_Int16)

spatialReference = osr.SpatialReference()
spatialReference.SetWellKnownGeogCS("WGS84")

dstFile.SetProjection(spatialReference.ExportToWkt())

originX    = -180
originY    = 90
cellWidth  = 0.25
cellHeight = 0.25

geoTransform = [originX, cellWidth, 0, originY, 0, -cellHeight]

dstFile.SetGeoTransform(geoTransform)

band = dstFile.GetRasterBand(1)

data = []
for row in range(360):
    row_data = []
    for col in range(180):
        row_data.append(random.randint(1, 100))
    data.append(row_data)

array = numpy.array(data, dtype=numpy.int16)

band.WriteArray(array)
band.SetNoDataValue(-500)

del dstFile

