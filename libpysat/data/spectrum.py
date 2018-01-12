import pandas as pd

import numpy as np

from ..transform import continuum
from . import _index as _idx
from . import spectra

class Spectrum(pd.Series):
    """
    """
    _metadata = ['_loc', 'wavelengths', 'metadata', 'tolerance']

    def __init__(self, *args, wavelengths=[], metadata=[], tolerance=.5, **kwargs):
        super(Spectrum, self).__init__(*args, **kwargs)

        self._get = _idx._SpectrumLocIndexer(name='loc', obj=self)
        self._get._tolerance = tolerance

        self.wavelengths = wavelengths
        self.metadata = metadata

    @property
    def _constructor(self):
        return Spectrum

    def continuum_correction(self, nodes = None, correction_nodes=[], correction = continuum.linear, **kwargs):
        """
        apply linear correction to spectrum
        """

        if nodes == None:
            nodes = [wavelengths[0], wavelengths[-1]]

        data, denom = continuum.continuum_correction(self.values, self.wavelengths.values, nodes=nodes,
                                    correction_nodes=correction_nodes, correction=correction, **kwargs)

        return Spectrum(data, index=self.wavelengths, wavelengths=self.wavelengths, tolerance = self.tolerance)


    @property
    def _constructor_expanddim(self):
        return spectra.Spectra


    @property
    def tolerance(self):
        if not hasattr(self._get, '_tolerance'):
            self._get._tolerance = .5
        return self._get._tolerance


    @tolerance.setter
    def tolerance(self, val):
        self._get._tolerance = val


    @property
    def get(self):
        return self._get
