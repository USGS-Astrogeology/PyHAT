from plio.io import io_spectral_profiler

from libpyhat import Spectra

def open(f, **kwargs):
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

        return Spectra(joined, wavelengths=geo_data.wavelengths,
                                        metadata=meta.columns,
                                        index=joined.index,
                                        columns=joined.columns,
                                        **kwargs)

