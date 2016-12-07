import scipy.signal
from pysat.spectral.baseline_code.common import WhittakerSmoother, iterative_threshold, Baseline


def fabc_baseline(intensities, dilation_param=50, smoothness_param=1e3):
  '''Fully Automatic Baseline Correction, by Carlos Cobas (2006).
  http://www.sciencedirect.com/science/article/pii/S1090780706002266
  '''
  cwt = scipy.signal.cwt(intensities, scipy.signal.ricker, (dilation_param,))
  dY = cwt.ravel()**2

  is_baseline = iterative_threshold(dY)
  is_baseline[0] = True
  is_baseline[-1] = True

  smoother = WhittakerSmoother(intensities, smoothness_param, deriv_order=1)
  return smoother.smooth(is_baseline)


class FABC(Baseline):
  def __init__(self, dilation_param=50, smoothness_param=1e3):
    self.dilation_ = dilation_param
    self.smoothness_ = smoothness_param

  def _fit_one(self, bands, intensities):
    return fabc_baseline(intensities, self.dilation_, self.smoothness_)

  def param_ranges(self):
    return {
        'dilation_': (1, 100, 'integer'),
        'smoothness_': (1, 1e6, 'log')
    }
