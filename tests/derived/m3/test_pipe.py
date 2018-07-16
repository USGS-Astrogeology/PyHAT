import pytest
import numpy as np

from libpysat.derived.m3 import pipe

def test_onenum_min(m3_img):
    res = pipe.oneum_min(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[ 0.998876,  0.997753,  0.996629],
                                                        [ 0.995506,  0.994383,  0.99326 ],
                                                        [ 0.992137,  0.991014,  0.989891]]))

def test_onenum_sym(m3_img):
    res = pipe.oneum_sym(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[-0.980184, -0.980186, -0.980188],
                                                        [-0.980189, -0.980191, -0.980192],
                                                        [-0.980194, -0.980196, -0.980197]]))

def test_bd620(m3_img):
    res = pipe.bd620(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[0.16030534, 0.14788732, 0.1372549 ],
                                                        [0.12804878, 0.12, 0.11290323],
                                                        [0.10659898, 0.10096154, 0.09589041]]))

def test_bd950(m3_img):
    res = pipe.bd950(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[-0.873589, -0.735741, -0.635468],
                                                        [-0.559249, -0.499355, -0.451049],
                                                        [-0.411265, -0.37793 , -0.349593]]))

def test_bd1050(m3_img):
    res = pipe.bd1050(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[-0.332263, -0.293201, -0.262357],
                                                        [-0.237385, -0.216754, -0.199422],
                                                        [-0.184657, -0.171927, -0.160839]]))

def test_bd1250(m3_img):
    res = pipe.bd1250(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[ 0.155646,  0.143527,  0.133159],
                                                        [ 0.124188,  0.11635 ,  0.109442],
                                                        [ 0.103309,  0.097826,  0.092896]]))

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

def test_bd3000(m3_img):
    res = pipe.bd3000(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[-0.34513274, -0.32231405, -0.30232558],
                                                        [-0.28467153, -0.26896552, -0.25490196],
                                                        [-0.24223602, -0.23076923, -0.22033898]]))

def test_r1580(m3_img):
    res = pipe.r1580(m3_img)
    np.testing.assert_array_almost_equal(res, np.arange(1,10).reshape((3,3)))

def test_r950_750(m3_img):
    res = pipe.r950_750(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[10., 5.5, 4.],
                                                        [3.25, 2.8, 2.5],
                                                        [2.28571429, 2.125, 2.]]))

def test_hlnd_isfeo(m3_img):
    res = pipe.hlnd_isfeo(m3_img)
    np.testing.assert_allclose(res, np.array([[  1.273581e+13,   3.031358e+12,   9.165291e+11],
                                           [  3.331018e+11,   1.398953e+11,   6.595778e+10],
                                           [  3.416221e+10,   1.911789e+10,   1.141158e+10]]), rtol=1e+11)

def test_olindex(m3_img):
    res = pipe.olindex(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[1.28081027, 1.31103736, 1.33712718],
                                                        [1.35993684, 1.38009259, 1.39806426],
                                                        [1.41421237, 1.42881891, 1.44210815]]))

def test_oneum_slope(m3_img):
    res = pipe.oneum_slope(m3_img)
    delta = np.abs(np.sum(res - 0.01022727))
    assert delta <= 1e-6

def test_r750(m3_img):
    res = pipe.r750(m3_img)
    np.testing.assert_array_almost_equal(res, np.arange(1,10).reshape((3,3)))

def test_r1580(m3_img):
    res = pipe.r1580(m3_img)
    np.testing.assert_array_almost_equal(res, np.arange(1,10).reshape((3,3)))

def test_r540(m3_img):
    res = pipe.r540(m3_img)
    np.testing.assert_array_almost_equal(res, np.arange(1,10).reshape((3,3)))

def test_r2780(m3_img):
    res = pipe.r2780(m3_img)
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
    np.testing.assert_array_almost_equal(res, np.array([[-0.358333, -0.325318, -0.297874],
                                                        [-0.2747  , -0.254872, -0.237713],
                                                        [-0.222719, -0.209504, -0.19777 ]]))

def test_bdi2000(m3_img):
    res = pipe.bdi2000(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[-0.026842, -0.024199, -0.022029],
                                                        [-0.020215, -0.018677, -0.017356],
                                                        [-0.016209, -0.015204, -0.014316]]))


def test_bd1umratio(m3_img):
    res = pipe.bd1umratio(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[0.26226209, 0.25687621, 0.25256142],
                                                        [0.2490271, 0.24607906, 0.2435826],
                                                        [0.24144133, 0.23958448, 0.23795892]]))


def test_nbd1400(m3_img):
    res = pipe.nbd1400(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[0.52941176, 0.50561798, 0.48387097],
                                                        [0.46391753, 0.44554455, 0.42857143],
                                                        [0.41284404, 0.39823009, 0.38461538]]))

def test_nbd1480(m3_img):
    res = pipe.nbd1480(m3_img)
    np.testing.assert_array_almost_equal(res, np.zeros((3,3)))

def test_nbd2300(m3_img):
    res = pipe.nbd2300(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[-1.86206897, -1.74193548, -1.63636364],
                                                        [-1.54285714, -1.45945946, -1.38461538],
                                                        [-1.31707317, -1.25581395, -1.2]]))

def test_nbd2700(m3_img):
    res = pipe.nbd2700(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[-2.25, -2.04545455, -1.875],
                                                        [-1.73076923, -1.60714286, -1.5],
                                                        [-1.40625, -1.32352941, -1.25]]))

def test_nbd2850(m3_img):
    res = pipe.nbd2850(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[-2.7, -2.45454545, -2.25],
                                                        [-2.07692308, -1.92857143, -1.8],
                                                        [-1.6875, -1.58823529, -1.5]]))

def test_bd2umratio(m3_img):
    res = pipe.bd2umratio(m3_img)
    np.testing.assert_array_almost_equal(res, np.array([[-0.53008299, -0.5037594,  -0.48195876],
                                                        [-0.46360759, -0.44794721, -0.43442623],
                                                        [-0.42263427, -0.41225962, -0.40306122]]))
