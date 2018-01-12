import pytest
import numpy as np

from libpysat.derived.m3 import supplemental as sup
from libpysat import HCube

@pytest.fixture
def test_params(wavelengths):
    return (np.array(wavelengths), 1)

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([749, 909, 1109])])

def test_curvature(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    res = sup.curvature(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([749, 949])])

def test_fe_est(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0)
    res = sup.fe_est(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([749, 949])])

def test_fe_mare_est(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0)
    res = sup.fe_mare_est(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([749, 949])])

def test_luceyc_amat(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0)
    res = sup.luceyc_amat(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([749, 949])])

def test_luceyc_omat(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0)
    res = sup.luceyc_omat(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([749, 949])])

def test_mare_omat(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0)
    res = sup.mare_omat(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([930, 1009])])

def test_tilt(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0)
    res = sup.tilt(data, wv_array)
    assert res.all() == expected
