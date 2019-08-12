from libpyhat.transform import stretch
import numpy as np

def one_dim():
    return np.repeat(np.arange(1, 1 + 2), (25)).reshape(1,-1,5)


def test_linear_stretch(expected = 1):
    res = stretch.linear_stretch(one_dim())
    assert res.all() == expected

def test_standard_deviation_stretch(expected = 1):
    res = stretch.standard_deviation_stretch(one_dim())
    assert res.all() == expected

def test_inverse_stretch(expected = 0):
    res = stretch.inverse_stretch(one_dim())
    assert res.all() == expected

def test_histequ_stretch(expected = 1):
    res = stretch.histequ_stretch(one_dim())
    assert res.all() == expected
