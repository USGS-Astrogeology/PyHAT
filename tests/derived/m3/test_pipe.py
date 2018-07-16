import pytest
import numpy as np

from libpysat.derived.m3 import pipe


def test_bd620(m3_img):
    res = pipe.bd620(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[0.16030534, 0.14788732, 0.1372549 ],
                                                        [0.12804878, 0.12, 0.11290323],
                                                        [0.10659898, 0.10096154, 0.09589041]]))

def test_bd1900(m3_img):
    res = pipe.bd1900(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[-0.09989909, -0.09, -0.08188586],
                                                        [-0.07511381, -0.06937631, -0.06445312],
                                                        [-0.06018237, -0.05644242, -0.0531401 ]]))

def test_bd2300(m3_img):
    res = pipe.bd2300(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[0.28366762,  0.26470588,  0.2481203 ],
                                                        [0.23349057,  0.22048998,  0.20886076],
                                                        [0.19839679,  0.1889313,   0.18032787]]))

def test_h2o1(m3_img):
    res = pipe.h2o1(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[-0.34513274, -0.32231405, -0.30232558],
                                                        [-0.28467153, -0.26896552, -0.25490196],
                                                        [-0.24223602, -0.23076923, -0.22033898]]))

def test_iralbedo(m3_img):
    res = pipe.iralbedo(m3_img)
    np.testing.assert_array_almost_equal(res, np.arange(1,10).reshape((3,3)))

def test_mafic_abs(m3_img):
    res = pipe.mafic_abs(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[10., 5.5, 4.],
                                                        [3.25, 2.8, 2.5],
                                                        [2.28571429, 2.125, 2.]]))

def test_omh(m3_img):
    res = pipe.omh(m3_img)
    # Scalng back to something assert can handle well.
    np.testing.assert_array_almost_equal(res / 1e13, np.array([[1.27358071e+13, 3.03135824e+12, 9.16529095e+11],
                                                        [3.33101771e+11, 1.39895339e+11, 6.59577816e+10],
                                                        [3.41622122e+10, 1.91178943e+10, 1.14115831e+10]])/1e13)

def test_olindex(m3_img):
    res = pipe.olindex(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[1.28081027, 1.31103736, 1.33712718],
                                                        [1.35993684, 1.38009259, 1.39806426],
                                                        [1.41421237, 1.42881891, 1.44210815]]))

def test_oneum_slope(m3_img):
    res = pipe.oneum_slope(m3_img)
    delta = np.abs(np.sum(res - 0.01022727))
    assert delta <= 1e-6

def test_reflectance1(m3_img):
    res = pipe.reflectance1(m3_img)
    np.testing.assert_array_almost_equal(res, np.arange(1,10).reshape((3,3)))

def test_reflectance2(m3_img):
    res = pipe.reflectance2(m3_img)
    np.testing.assert_array_almost_equal(res, np.arange(1,10).reshape((3,3)))

def test_reflectance3(m3_img):
    res = pipe.reflectance3(m3_img)
    np.testing.assert_array_almost_equal(res, np.arange(1,10).reshape((3,3)))

def test_reflectance4(m3_img):
    res = pipe.reflectance4(m3_img)
    np.testing.assert_array_almost_equal(res, np.arange(1,10).reshape((3,3)))

def test_thermal_ratio(m3_img):
    res = pipe.thermal_ratio(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[0.1, 0.18181818, 0.25],
                                                        [0.30769231, 0.35714286, 0.4],
                                                        [0.4375, 0.47058824, 0.5]]))

def test_thermal_slope(m3_img):
    res = pipe.thermal_slope(m3_img)
    delta = np.abs(np.sum(res - 0.02045455))
    assert delta <= 1e-6
    
def test_twoum_ratio(m3_img):
    res = pipe.twoum_ratio(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[0.1, 0.18181818, 0.25],
                                                        [0.30769231, 0.35714286, 0.4],
                                                        [0.4375, 0.47058824, 0.5]]))

def test_twoum_slope(m3_img):
    res = pipe.twoum_slope(m3_img)
    delta = np.abs(np.sum(res - 0.009375))
    assert delta <= 1e-6

def test_uvvis(m3_img):
    res = pipe.uvvis(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[0.1, 0.18181818, 0.25],
                                                        [0.30769231, 0.35714286, 0.4],
                                                        [0.4375, 0.47058824, 0.5]]))

def test_visslope(m3_img):
    res = pipe.visslope(m3_img)
    delta = np.abs(np.sum(res - 0.02727273))
    assert delta <= 1e-6

def test_visuv(m3_img):
    res = pipe.visuv(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[ 10., 5.5, 4.],
                                                        [3.25, 2.8, 2.5],
                                                        [2.28571429, 2.125, 2.]]))

def test_visnir(m3_img):
    res = pipe.visnir(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[ 0.1, 0.18181818, 0.25],
                                                        [0.30769231, 0.35714286, 0.4],
                                                        [0.4375, 0.47058824, 0.5]]))

def test_bdi1000(m3_img):
    res = pipe.bdi1000(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[-26.35833306, -26.32531836, -26.29787406],
                                                        [-26.27470005, -26.25487157, -26.23771294],
                                                        [-26.22271892, -26.20950421, -26.19776983]]))

def test_bdi2000(m3_img):
    res = pipe.bdi2000(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[-21.02684206, -21.02419945, -21.02202926],
                                                        [-21.02021543, -21.01867701, -21.01735578],
                                                        [-21.01620885, -21.0152039,  -21.01431614]]))
