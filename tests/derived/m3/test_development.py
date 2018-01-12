import pytest
import numpy as np

from libpysat.derived.m3 import development as dev
from libpysat import HCube

@pytest.fixture
def test_params(wavelengths):
    return (np.array(wavelengths), 1)

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([699, 929, 989, 1579])])

def test_bd1umratio(four_dim, wv_array, expected):
    data = HCube(four_dim, wv_array, waxis = 0)
    res = dev.bd1umratio(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([1348, 1408, 1428, 1448, 1578])])

def test_h2o2(five_dim, wv_array, expected):
    data = HCube(five_dim, wv_array, waxis = 0)
    res = dev.h2o2(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [(np.array([1428, 1448, 1488, 1508, 1528]), 0)])

def test_h2o3(five_dim, wv_array, expected):
    data = HCube(five_dim, wv_array, waxis = 0)
    res = dev.h2o3(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([2218, 2258, 2378, 2418, 2298, 2338])])

def test_h2o4(six_dim, wv_array, expected):
    data = data = HCube(six_dim, wv_array, waxis = 0)
    res = dev.h2o4(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([2578, 2618, 2658, 2698, 2738])])

def test_h2o5(five_dim, wv_array, expected):
    data = HCube(five_dim, wv_array, waxis = 0)
    res = dev.h2o5(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([2538, 2578, 2618, 2817, 2857, 2897])])

def test_ice(six_dim, wv_array, expected):
    data = HCube(six_dim, wv_array, waxis = 0)
    res = dev.ice(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([1578, 1898, 2298, 2578])])

def test_bd2umratio(four_dim, wv_array, expected):
    data = HCube(four_dim, wv_array, waxis = 0)
    res = dev.bd2umratio(data, wv_array)
    assert res.all() == expected
