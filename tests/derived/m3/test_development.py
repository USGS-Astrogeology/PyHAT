import pytest
import numpy as np

from libpysat.derived.m3 import development as dev


def test_bd1umratio(m3_img):
    res = dev.bd1umratio(m3_img)
    print(res)
    np.testing.assert_array_almost_equal(res, np.array([[0.26226209, 0.25687621, 0.25256142],
                                                        [0.2490271, 0.24607906, 0.2435826],
                                                        [0.24144133, 0.23958448, 0.23795892]]))


def test_h2o2(m3_img):
    res = dev.h2o2(m3_img)
    print(res)
    np.testing.assert_array_almost_equal(res, np.array([[0.52941176, 0.50561798, 0.48387097],
                                                        [0.46391753, 0.44554455, 0.42857143],
                                                        [0.41284404, 0.39823009, 0.38461538]]))

def test_h2o3(m3_img):
    res = dev.h2o3(m3_img)
    np.testing.assert_array_almost_equal(res, np.zeros((3,3)))

def test_h2o4(m3_img):
    res = dev.h2o4(m3_img)
    print(res)
    np.testing.assert_array_almost_equal(res, np.array([[-1.86206897, -1.74193548, -1.63636364],
                                                        [-1.54285714, -1.45945946, -1.38461538],
                                                        [-1.31707317, -1.25581395, -1.2]]))

def test_h2o5(m3_img):
    res = dev.h2o5(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[-2.25, -2.04545455, -1.875],
                                                        [-1.73076923, -1.60714286, -1.5],
                                                        [-1.40625, -1.32352941, -1.25]]))

def test_ice(m3_img):
    res = dev.ice(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[-2.7, -2.45454545, -2.25],
                                                        [-2.07692308, -1.92857143, -1.8],
                                                        [-1.6875, -1.58823529, -1.5]]))

def test_bd2umratio(m3_img):
    res = dev.bd2umratio(m3_img)
    print(res)
    np.testing.assert_array_almost_equal(res, np.array([[-0.53008299, -0.5037594,  -0.48195876],
                                                        [-0.46360759, -0.44794721, -0.43442623],
                                                        [-0.42263427, -0.41225962, -0.40306122]]))
