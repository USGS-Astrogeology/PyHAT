from scipy.signal import medfilt
from pysat.spectral.baseline_code.common import Baseline


def median_baseline(intensities, window_size=501):
  '''Perform median filtering baseline removal.
  Window should be wider than FWHM of the peaks.
  "A Model-free Algorithm for the Removal of Baseline Artifacts" Friedrichs 1995
  '''
  # Ensure the window size is odd
  if window_size % 2 == 0:
    window_size += 1
  # Enable batch mode
  if intensities.ndim == 2:
    window_size = (1, window_size)
  return medfilt(intensities, window_size)


class MedianFilter(Baseline):
  def __init__(self, window_size=501):
    self.window_ = window_size

  def _fit_many(self, bands, intensities):
    return median_baseline(intensities, window_size=self.window_)

  def param_ranges(self):
    return {'window_': (201, 901, 'integer')}
