import pandas as pd
import numpy as np

from plio.io import io_spectral_profiler, io_moon_minerology_mapper

from . import hcube as hc
from . import spectra as sp


def spectral_profiler(f, tolerance=1):
        """
        Generate DataFrame from spectral profiler data.

        parameters
        ----------
        f : str
            file path to spectral profiler file

        tolerance : Real
                    Tolerance for floating point index
        """
        geo_data = io_spectral_profiler.Spectral_Profiler(f)
        meta = geo_data.ancillary_data

        df = geo_data.spectra.to_frame().unstack(level=1)
        df = df.transpose()
        df = df.swaplevel(0,1)

        df.index.names = ['minor', 'id']
        meta.index.name = 'id'

        wavelengths = df.columns

        df = df.reset_index().merge(meta.reset_index(), on='id')
        df = df.set_index(['minor', 'id'], drop=True)

        return sp.Spectra(df, wavelengths=wavelengths, tolerance=tolerance)


def m3(f, tolerance = 2, waxis = 0):
    """
    Generate DataFrame from spectral profiler data.
    parameters
    ----------
    f : str
        file path to spectral profiler file
    tolerance : Real
                Tolerance for floating point index
    """

    wavelengths, _, ds = io_moon_minerology_mapper.openm3(f)
    m3_array = ds.ReadAsArray()

    return hc.HCube(m3_array, wavelengths, waxis = waxis, tolerance=tolerance)
