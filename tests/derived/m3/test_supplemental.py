import pytest
import numpy as np

from libpysat.derived.m3 import supplemental as sup

def test_curvature(m3_img):
    res = sup.curvature(m3_img)
    np.testing.assert_array_almost_equal(res, np.ones((3,3)))

def test_fe_est(m3_img):
    res = sup.fe_est(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[-33.12599412, -27.63587155, -20.91762514], 
                                                        [-15.99699961, -13.07633664, -11.36015607],
                                                        [-10.30167489, -9.61287544, -9.14316831]]))

def test_fe_mare_est(m3_img):
    res = sup.fe_mare_est(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[ -328.359308, -351.4761815, -449.634938], 
                                                        [-566.55416525, -690.9775808, -819.1530905],
                                                        [-949.472654, -1081.13225113, -1213.685204]]))

def test_luceyc_amat(m3_img):
    res = sup.luceyc_amat(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[8.79589109, 4.68376985, 4.05557641],
                                                        [4.45872179, 5.22223132, 6.1170009 ],
                                                        [7.06485596, 8.0366862, 9.02040465]]))

def test_luceyc_omat(m3_img):
    res = sup.luceyc_omat(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[8.85790607, 4.71831538, 4.05246838],
                                                        [4.42831797, 5.17672677, 6.06320872],
                                                        [7.0062108, 7.975, 8.9567014 ]]))

def test_mare_omat(m3_img):
    res = sup.mare_omat(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[-9.6527, -5.0461, -3.3897],
                                                        [-2.47085, -1.84702, -1.3707],
                                                        [-0.97867143, -0.639325, -0.3351]]))

def test_tilt(m3_img):
    res = sup.tilt(m3_img)
    assert (res == -9).all()