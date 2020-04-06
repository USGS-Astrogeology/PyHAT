from libpyhat.transform.baseline_code import rubberband
import numpy as np

# First 10 values of a PyHAT File
bands = np.array([585.149, 585.374, 585.599, 585.824, 586.049, 586.273, 586.498, 586.723, 586.948, 587.173])
intensities = np.array([823.06, 774.06, 828.06, 828.06, 866.06, 939.06, 1016.06, 1057.06, 940.06,  938.06])
RB = rubberband.Rubberband(num_iters=1, num_ranges=4)
baseline = RB._fit_one(bands, intensities)
pass

def test_one_iter():
    RB = rubberband.Rubberband(num_iters=1, num_ranges=4)
    baseline = RB._fit_one(bands, intensities)
    expected = np.array([823.06, 774.06, 802.45891216, 828.06, 853.39526708, 875.83873318, 895.59078638, 912.54501525, 926.70141979, 938.06])
    np.testing.assert_array_almost_equal(baseline, expected, decimal=4)

def test_zero_iter():
    RB = rubberband.Rubberband(num_iters=0, num_ranges=4)
    baseline = RB._fit_one(bands, intensities)
    expected = np.array([823.06, 774.06, 794.5714, 815.0828, 835.5942, 856.0144, 876.5258, 897.0372, 917.5486, 938.06])
    np.testing.assert_array_almost_equal(baseline, expected, decimal=4)

def test_param_ranges():
    RB = rubberband.Rubberband(num_iters=0, num_ranges=4)
    params = RB.param_ranges()
    expected = {'num_ranges_': (1, 100, 'integer'), 'num_iters_': (0, 36, 'integer')}
    assert params == expected
