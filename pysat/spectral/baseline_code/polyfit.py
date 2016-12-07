import numpy as np
from pysat.spectral.baseline_code.common import Baseline


def polyfit_baseline(bands, intensities, poly_order=5, num_stdv=3.,
                     max_iter=200):
  '''Iteratively fits a polynomial, discarding far away points as peaks.
  Similar in spirit to ALS and related methods.
  Automated method for subtraction of fluorescence from biological Raman spectra
  Lieber & Mahadevan-Jansen 2003
  '''
  fit_pts = intensities.copy()
  # precalculate [x^p, x^p-1, ..., x^1, x^0]
  poly_terms = bands[:,None] ** np.arange(poly_order, -1, -1)
  for _ in range(max_iter):
    coefs = np.polyfit(bands, fit_pts.T, poly_order)
    baseline = poly_terms.dot(coefs).T
    diff = fit_pts - baseline
    thresh = diff.std(axis=-1) * num_stdv
    mask = diff > np.array(thresh, copy=False)[...,None]
    unfitted = np.count_nonzero(mask)
    if unfitted == 0:
      break
    fit_pts[mask] = baseline[mask]  # these points are peaks, discard
  else:
    print("Warning: polyfit_baseline didn't converge in %d iters" % max_iter)
  return baseline


class PolyFit(Baseline):
  def __init__(self, poly_order=5, num_stdv=3.):
    self.poly_order_ = poly_order
    self.stdv_ = num_stdv

  def _fit_many(self, bands, intensities):
    return polyfit_baseline(bands, intensities,
                            poly_order=self.poly_order_,
                            num_stdv=self.stdv_)

  def param_ranges(self):
    return {
        'poly_order_': (1, 12, 'integer'),
        'stdv_': (1, 5, 'linear')
    }
