import pandas as pd
import random as rand

import numpy as np

from numbers import Real
from numbers import Number

from functools import reduce
from functools import singledispatch

from . import io
from libpysat.data import _index as _idx
from .spectrum import Spectrum
from ..transform import continuum
from ..utils import utils


class Spectra(pd.DataFrame):
    """
    A pandas derived DataFrame used to store spectral and hyper-spectral observations.

    attributes
    ----------

    wavelengths : pandas.Float64Index
                  The wavelengths store as a pandas index

    get : PandasLocIndexer
          Indexing object, maps wavelengths to indices enabling access a tolerance for
          floating point labels.

    ----------
    """

    # attributes that carry over on operations
    _metadata = ['_get', '_iget', 'wavelengths', 'metadata']


    def __init__(self, *args, wavelengths = [], metadata = [], tolerance=0, **kwargs):
        super(Spectra, self).__init__(*args, **kwargs)

        get_name = self.loc.name
        iget_name = self.iloc.name
        self._iget = _idx._SpectrumiLocIndexer(name=iget_name, obj=self)
        self._get = _idx._SpectrumLocIndexer(name=get_name, obj=self)

        self._get._tolerance = tolerance
        self.wavelengths = pd.Float64Index(wavelengths)

        if metadata:
            self.metadata = pd.Index(metadata)
        else:
            self.metadata = self.columns.difference(self.wavelengths)


    @property
    def _constructor_sliced(self):
        """
        Returns constructor used when dataframe dimension decreases (i.e. goes from a dataframe
        to a series).
        """
        return Spectrum


    @property
    def _constructor(self):
        """
        Returns constructor used when creating copies (i.e. when operations are run on the dataframe).
        """
        return Spectra


    def continuum_correction(self, nodes = None, correction_nodes=[], correction = continuum.linear, **kwargs):
        """
        apply linear correction to all spectra
        """
        if not nodes:
            nodes = [self.wavelengths[0], self.wavelengths[-1]]

        data = self.spectra.values
        corrected, line = continuum.continuum_correction(data, self.wavelengths.values ,nodes, correction_nodes, correction, axis=1, **kwargs)
        return Spectra(corrected, columns=self.spectra.columns, wavelengths=self.wavelengths, tolerance = self.tolerance)


    def __getitem__(self, key):
        """
        overrides ndarray's __getitem__ to use .get's floating point tolerance for
        floating point indexes.

        parameters
        ----------
        key : object
              the column labels to access on

        """
        if isinstance(self.index, pd.MultiIndex):
            return self.get[:,:,key]
        else:
             return self.get[:,key]


    @classmethod
    def from_spectral_profiler(cls, f, tolerance=1):
        """
        Generate DataFrame from spectral profiler data.

        parameters
        ----------
        f : str
            file path to spectral profiler file

        tolerance : Real
                    Tolerance for floating point index
        """
        return io.spectral_profiler(f, tolerance=tolerance)


    @property
    def get(self):
        return self._get


    @property
    def iget(self):
        return self._iget


    @property
    def meta(self):
        return self[self.metadata]


    @property
    def spectra(self):
        return self[self.wavelengths]


    def plot_spectra(self, *args, **kwargs):
        return self.T.plot(*args, **kwargs)


    @property
    def tolerance(self):
        if not hasattr(self._get, '_tolerance'):
            self._get._tolerance = .5
        return self._get._tolerance


    @tolerance.setter
    def tolerance(self, val):
        self._get._tolerance = val
