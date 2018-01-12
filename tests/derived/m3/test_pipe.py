import pytest
import numpy as np

from libpysat.derived.m3 import pipe
from libpysat import HCube

@pytest.fixture
def test_params(wavelengths):
    return (np.array(wavelengths) , 1)

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([419, 619, 749])])

def test_bd620(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.bd620(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([1408, 1898, 2498])])

def test_bd1900(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.bd1900(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([1578, 2298, 2578])])

def test_bd2300(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.bd2300(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([1578, 2538, 2978])])

def test_h2o1(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.h2o1(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([1578])])

def test_iralbedo(one_dim, wv_array, expected):
    data = HCube(one_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.iralbedo(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([749, 950])])

def test_mafic_abs(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.mafic_abs(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([749, 889])])

def test_omh(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.omh(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([650, 860, 1047, 1230, 1750])])

def test_olindex(five_dim, wv_array, expected):
    data = HCube(five_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.olindex(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([699, 1579])])

def test_oneum_slope(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.oneum_slope(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([540])])

def test_reflectance1(one_dim, wv_array, expected):
    data = HCube(one_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.reflectance1(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([749])])

def test_reflectance2(one_dim, wv_array, expected):
    data = HCube(one_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.reflectance2(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([2778])])

def test_reflectance3(one_dim, wv_array, expected):
    data = HCube(one_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.reflectance3(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([1578])])

def test_reflectance4(one_dim, wv_array, expected):
    data = HCube(one_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.reflectance4(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([2538, 2978])])

def test_thermal_ratio(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.thermal_ratio(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([2538, 2978])])

def test_thermal_slope(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.thermal_slope(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([1578, 2538])])

def test_twoum_ratio(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.twoum_ratio(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([1578, 2538])])

def test_twoum_slope(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.twoum_slope(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([419, 749])])

def test_uvvis(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.uvvis(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([419, 749])])

def test_visslope(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.visslope(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([419, 749])])

def test_visuv(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.visuv(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([699, 1579])])

def test_visnir(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.visnir(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([789 + 20*i for i in range(0, 30)])])

def test_bdi1000(thirty_dim, wv_array, expected):
    print(wv_array)
    data = HCube(thirty_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.bdi1000(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([1658 + 40*i for i in range(0, 25)])])

def test_bdi2000(twenty_five_dim, wv_array, expected):
    print(wv_array)
    data = HCube(twenty_five_dim, wv_array, waxis = 0, tolerance = 2)
    res = pipe.bdi2000(data, wv_array)
    assert res.all() == expected
