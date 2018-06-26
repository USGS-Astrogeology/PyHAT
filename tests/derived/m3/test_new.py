import pytest
import numpy as np

from libpysat.derived.m3 import new

def test_mustard(m3_img):
    res = new.mustard(m3_img)

    np.testing.assert_array_almost_equal(res,
                                         np.array([[[-0.358333, -0.325318, -0.297874],
                                                    [-0.2747  , -0.254872, -0.237713],
                                                    [-0.222719, -0.209504, -0.19777 ]],
                                                    [[-0.026842, -0.024199, -0.022029],
                                                    [-0.020215, -0.018677, -0.017356],
                                                    [-0.016209, -0.015204, -0.014316]],
                                                    [[1, 2, 3],
                                                    [4, 5, 6],
                                                    [7, 8, 9]]]))
