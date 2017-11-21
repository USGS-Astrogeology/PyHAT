from pandas import Series

import libpysat.spectral.analytics as analytics
from libpysat.spectral.continuum import continuum_correct
from libpysat.spectral.smoothing import boxcar, gaussian


def tospectra(func):  # pragma: no cover
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return Spectra(result)

    return wrapper


def tospectrum(func):  # pragma: no cover
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return Spectrum(result)

    return wrapper


class Spectrum(object):
    def __init__(self, series):
        self.series = series

    def __repr__(self):
        return self.series.__repr__()

    def __getattr__(self, attr):
        result = getattr(self.series, attr)
        if callable(result):
            result = tospectrum(result)
        return result

    def __getitem__(self, key):
        try:
            result = self.series.loc[key]
        except:
            result = self.series.iloc[key]
        return result

    def boxcar_smooth(self, *args, **kwargs):
        return Spectrum(boxcar(self.series, *args, **kwargs))

    def gaussian_smooth(self, *args, **kwargs):
        return Spectrum(gaussian(self.series, *args, **kwargs))

    def continuum_correct(self, *args, **kwargs):
        corrected, continuum = continuum_correct(self.series, *args, **kwargs)
        return Spectrum(corrected), Spectrum(continuum)

    def band_minima(self, *args, **kwargs):
        minidx, minvalue = analytics.band_minima(self, *args, **kwargs)
        return minidx, minvalue

    def band_center(self, *args, **kwargs):
        return analytics.band_center(self, *args, **kwargs)

    def band_area(self, *args, **kwargs):
        return analytics.band_area(self, *args, **kwargs)


class Spectra(object):
    def __init__(self, df=None):
        self.df = df

    def __getitem__(self, key):
        result = self.df[key]
        if isinstance(result, type(self.df)):
            result = Spectra(result)
        elif isinstance(result, Series):
            return Spectrum(result)
        return result

    def __getattr__(self, attr):
        result = getattr(self.df, attr)
        if callable(result):
            result = tospectra(result)
        return result

    def __repr__(self):
        return repr(self.df)
