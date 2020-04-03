from libpyhat.transform.baseline_code import rubberband
import numpy as np

# First 10 values of a PyHAT File
bands = np.array([585.149, 585.374, 585.599, 585.824, 586.049, 586.273, 586.498, 586.723, 586.948, 587.173])
intensities = np.array([76.9, 54.54, 55.03, 41.79, 50, 54.36, 50.75, 74.18, 67.5, 36.96])

def test_one_iter():
    RB = rubberband.Rubberband(num_iters=1, num_ranges=4)
    baseline = RB._fit_one(bands, intensities)
    expected = [76.9, 54.54, 48.36242951, 41.79, 41.97067336, 41.75831319, 41.15102343, 40.14887464, 38.75186683, 36.96]
    np.testing.assert_array_almost_equal(baseline, expected)

def test_zero_iter():
    RB = rubberband.Rubberband(num_iters=0, num_ranges=4)
    baseline = RB._fit_one(bands, intensities)
    expected = [76.9, 54.54, 48.165, 41.79, 40.98440326, 40.18238695, 39.37679021, 38.57119348, 37.76559674, 36.96]
    np.testing.assert_array_almost_equal(baseline, expected)

def test_param_ranges():
    RB = rubberband.Rubberband(num_iters=0, num_ranges=4)
    params = RB.param_ranges()
    expected = {'num_ranges_': (1, 100, 'integer'), 'num_iters_': (0, 36, 'integer')}
    assert params == expected
