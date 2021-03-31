import pytest
from libpyhat.pyhat_io.io_moon_mineralogy_mapper import M3
from libpyhat.examples import get_path
import numpy as np
from numpy.testing import assert_array_almost_equal

def test_m3_io():
    m = M3(get_path('M3_4030seg_L2_aristcrater.tif'))
    expected = np.array([[[0.05034748, 0.05205967], [0.0512817, 0.05294098]],
                [[0.05523797, 0.05685501], [0.05609552, 0.05767513]]])
    
    assert m.data.shape == (83, 50, 50)
    assert_array_almost_equal(m.data[0:2,0:2,0:2],expected)
