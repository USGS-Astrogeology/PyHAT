import pandas as pd
import numpy as np

from plio.io import io_spectral_profiler

import libpysat


def spectral_profiler(f, **kwargs):
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
        meta.index.names = ['id']
        df = geo_data.spectra.transpose()
        df.index.names = ['id', 'minor']
        joined = df.join(meta, how='inner').transpose()

        return libpysat.Spectra(joined, wavelengths=geo_data.wavelengths,
                                        metadata=meta.columns,
                                        index=joined.index,
                                        columns=joined.columns,
                                        **kwargs)


DRIVERS = [spectral_profiler]

def read_file(filename, **kwargs):
    #try:
    for d in DRIVERS:
        return d(filename, **kwargs)
    #except:
    #    return