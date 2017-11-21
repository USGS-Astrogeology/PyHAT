import numpy as np
from scipy.linalg import solveh_banded


class Baseline(object):
    def _fit_one(self, bands, intensities):
        '''bands: array of length n
           intensities: array of length n
           Returns baseline array of length n
        '''
        raise NotImplementedError()

    def _fit_many(self, bands, intensities):
        '''bands: array of length n
           intensities: 2d array of shape (k, n)
           Returns baseline array of shape (k, n)
        '''
        # Fallback implementation based on _fit_one()
        if intensities.ndim == 1:
            return self._fit_one(bands, intensities)
        baseline = np.zeros_like(intensities)
        for i, y in enumerate(intensities):
            baseline[i] = self._fit_one(bands, y)
        return baseline

    def param_ranges(self):
        '''Returns a dict of parameter -> (min,max,scale) mappings.
        Min and max are scalars, scale is one of {'linear','log','integer'}.'''
        raise NotImplementedError()

    def fit(self, bands, intensities, segment=False):
        '''Fits one baseline per spectrum and stores them as self.baseline.
        When segment=True, automatically detects discontinuities in the bands
        and fits a separate baseline per segment.'''
        if segment:
            segments = _segment(bands, intensities)
            self.baseline = np.hstack([self._fit_many(*s) for s in segments])
        else:
            self.baseline = self._fit_many(bands, intensities)
        return self

    def fit_transform(self, bands, intensities, segment=False):
        self.fit(bands, intensities, segment=segment)
        return intensities - self.baseline


def _segment(x, y):
    '''Splits y into segments based on sharp jumps in x.
    Returns an iterable of chunks of (x,y)'''
    d = np.diff(x)
    q1, q3 = np.percentile(d, (25, 75))
    # Borrowed from matplotlib's boxplot outlier detection.
    cutoff = q3 + 1.5 * (q3 - q1)
    inds, = np.where(d > cutoff)
    # Gross iteration over slices into x and y
    i = 0
    for j in inds:
        s = slice(i, j + 1)
        yield x[s], y[..., s]
        i = j + 1
    yield x[i:], y[..., i:]


def iterative_threshold(signal, num_stds=3):
    thresh = signal.mean(axis=-1) + num_stds * signal.std(axis=-1)
    old_mask = np.zeros_like(signal, dtype=bool)
    mask = signal >= np.array(thresh, copy=False)[..., None]
    while (mask != old_mask).any():
        below = np.ma.array(signal, mask=mask)
        thresh = below.mean(axis=-1) + num_stds * below.std(axis=-1)
        old_mask = mask
        mask = signal >= np.array(thresh, copy=False)[..., None]
    return ~mask


class WhittakerSmoother(object):
    def __init__(self, signal, smoothness_param, deriv_order=1):
        self.y = signal
        assert deriv_order > 0, 'deriv_order must be an int > 0'
        # Compute the fixed derivative of identity (D).
        d = np.zeros(deriv_order * 2 + 1, dtype=int)
        d[deriv_order] = 1
        d = np.diff(d, n=deriv_order)
        n = self.y.shape[0]
        k = len(d)
        s = float(smoothness_param)

        # Here be dragons: essentially we're faking a big banded matrix D,
        # doing s * D.T.dot(D) with it, then taking the upper triangular bands.
        diag_sums = np.vstack([
            np.pad(s * np.cumsum(d[-i:] * d[:i]), ((k - i, 0),), 'constant')
            for i in range(1, k + 1)])
        upper_bands = np.tile(diag_sums[:, -1:], n)
        upper_bands[:, :k] = diag_sums
        for i, ds in enumerate(diag_sums):
            upper_bands[i, -i - 1:] = ds[::-1][:i + 1]
        self.upper_bands = upper_bands

    def smooth(self, w):
        foo = self.upper_bands.copy()
        foo[-1] += w  # last row is the diagonal
        return solveh_banded(foo, w * self.y, overwrite_ab=True, overwrite_b=True)
