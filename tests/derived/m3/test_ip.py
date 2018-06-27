import pytest
import numpy as np

from libpysat.derived.m3 import ip

def test_lscc_maturity(m3_img):
    res = ip.lscc_maturity(m3_img)
    np.testing.assert_array_almost_equal(res, np.array(0.9988332397044207))
