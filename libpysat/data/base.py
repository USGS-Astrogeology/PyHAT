import numpy as np
from pandas import Index, concat

from ..transform import smooth, continuum

import libpysat

def _spectral_unary_op(this, new, preserve_metadata=True):
    """
    Wrapper for funcs that should return a spectral type

    Parameters
    ----------
    this : obj
           The parent or source Spectra/Spectrum that is operated on

    new : obj
          The return from the operation. Should be an ndarray, series,
          or dataframe
    
    preserve_metadata : bool
                        Whether or not the metadata should be added to 
                        the returned object if any metadata is present
                        on the parent (this) object. Default: True
    """
    # Create the new class with the metadata obj, but the
    # data only index
    if isinstance(this, libpysat.Spectrum):
        new = libpysat.Spectrum(new, wavelengths=this.wavelengths,
                        metadata=None,
                        tolerance=this.tolerance,
                        index=this.data.index)
    else:
        new = libpysat.Spectra(new, wavelengths=this.wavelengths,
            metadata=None,
            tolerance=this.tolerance,
            index=this.data.index, 
            columns=this.data.columns)

    if preserve_metadata and this.metadata is not None:
        new = concat((new, this.metadata))
        new.metadata = this.metadata.index
    return new

class PySatBase(object):

    def continuum_correct(self, nodes=[], correction_nodes=[],
                         func=continuum.linear, 
                         preserve_metadata=True,
                         **kwargs):
        """
        Apply a continuum correction to all entries in the object.

        Parameters
        ----------
        nodes : list
                The nodes to use when applying the continuum correction as
                the endpoints (linear and non-linear) or the nodes to use as
                the domain (regression). Nodes are the label values in the
                wavelength attributes. When not specified the first and last
                wavelengths are utilized. For example, in the unspecified case
                and a linear correction wavelengths[0] (the first) and 
                wavelengths[-1] (the final) values are used as the endpoints. More
                than 2 nodes can be specified, resulting in a piecewise continuum. 
                For example, nodes=[500,1500,2000] will compute and apply 2 continuum,
                one in the {500,1500} domain and one in the {1500,2000} domain.

        correction_nodes : list
                           By default, the computed continuum is applied to the nodes
                           used in the computation. For example, if the continuum is
                           computed on the domain {700,1500}, the spectrum will be corrected
                           only on the domain {700,1500}. It is possible to pass correction
                           nodes that force the correction to a different domain. For example,
                           if nodes=[700,1500] and correction_nodes=[500,1500] then
                           continuum is computed on the domain {700,1500} but applied to
                           all observations in the domain {500,1500}
        func : object
               The continuum correction to apply. Default: linear

        preserve_metadata : bool
                            If True (the default) the object returned by this
                            function will maintain any metadata that existed on
                            the original object.  In other words, if a spectrum/spectra 
                            had metadata, the continuum corrected spectrum/spectra will
                            also have the same metadata.

        Returns
        -------
        res : object
              A Spectrum or Spectra object depending on the required dimensionality.

        denom : object
                A Spectrum object containing the continuum fit indexed identically
                to the res object.
        """
        if not nodes:
            nodes = [self.wavelengths[0], self.wavelengths[-1]]
        res, denom = continuum.continuum_correction(self.data.values,
                                                    self.wavelengths,
                                                    nodes=nodes,
                                                    correction_nodes=correction_nodes,
                                                    correction=func,
                                                    **kwargs)
        res = _spectral_unary_op(self, res, preserve_metadata=preserve_metadata)
        denom = _spectral_unary_op(self, denom, preserve_metadata=False)
        return res, denom


    def smooth(self, func=smooth.boxcar, preserve_metadata='True', **kwargs):
        res = func(self.data.values, **kwargs)
        return _spectral_unary_op(self, res, preserve_metadata=preserve_metadata)

    @property
    def metadata(self):
        if self._metadata_index is not None:
            return self.loc[self._metadata_index]

    @metadata.setter
    def metadata(self, val):
        if hasattr(val, '__iter__') and not isinstance(val, (str, bytes)):
            self._metadata_index = val

    @property
    def tolerance(self):
        if not hasattr(self, '_tolerance'):
            self._tolerance = 2
        return self._tolerance
    
    @tolerance.setter
    def tolerance(self, val):
        if isinstance(val, int):
            self._tolerance = val
            self._reindex()
        else:
            raise TypeError

    def _reindex(self):
        if self.wavelengths is not None:
            wv = Index(np.round(self.wavelengths, decimals=self.tolerance))
            if self._metadata_index is not None:
                index = wv.append(Index(self._metadata_index))
            else:
                index = wv
            try:
                # This could be cleaner because if the df is square this will fail.
                self.index = index
            except:
                self.columns = index
