from pandas import DataFrame, Series, to_numeric
import numpy as np

from .base import PyHatBase
from .spectrum import Spectrum

import libpyhat

class Spectra(PyHatBase, DataFrame):
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
    _metadata = ['wavelengths', '_metadata_index', '_tolerance']

    def __init__(self, *args, **kwargs):
        wavelengths = kwargs.pop('wavelengths', None)
        metadata_index = kwargs.pop('metadata', None)
        tolerance = kwargs.pop('tolerance', 2)
        super(Spectra, self).__init__(*args, **kwargs)

        self.wavelengths = wavelengths
        self._metadata_index = metadata_index
        self.tolerance = tolerance

    @property
    def data(self):
        # Trying to support indices as either index or column
        wv = np.round(self.wavelengths, self.tolerance)
        try:
            return self[wv].astype(np.float)
        except:
            return self.loc[wv].astype(np.float)

    @property
    def _constructor_sliced(self):
        """
        Returns constructor used when dataframe dimension decreases (i.e. goes from a dataframe
        to a series).
        """
        return Spectrum

    @property
    def _constructor(self):
        return Spectra

    def __finalize__(self, other, method=None, **kwargs):
        """propagate metadata from other to self """
        # merge operation: using metadata of the left object
        if method == 'merge':
            for name in self._metadata:
                object.__setattr__(self, name, getattr(other.left, name, None))
        # concat operation: using metadata of the first object
        elif method == 'concat':
            for name in self._metadata:
                object.__setattr__(self, name, getattr(other.objs[0], name, None))
        else:
            for name in self._metadata:
                object.__setattr__(self, name, getattr(other, name, None))
        return self

    def __getitem__(self, key):
        """
        overrides ndarray's __getitem__ to use .get's floating point tolerance for
        floating point indexes.

        parameters
        ----------
        key : object
              the column labels to access on

        """
        result = super(Spectra, self).__getitem__(key)
        if isinstance(result, Series):
            result.__class__ = Spectrum
            result.wavelengths = self.wavelengths
            result._metadata_index = self._metadata_index
            # Tolerance has to be set last because a change in tolerance updates
            # the existing indices
            result.tolerance = self.tolerance
            self._reindex()
        elif isinstance(result, DataFrame):
            result.__class__ = Spectra
            result.wavelengths = self.wavelengths
            result.tolerance = self.tolerance
            result._metadata_index = self._metadata_index
            self._reindex()
        return result

