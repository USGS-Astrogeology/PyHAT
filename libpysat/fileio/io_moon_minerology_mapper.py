import numpy as np
from osgeo import gdal


def openm3(input_data):
    if input_data.split('.')[-1] == 'hdr':
        # GDAL wants the img, but many users aim at the .hdr
        input_data = input_data.split('.')[0] + '.img'
    ds = gdal.Open(input_data)
    ref_array = ds.GetRasterBand(1).ReadAsArray()
    metadata = ds.GetMetadata()
    wv_array = metadatatoband(metadata)
    return wv_array, ref_array, ds


def metadatatoband(metadata):
    wv2band = []
    for k, v in metadata.iteritems():
        try:
            wv2band.append(float(value))
        except:
            v = v.split(" ")[-1].split("(")[1].split(")")[0]
            wv2band.append(float(v))
    wv2band.sort(key=int)
    return np.asarray(wv2band)
