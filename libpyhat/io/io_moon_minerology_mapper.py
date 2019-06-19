import os
import numpy as np
from plio.io.io_gdal import GeoDataset

from . hcube import HCube
from .. derived import m3
from .. derived.utils import get_derived_funcs

import gdal


class M3(GeoDataset, HCube):
    """
    An M3 specific reader with the spectral mixin.
    """
    def __init__(self, file_name):

        GeoDataset.__init__(self, file_name)
        HCube.__init__(self)

        self.derived_funcs = {}

        if libpyhat_enabled:
            self.derived_funcs = get_derived_funcs(m3)

    def __getattr__(self, name):
        try:
            func = self.derived_funcs[name]

            setattr(self, name, func.__get__(self))
            return getattr(self, name)

        except KeyError as keyerr:
            raise AttributeError("'M3' object has no attribute '{}'".format(name)) from None

    @property
    def wavelengths(self):
        if not hasattr(self, '_wavelengths'):
            try:
                info = gdal.Info(self.file_name, format='json')
                if 'Resize' in info['metadata']['']['Band_1']:
                    wavelengths = [float(j.split(' ')[-1].replace('(','').replace(')', '')) for\
                                  i,j in sorted(info['metadata'][''].items(),
                                  key=lambda x: float(x[0].split('_')[-1]))]
                    # This is a geotiff translated from the PDS IMG
                else:
                    # This is a PDS IMG
                    wavelengths = [float(j) for i, j in sorted(info['metadata'][''].items(),
                                    key=lambda x: float(x[0].split('_')[-1]))]
                self._original_wavelengths = wavelengths
                self._wavelengths = np.round(wavelengths, self.tolerance)
            except:
                self._wavelengths = []
        return self._wavelengths

def open(input_data):
    if os.path.splitext(input_data)[-1] == 'hdr':
        # GDAL wants the img, but many users aim at the .hdr
        input_data = os.path.splitext(input_data)[:-1] + '.img'
    ds = M3(input_data)

    return ds
