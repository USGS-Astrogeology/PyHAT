import pytest
import numpy as np

from libpysat.derived.m3 import new

def test_mustard(m3_img):
    res = new.mustard(m3_img)

    np.testing.assert_array_almost_equal(res,
                                         np.array([[[-26.35833306, -26.32531836, -26.29787406],
                                                    [-26.27470005, -26.25487157, -26.23771294],
                                                    [-26.22271892, -26.20950421, -26.19776983]],
                                                    [[-21.02684206, -21.02419945, -21.02202926],
                                                    [-21.02021543, -21.01867701, -21.01735578],
                                                    [-21.01620885, -21.0152039,  -21.01431614]],
                                                    [[1, 2, 3],
                                                    [4, 5, 6],
                                                    [7, 8, 9]]]))

