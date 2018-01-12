import numpy as np
import pandas as pd

from functools import reduce
from functools import singledispatch

from numbers import Real

from plio.io import io_moon_minerology_mapper

from . import _index as _idx
from . import io

class HCube(np.ndarray):
    """
    A Numpy derived array used to store spectral and hyper-spectral images.

    attributes
    ----------

    wavelengths : pandas.Float64Index
                  The wavelengths store as a pandas index

    get : _ArrayLocIndexer
          Indexing object, maps wavelengths to indices allowing for access using
          band labels

    ----------
    """
    def __new__(cls, ndarray, wavelengths=[], waxis=None, tolerance=.5):
        obj = np.asarray(ndarray).view(cls)

        if isinstance(wavelengths, Real):
            obj.wavelengths = pd.Float64Index([wavelengths])
        else:
            obj.wavelengths = pd.Float64Index(wavelengths)

        obj._get = _idx._ArrayLocIndexer(obj=obj, waxis=waxis, tolerance=tolerance)
        return obj


    def __array_finalize__(self, obj):
        if obj is None:
            return obj

        self.wavelengths = getattr(obj, 'wavelengths', None)
        self.wavelengths = getattr(obj, '_get', None)

    def __getitem__(self, keys):
        """
        Override numpy's __getitem__ to crop axis labels if slicing accross the labeled axis (e.g
        the axis representing labels)

        parameters
        ----------
        keys : object
               a key or set of keys to access on

        returns
        -------
        : HCube
          copy of the subset of the array

        """
        # TODO: Make this less garbage 
        try:
            if hasattr(keys, '__iter__'):
                if self._get.waxis <= len(keys):
                    # wavelength is being sliced
                    wavelengths=self.wavelengths[keys[self._get.waxis]]
                    newarr = super(HCube, self).__getitem__(keys)
                    return HCube(newarr, wavelengths, self._get.waxis, self._get.tolerance)
                else:
                    newarr = super(HCube, self).__getitem__(keys)
                    if isinstance(keys, slice):
                        return HCube(newarr, self.wavelengths, self._get.waxis, self._get.tolerance)
                    else:
                        return HCube(newarr, [self.wavelengths], self._get.waxis, self._get.tolerance)
            else:
                if self._get.waxis == 0:
                    # wavelength is being sliced
                    wavelengths=self.wavelengths[keys]
                    newarr = super(HCube, self).__getitem__(keys)
                    return HCube(newarr, wavelengths, self._get.waxis, self._get.tolerance)
                else:
                    newarr = super(HCube, self).__getitem__(keys)
                    return HCube(newarr, self.wavelengths, self._get.waxis, self._get.tolerance)
        except Exception:
            return super(HCube, self).__getitem__(keys)

    @classmethod
    def from_m3(cls, f, tolerance=2, waxis=0):
        return io.m3(f, tolerance, waxis)


    @property
    def get(self):
        """
        Access the array using labeled indices.

        see also
        --------
        _SpectraDataFrame.get : label-wise access to a spectral dataframe
        _ArrayLocIndexer : Enable label-wise access to numpy arrays
        """
        return self._get


    @property
    def tolerance(self):
        if not hasattr(self._get, '_tolerance'):
            self._get._tolerance = .5
        return self._get._tolerance


    @tolerance.setter
    def tolerance(self, val):
        self._get._tolerance = val


    def band(self, n):
        return self.get[:,:,n]
