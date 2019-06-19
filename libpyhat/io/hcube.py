import numpy as np
import gdal

from plio.utils.indexing import _LocIndexer, _iLocIndexer
from .. transform.continuum import continuum_correction
from .. transform.continuum import polynomial, linear, regression


class HCube(object):
    """
    A Mixin class for use with the io_gdal.GeoDataset class
    to optionally add support for spectral labels, label
    based indexing, and lazy loading for reads.
    """
    def __init__(self, data = [], wavelengths = []):
        if len(data) != 0:
            self._data = data
        if len(wavelengths) != 0:
            self._wavelengths = wavelengths

    @property
    def wavelengths(self):
        if not hasattr(self, '_wavelengths'):
            try:
                info = gdal.Info(self.file_name, format='json')
                wavelengths = [float(j) for i, j in sorted(info['metadata'][''].items(),
                                 key=lambda x: float(x[0].split('_')[-1]))]
                self._original_wavelengths = wavelengths
                self._wavelengths = np.round(wavelengths, self.tolerance)
            except:
                self._wavelengths = []
        return self._wavelengths

    @property
    def data(self):
        if not hasattr(self, '_data'):
            try:
                key = (slice(None, None, None),
                       slice(None, None, None),
                       slice(None, None, None))
                data = self._read(key)
            except Exception as e:
                print(e)
                data = []
            self._data = data

        return self._data

    @property
    def tolerance(self):
        return getattr(self, '_tolerance', 2)

    @tolerance.setter
    def tolerance(self, val):
        if isinstance(val, int):
            self._tolerance = val
            self._reindex()
        else:
            raise TypeError

    def _reindex(self):
        if self._original_wavelengths is not None:
            self._wavelengths = np.round(self._original_wavelengths, decimals=self.tolerance)

    def __getitem__(self, key):
        i = _iLocIndexer(self)
        return i[key]

    @property
    def loc(self):
        return _LocIndexer(self)

    @property
    def iloc(self):
        return _iLocIndexer(self)

    def reduce(self, how = np.mean, axis = (1, 2)):
        """
        Parameters
        ----------
        how : function
              Function to apply across along axises of the hcube

        axis : tuple
               List of axis to apply a given function along

        Returns
        -------
        new_hcube : Object
                    A new hcube object with the reduced data set
        """
        res = how(self.data, axis = axis)

        new_hcube = HCube(res, self.wavelengths)
        return new_hcube

    def continuum_correct(self, nodes, correction_nodes = np.array([]), correction = linear,
                          axis=0, adaptive=False, window=3, **kwargs):
        """
        Parameters
        ----------

        nodes : list
                A list of wavelengths for the continuum to be corrected along

        correction_nodes : list
                           A list of nodes to limit the correction between

        correction : function
                     Function specifying the type of correction to perform
                     along the continuum

        axis : int
               Axis to apply the continuum correction on

        adaptive : boolean
                   ?

        window : int
                 ?

        Returns
        -------

        new_hcube : Object
                    A new hcube object with the corrected dataset
        """

        continuum_data = continuum_correction(self.data, self.wavelengths, nodes = nodes,
                                              correction_nodes = correction_nodes, correction = correction,
                                              axis = axis, adaptive = adaptive,
                                              window = window, **kwargs)

        new_hcube = HCube(continuum_data[0], self.wavelengths)
        return new_hcube


    def clip_roi(self, x, y, band, tolerance=2):
        """
        Parameters
        ----------

        x : tuple
            Lower and upper bound along the x axis for clipping

        y : tuple
            Lower and upper bound along the y axis for clipping

        band : tuple
               Lower and upper band along the z axis for clipping

        tolerance : int
                    Tolerance given for trying to find wavelengths
                    between the upper and lower bound

        Returns
        -------

        new_hcube : Object
                    A new hcube object with the clipped dataset
        """
        wavelength_clip = []
        for wavelength in self.wavelengths:
            wavelength_upper = wavelength + tolerance
            wavelength_lower = wavelength - tolerance
            if wavelength_upper > band[0] and wavelength_lower < band[1]:
                wavelength_clip.append(wavelength)

        key = (wavelength_clip, slice(*x), slice(*y))
        data_clip = _LocIndexer(self)[key]

        new_hcube = HCube(np.copy(data_clip), np.array(wavelength_clip))
        return new_hcube

    def _read(self, key):
        ifnone = lambda a, b: b if a is None else a

        y = key[1]
        x = key[2]
        if isinstance(x, slice):
            xstart = ifnone(x.start,0)
            xstop = ifnone(x.stop,self.raster_size[0])
            xstep = xstop - xstart
        else:
            raise TypeError("Loc style access elements must be slices, e.g., [:] or [10:100]")
        if isinstance(y, slice):
            ystart = ifnone(y.start, 0)
            ystop = ifnone(y.stop, self.raster_size[1])
            ystep = ystop - ystart
        else:
            raise TypeError("Loc style access elements must be slices, e.g., [:] or [10:100]")

        pixels = (xstart, ystart, xstep, ystep)
        if isinstance(key[0], (int, np.integer)):
            return self.read_array(band=int(key[0]+1), pixels=pixels)

        elif isinstance(key[0], slice):
            # Given some slice iterate over the bands and get the bands and pixel space requested
            arrs = []
            for band in list(list(range(1, self.nbands + 1))[key[0]]):
                arrs.append(self.read_array(band, pixels = pixels))
            return np.stack(arrs)

        else:
            arrs = []
            for b in key[0]:
                arrs.append(self.read_array(band=int(b+1), pixels=pixels))
        return np.stack(arrs)
