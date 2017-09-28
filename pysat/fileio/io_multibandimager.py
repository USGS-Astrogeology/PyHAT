import numpy as np
from osgeo import gdal


def openmi(input_data):
    ds = gdal.Open(input_data)
    band_pointers = []
    nbands = ds.RasterCount

    for b in xrange(1, nbands + 1):
        band_pointers.append(ds.GetRasterBand(b))

    ref_array = ds.GetRasterBand(1).ReadAsArray()
    wv_array = None
    return wv_array, ref_array[::3, ::3], ds


def getspectra(x, y, ds):
    nbands = ds.RasterCount
    reflectance = np.empty(nbands)
    for b in range(1, nbands + 1):
        reflectance[b - 1] = ds.GetRasterBand(b).ReadAsArray(y, x, 1, 1)

    mergedref = np.empty(nbands - 1)
    mergedref[:4] = reflectance[:4]
    mergedref[4] = (reflectance[4] + reflectance[5]) / 2
    mergedref[5:] = reflectance[6:]
    return mergedref
