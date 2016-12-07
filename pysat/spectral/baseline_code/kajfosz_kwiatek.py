import numpy as np
from pysat.spectral.baseline_code.common import Baseline


def kajfosz_kwiatek_baseline(bands, intensities, top_width=0,
                             bottom_width=50, exponent=2,
                             tangent=False):
  """
  This function uses an enhanced version of the algorithm published by
  Kajfosz, J. and Kwiatek, W.M. (1987)  "Non-polynomial approximation of
  background in x-ray spectra." Nucl. Instrum. Methods B22, 78-81.

  top_width:
    Specifies the width of the polynomials which are concave upward.
    The top_width is the full width in energy units at which the
    magnitude of the polynomial is 0.1 of max. The default is 0, which
    means that concave upward polynomials are not used.

  bottom_width:
    Specifies the width of the polynomials which are concave downward.
    The bottom_width is the full width in energy units at which the
    magnitude of the polynomial is 0.1 of max. The default is 50.

  exponent:
    Specifies the power of polynomial which is used. The power must be
    an integer. The default is 2, i.e. parabolas. Higher exponents,
    for example EXPONENT=4, results in polynomials with flatter tops
    and steeper sides, which can better fit spectra with steeply
    sloping backgrounds.

  tangent:
    Specifies that the polynomials are to be tangent to the slope of the
    spectrum. The default is vertical polynomials. This option works
    best on steeply sloping spectra. It has trouble in spectra with
    big peaks because the polynomials are very tilted up inside the
    peaks.

  For more info, see:
  cars9.uchicago.edu/software/idl/mca_utility_routines.html#FIT_BACKGROUND
  """
  REFERENCE_AMPL = 0.1
  MAX_TANGENT = 2

  nchans = len(intensities)
  # Normalize intensities for widths to make sense.
  scale_factor = intensities.max()
  scratch = intensities / scale_factor
  slope = abs(np.diff(bands).mean())

  # Fit functions which come down from top
  if top_width > 0:
    power_funct, max_index = _kk_lookup_table(
        scratch, top_width, exponent, slope, REFERENCE_AMPL)

    bckgnd = scratch.copy()
    for center_chan in range(nchans):
      first_chan = max((center_chan - max_index), 0)
      last_chan = min(center_chan + max_index + 1, nchans)
      f = first_chan - center_chan + max_index
      l = last_chan - center_chan + max_index
      lin_offset = scratch[center_chan]
      new_bckgnd = power_funct[f:l] + lin_offset
      old_bckgnd = bckgnd[first_chan:last_chan]
      np.copyto(old_bckgnd, new_bckgnd, where=(new_bckgnd > old_bckgnd))

    # Copy this approximation of background to scratch
    scratch = bckgnd.copy()
  else:
    bckgnd = np.empty_like(scratch)

  # Fit functions which come up from below
  power_funct, max_index = _kk_lookup_table(
      scratch, bottom_width, exponent, slope, REFERENCE_AMPL)

  bckgnd.fill(-np.inf)
  for center_chan in range(nchans - 1):
    if tangent:
       # Find slope of tangent to spectrum at this channel
       first_chan = max(center_chan - MAX_TANGENT, 0)
       last_chan = min(center_chan + MAX_TANGENT + 1, nchans)
       denom = center_chan - np.arange(last_chan - first_chan)
       tangent_slope = (scratch[center_chan] -
                        scratch[first_chan:last_chan]) / np.maximum(denom,1)
       tangent_slope = np.sum(tangent_slope) / (last_chan - first_chan)

    first_chan = max(center_chan - max_index, 0)
    last_chan = min(center_chan + max_index + 1, nchans)
    lin_offset = scratch[center_chan]
    if tangent:
      nc = last_chan - first_chan
      lin_offset += (np.arange(nc) - nc / 2.) * tangent_slope

    # Find the maximum height of a function centered on this channel
    # such that it is never higher than the counts in any channel
    f = first_chan - center_chan + max_index
    l = last_chan - center_chan + max_index
    pf = power_funct[f:l] - lin_offset
    height = (scratch[first_chan:last_chan] + pf).min()

    # We now have the function height. Set the background to the
    # height of the maximum function amplitude at each channel
    new_bckgnd = height - pf
    old_bckgnd = bckgnd[first_chan:last_chan]
    np.copyto(old_bckgnd, new_bckgnd, where=(new_bckgnd > old_bckgnd))

  return bckgnd * scale_factor


def _kk_lookup_table(spectrum, width, exponent, slope, ref_ampl):
  nchans = len(spectrum)
  if width == 0:
    denom = 1e-20
  else:
    chan_width = width / (2. * slope)
    denom = chan_width ** exponent
  indices = np.arange(-nchans, nchans+1)
  power_funct = indices ** exponent * (ref_ampl / denom)
  power_funct = power_funct[power_funct <= 1]
  max_index = len(power_funct) // 2 - 1
  return power_funct, max_index


class KajfoszKwiatek(Baseline):
  def __init__(self, top_width=0, bottom_width=50, exponent=2, tangent=False):
    self.top_width_ = top_width
    self.bottom_width_ = bottom_width
    self.exponent_ = exponent
    self.tangent_ = tangent

  def _fit_one(self, bands, intensities):
    return kajfosz_kwiatek_baseline(bands, intensities, self.top_width_,
                                    self.bottom_width_, self.exponent_,
                                    self.tangent_)

  def param_ranges(self):
    return {
        'top_width_': (0, 100, 'integer'),
        'bottom_width_': (0, 100, 'integer')
    }
