from pandas import Series
import numpy as np

from ..transform import continuum
from . import spectra
from .base import PySatBase

from pandas import to_numeric, Index

    
class Spectrum(PySatBase, Series):
    """
    """
    _metadata = ['wavelengths','_metadata_index', '_tolerance']

    def __new__(cls, *args, **kwargs):
        kwargs.pop('wavelengths', None)
        kwargs.pop('metadata', None)
        kwargs.pop('tolerance', 2)

        arr = Series.__new__(cls)
        if type(arr) is Spectrum:
            return arr
        else:
            return arr.view(Spectrum)

    def __init__(self, *args, **kwargs):
        wavelengths = kwargs.pop('wavelengths', None)
        metadata_index = kwargs.pop('metadata', None)
        tolerance = kwargs.pop('tolerance', 2)
        super(Spectrum, self).__init__(*args, **kwargs)
        
        self.wavelengths = wavelengths
        self._metadata_index = metadata_index
        self.tolerance = tolerance

        self._reindex()

    @property
    def data(self):
        # Have to apply the tolerances when doing the positional lookup
        wv = Index(np.round(self.wavelengths, decimals=self.tolerance))
        return Spectrum(to_numeric(self.loc[wv]))

    @property
    def _constructor(self):
        return Spectrum

    def _wrapped_pandas_method(self, mtd, *args, **kwargs):
        """Wrap a generic pandas method to ensure it returns a GeoSeries"""
        val = getattr(super(Spectrum, self), mtd)(*args, **kwargs)
        if type(val) == Series:
            val.__class__ = Spectrum
            val.wavelengths = self.wavelengths
            val._metadata_index = self._metadata_index
            val._tolerance = self._tolerance
        return val

    def __getitem__(self, key):
        return self._wrapped_pandas_method('__getitem__', key)

    def sort_index(self, *args, **kwargs):
        return self._wrapped_pandas_method('sort_index', *args, **kwargs)

    def take(self, *args, **kwargs):
        return self._wrapped_pandas_method('take', *args, **kwargs)

    #def select(self, *args, **kwargs):
    #    return self._wrapped_pandas_method('select', *args, **kwargs)

    '''def continuum_correction(self, nodes = None, correction_nodes=[], correction = continuum.linear, **kwargs):
        """
        apply linear correction to spectrum
        """

        if nodes == None:
            nodes = [wavelengths[0], wavelengths[-1]]

        data, denom = continuum.continuum_correction(self.values, self.wavelengths.values, nodes=nodes,
                                    correction_nodes=correction_nodes, correction=correction, **kwargs)

        return Spectrum(data, index=self.wavelengths, wavelengths=self.wavelengths, tolerance = self.tolerance)
    '''