try:
    import pywt
except ImportError:
    import warnings

    warnings.warn('Failed to import pywavelets(pywt). wavelet_baseline will fail')
from libpysat.spectral.baseline_code.common import Baseline


def wavelet_baseline(intensities, filter_len=4, level=9):
    '''Perform wavelet baseline correction.
    "Automatic Baseline Correction by Wavelet Transform for Quantitative
     Open-Path Fourier Transform Infrared Spectroscopy", Shao & Griffiths 2007
    http://staff.ustc.edu.cn/~lshao/papers/paper03.pdf

    filter_len : length of the Daubechies wavelet. Must be an even number.
    level : number of wavelet decompositions to perform.
    '''
    mode = 'cpd'  # constant padding
    w = pywt.Wavelet('db%d' % (filter_len // 2))
    max_level = pywt.dwt_max_level(len(intensities), w.dec_len)
    res = pywt.wavedec(intensities, w, mode, level=min(level, max_level))
    res[0][:] = 0  # zero out approximation, keep details
    bc = pywt.waverec(res, w, mode)
    bc = bc[:len(intensities)]  # accounts for off-by-one issues in waverec
    baseline = intensities - bc  # hack, to make int - bl = bc
    return baseline


class Wavelet(Baseline):
    def __init__(self, filter_len=4, level=9):
        self.filter_len_ = filter_len
        self.level_ = level

    def _fit_one(self, bands, intensities):
        return wavelet_baseline(intensities, filter_len=self.filter_len_,
                                level=self.level_)

    def param_ranges(self):
        return {
            'filter_len_': (2, 40, 'integer'),
            'level_': (5, 24, 'integer')
        }
