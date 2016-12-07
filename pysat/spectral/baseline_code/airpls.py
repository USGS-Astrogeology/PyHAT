import numpy as np
from pysat.spectral.baseline_code.common import WhittakerSmoother, Baseline


def airpls_baseline(intensities, smoothness_param=100, max_iters=10,
                    conv_thresh=0.001, verbose=False):
  '''
  Baseline corr. using adaptive iteratively reweighted penalized least squares.
  Also known as airPLS, 2010.
  http://pubs.rsc.org/EN/content/articlehtml/2010/an/b922045c
  https://code.google.com/p/airpls/
  https://airpls.googlecode.com/svn/trunk/airPLS.py
  '''
  smoother = WhittakerSmoother(intensities, smoothness_param)
  total_intensity = np.abs(intensities).sum()
  w = np.ones(intensities.shape[0])
  for i in range(1, max_iters+1):
    baseline = smoother.smooth(w)
    # Compute error (sum of distances below the baseline).
    corrected = intensities - baseline
    mask = corrected < 0
    baseline_error = -corrected[mask]
    total_error = baseline_error.sum()
    # Check convergence as a fraction of total intensity.
    conv = total_error / total_intensity
    if verbose:
      print(i, conv)
    if conv < conv_thresh:
      break
    # Set peak weights to zero.
    w[~mask] = 0
    # Set baseline weights.
    baseline_error /= total_error
    w[mask] = np.exp(i*baseline_error)
    w[0] = np.exp(i*baseline_error.min())
    w[-1] = w[0]
  else:
    print('airPLS did not converge in %d iterations' % max_iters)
  return baseline


class AirPLS(Baseline):
  def __init__(self, smoothness_param=100, max_iters=10,
               conv_thresh=0.001, verbose=False):
    self.smoothness_ = smoothness_param
    self.max_iters_ = max_iters
    self.conv_thresh_ = conv_thresh
    self.verbose_ = verbose

  def _fit_one(self, bands, intensities):
    return airpls_baseline(intensities, self.smoothness_, self.max_iters_,
                           self.conv_thresh_, self.verbose_)

  def param_ranges(self):
    return {
        'smoothness_': (1, 1e4, 'log')
    }
