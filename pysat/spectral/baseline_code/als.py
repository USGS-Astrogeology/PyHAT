import numpy as np
from pysat.spectral.baseline_code.common import WhittakerSmoother, Baseline


def als_baseline(intensities, asymmetry_param=0.05, smoothness_param=1e6,
                 max_iters=10, conv_thresh=1e-5, verbose=False):
  '''Perform asymmetric least squares baseline removal.
  * http://www.science.uva.nl/~hboelens/publications/draftpub/Eilers_2005.pdf

  smoothness_param: Relative importance of smoothness of the predicted response.
  asymmetry_param (p): if y > z, w = p, otherwise w = 1-p.
                       Setting p=1 is effectively a hinge loss.
  '''
  smoother = WhittakerSmoother(intensities, smoothness_param, deriv_order=2)
  # Rename p for concision.
  p = asymmetry_param
  # Initialize weights.
  w = np.ones(intensities.shape[0])
  for i in range(max_iters):
    z = smoother.smooth(w)
    mask = intensities > z
    new_w = p*mask + (1-p)*(~mask)
    conv = np.linalg.norm(new_w - w)
    if verbose:
      print(i+1), conv
    if conv < conv_thresh:
      break
    w = new_w
  else:
    print('ALS did not converge in %d iterations' % max_iters)
  return z


class ALS(Baseline):
  def __init__(self, asymmetry_param=0.05, smoothness_param=1e6, max_iters=10,
               conv_thresh=1e-5, verbose=False):
    self.asymmetry_ = asymmetry_param
    self.smoothness_ = smoothness_param
    self.max_iters_ = max_iters
    self.conv_thresh_ = conv_thresh
    self.verbose_ = verbose

  def _fit_one(self, bands, intensities):
    return als_baseline(intensities, self.asymmetry_, self.smoothness_,
                        self.max_iters_, self.conv_thresh_, self.verbose_)

  def param_ranges(self):
    return {
        'asymmetry_': (1e-3, 1e-1, 'log'),
        'smoothness_': (1e2, 1e8, 'log')
    }
