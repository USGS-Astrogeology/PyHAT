import numpy as np
from scipy.spatial import ConvexHull
from pysat.spectral.baseline_code.common import Baseline


def rubberband_baseline(bands, intensities, num_iters=8, num_ranges=64):
  '''Bruker OPUS method. If num_iters=0, uses basic method from OPUS.'''
  y = intensities.copy()
  for _ in range(num_iters):
    yrange = y.max() - y.min()
    x_center = (bands[-1] - bands[0]) / 2.
    tmp = (bands - x_center) ** 2
    y += yrange/10. * tmp / tmp[-1]
  baseline = _rubberband(bands, y, num_ranges)
  # undo the n steps of convex function addition
  baseline -= (y - intensities)
  return baseline


def _rubberband(bands, intensities, num_ranges):
  '''Basic rubberband method,
  from p.77 of "IR and Raman Spectroscopy" (OPUS manual)'''
  # create n ranges of equal size in the spectrum
  range_size = len(intensities) // num_ranges
  y = intensities[:range_size*num_ranges].reshape((num_ranges, range_size))
  # find the smallest intensity point in each range
  idx = np.arange(num_ranges) * range_size + np.argmin(y, axis=1)
  # add in the start and end points as well, to avoid weird edge effects
  if idx[0] != 0:
    idx = np.append(0, idx)
  if idx[-1] != len(intensities) - 1:
    idx = np.append(idx, len(intensities) - 1)
  baseline_pts = np.column_stack((bands[idx], intensities[idx]))
  # wrap a rubber band around the baseline points
  hull = ConvexHull(baseline_pts)
  hidx = idx[hull.vertices]
  # take only the bottom side of the hull
  left = np.argmin(bands[hidx])
  right = np.argmax(bands[hidx])
  mask = np.ones(len(hidx), dtype=bool)
  for i in range(len(hidx)):
    if i > right and (i < left or right > left):
      mask[i] = False
    elif i < left and i < right:
      mask[i] = False
  hidx = hidx[mask]
  hidx = hidx[np.argsort(bands[hidx])]
  # interpolate a baseline
  return np.interp(bands, bands[hidx], intensities[hidx])


class Rubberband(Baseline):
  def __init__(self, num_iters=8, num_ranges=64):
    self.num_iters_ = num_iters
    self.num_ranges_ = num_ranges

  def _fit_one(self, bands, intensities):
    return rubberband_baseline(bands, intensities, num_iters=self.num_iters_,
                               num_ranges=self.num_ranges_)

  def param_ranges(self):
    return {
        'num_ranges_': (1, 100, 'integer'),
        'num_iters_': (0, 36, 'integer')
    }
