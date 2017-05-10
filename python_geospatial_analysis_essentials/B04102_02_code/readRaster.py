# Sample program to read raster-format data.

from osgeo import gdal

dem_file = gdal.Open("E10g")
num_bands = dem_file.RasterCount
band = dem_file.GetRasterBand(1)
data = band.ReadAsArray()

num_rows,num_cols = data.shape

histogram = {} # maps elevation to number of occurrences of that elevation.
no_data = int(band.GetNoDataValue())

for row in range(num_rows):
    for col in range(num_cols):
        elevation = int(data[row, col])
        if elevation == no_data: continue
        try:
            histogram[elevation] += 1
        except KeyError:
            histogram[elevation] = 1

for elevation in sorted(histogram.keys()):
    print elevation, histogram[elevation]

