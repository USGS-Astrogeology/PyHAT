import pytest
import numpy as np

from libpysat.derived.crism import crism

def test_r770(crism_img):
    res = crism.r770(crism_img)
    expected = np.arange(19, 28).reshape(3,3)
    np.testing.assert_array_almost_equal(res, expected)

def test_rbr(crism_img):
    res = crism.rbr(crism_img)
    np.testing.assert_array_almost_equal(res, np.ones((3,3)))

@pytest.mark.parametrize("use_kernels, expected", [
        (True, np.zeros((3,3))),
        (False, [[ 0.238411, 0.221538, 0.206897],
                 [ 0.19407, 0.182741, 0.172662],
                 [ 0.163636, 0.155508, 0.148148]])
])
def test_bd530(crism_img, use_kernels, expected):
    res = crism.bd530(crism_img, use_kernels = use_kernels)
    np.testing.assert_array_almost_equal(res, expected)

@pytest.mark.parametrize("use_kernels, expected", [
        (True, [[0.17342537, 0.1647541, 0.15690867],
                [0.14977645, 0.14326443, 0.13729508],
                [0.13180328, 0.12673392, 0.12204007]]),
        (False, [[ 0.19608939, 0.17826308, 0.16340782],
                 [ 0.15083799, 0.14006385, 0.13072626],
                 [ 0.12255587, 0.1153467, 0.10893855]])
])
def test_sh600(crism_img, use_kernels, expected):
    res = crism.sh600(crism_img, use_kernels)
    np.testing.assert_array_almost_equal(res, expected)

def test_sh770(crism_img):
    res = crism.sh770(crism_img)
    expected = [[0.279605, 0.265625, 0.252976],
                [0.241477, 0.230978, 0.221354],
                [0.2125, 0.204327, 0.196759]]
    np.testing.assert_array_almost_equal(res, expected)

@pytest.mark.parametrize("use_kernels, expected", [
        (True, [[0.473684, 0.45, 0.428571],
                [0.409091, 0.391304, 0.375],
                [0.36, 0.346154, 0.333333]]),
        (False, [[-0.120247, -0.108133, -0.098237],
                [-0.09, -0.083038, -0.077075],
                [-0.071911, -0.067396, -0.063415]])
])
def test_bd640(crism_img, use_kernels, expected):
    res = crism.bd640(crism_img, use_kernels)
    np.testing.assert_array_almost_equal(res, expected)

@pytest.mark.parametrize("use_kernels, expected", [
        (True, np.zeros((3,3))),
        (False, [[-0.455696, -0.39779, -0.352941],
                    [-0.317181, -0.288, -0.263736],
                    [-0.243243, -0.225705, -0.210526]])
])
def test_bd860(crism_img, use_kernels, expected):
    res = crism.bd860(crism_img, use_kernels)
    np.testing.assert_array_almost_equal(res, expected)

@pytest.mark.parametrize("use_kernels, expected", [
        (True, np.zeros((3,3))),
        (False, [[0.215017, 0.199367, 0.185841],
                [0.174033, 0.163636, 0.154412],
                [0.146172, 0.138767, 0.132075]])
])
def test_bd920(crism_img, use_kernels, expected):
    res = crism.bd920(crism_img, use_kernels)
    np.testing.assert_array_almost_equal(res, expected)

def test_rpeak1(crism_img):
    with pytest.raises(NotImplementedError):
        crism.rpeak1(crism_img)

def test_bdi1000VIS(crism_img):
    with pytest.raises(NotImplementedError):
        crism.bdi1000VIS(crism_img)

def test_bdi1000IR(crism_img):
    with pytest.raises(NotImplementedError):
        crism.bdi1000IR(crism_img)

def test_r1330(crism_img):
    res = crism.r1330(crism_img)
    expected = np.arange(46, 55).reshape(3,3)
    np.testing.assert_array_almost_equal(res, expected)

def test_bd1300(crism_img):
    res = crism.bd1300(crism_img)
    expected = [[-2.36842105, -2.25, -2.14285714],
                [-2.04545455, -1.95652174, -1.875],
                [-1.8, -1.73076923, -1.66666667]]
    np.testing.assert_array_almost_equal(res, expected)

'''def test_ira(one_dim, wv_array, expected):
    res = crism.ira(crism_img)
    assert False

def test_olivine_index(crism_img):
    res = crism.olivine_index(crism_img)
    assert False

def test_olivine_index2(crism_img):
    with pytest.raises(NotImplementedError):
        crism.olivine_index2(crism_img)'''

def test_lcp_index(crism_img):
    res = crism.lcp_index(crism_img)
    expected = [[-25.39184953, -20.09925558, -16.36363636],
                [-13.61344538, -11.52204836, -9.89010989],
                [-8.58960764, -7.53488372, -6.66666667]]
    np.testing.assert_array_almost_equal(res, expected)

def test_lcp_index2(crism_img):
    with pytest.raises(NotImplementedError):
        crism.lcp_index2(crism_img)

def test_hcp_index(crism_img):
    res = crism.hcp_index(crism_img)
    expected = [[-25.39184953, -20.09925558, -16.36363636],
                [-13.61344538, -11.52204836, -9.89010989],
                [-8.58960764, -7.53488372, -6.66666667]]
    np.testing.assert_array_almost_equal(res, expected)

def test_hcp_index2(crism_img):
    with pytest.raises(NotImplementedError):
        crism.hcp_index2(crism_img)

'''def test_var(crism_img):
    with pytest.raises(NotImplementedError):
        crism.var(crism_img)'''

def test_islope1(crism_img):
    res = crism.islope1(crism_img)
    expected = np.zeros((3, 3))
    np.testing.assert_array_almost_equal(res, expected)

def test_bd1400(crism_img):
    res = crism.bd1400(crism_img)
    expected = [[ 0.47368421, 0.45, 0.42857143],
                [ 0.40909091, 0.39130435, 0.375],
                [ 0.36, 0.34615385, 0.33333333]]
    np.testing.assert_array_almost_equal(res, expected)

def test_bd1435(crism_img):
    res = crism.bd1435(crism_img)
    expected = [[ 0.9, 0.81818182, 0.75],
                [ 0.69230769, 0.64285714, 0.6],
                [ 0.5625, 0.52941176, 0.5]]
    np.testing.assert_array_almost_equal(res, expected)

def test_bd1500(crism_img):
    res = crism.bd1500(crism_img)
    expected = [[-1.421053, -1.35, -1.285714],
                [-1.227273, -1.173913, -1.125],
                [-1.08, -1.038462, -1.]]
    np.testing.assert_array_almost_equal(res, expected)

def test_icer1(crism_img):
    res = crism.icer1(crism_img)
    print(res)
    expected = np.ones((3, 3))
    np.testing.assert_array_almost_equal(res, expected)

def test_icer1_2(crism_img):
    res = crism.icer1_2(crism_img)
    expected = [[ 0.9, 0.81818182, 0.75],
                [ 0.69230769, 0.64285714, 0.6],
                [ 0.5625, 0.52941176, 0.5]]
    np.testing.assert_array_almost_equal(res, expected)

@pytest.mark.parametrize("use_kernels, expected", [
        (True, [[0.47368421, 0.45, 0.42857143],
                [0.40909091, 0.39130435, 0.375],
                [0.36, 0.34615385, 0.33333333]]),
        (False, [[0.47368421, 0.45, 0.42857143],
                 [0.40909091, 0.39130435, 0.375],
                 [0.36, 0.34615385, 0.33333333]])
])
def test_bd1750(crism_img, use_kernels, expected):
    res = crism.bd1750(crism_img)
    np.testing.assert_array_almost_equal(res, expected)

def test_bd1900(crism_img):
    res = crism.bd1900(crism_img)
    expected = [[0.992593, 0.992082, 0.991571],
                [0.99106, 0.990549, 0.990038],
                [0.989527, 0.989017, 0.988506]]
    np.testing.assert_array_almost_equal(res, expected)

def test_bd1900_2(crism_img):
    res = crism.bd1900_2(crism_img)
    expected = np.ones((3, 3))
    np.testing.assert_array_almost_equal(res, expected)

def test_bd1900r(crism_img):
    res = crism.bd1900r(crism_img)
    expected = [[0.696774, 0.687898, 0.679245],
                [0.670807, 0.662577, 0.654545],
                [0.646707, 0.639053, 0.631579]]
    np.testing.assert_array_almost_equal(res, expected)

def test_bd1900r2(crism_img):
    with pytest.raises(NotImplementedError):
        crism.bd1900r2(crism_img)

def test_bdi2000(crism_img):
    with pytest.raises(NotImplementedError):
        crism.bdi2000(crism_img)

@pytest.mark.parametrize("use_kernels, expected", [
        (True, [[-0.9, -0.81818182, -0.75],
                [-0.69230769, -0.64285714, -0.6],
                [-0.5625, -0.52941176, -0.5]]),
        (False, [[0.169203, 0.160034, 0.151807],
                 [0.144385, 0.137655, 0.131524],
                 [0.125916, 0.120767, 0.116022]])
])
def test_bd2100(crism_img, use_kernels, expected):
    res = crism.bd2100(crism_img, use_kernels)
    np.testing.assert_array_almost_equal(res, expected)

def test_bd2165(crism_img):
    res = crism.bd2165(crism_img)
    expected = [[0.347181, 0.325905, 0.307087],
                [0.290323, 0.275294, 0.261745],
                [0.249467, 0.238289, 0.22807 ]]
    np.testing.assert_array_almost_equal(res, expected)

def test_bd2190(crism_img):
    res = crism.bd2190(crism_img)
    expected = [[0.310345, 0.290323, 0.272727],
                [0.257143, 0.243243, 0.230769],
                [0.219512, 0.209302, 0.2]]
    np.testing.assert_array_almost_equal(res, expected)

def test_doub2200h(crism_img):
    res = crism.doub2200h(crism_img)
    expected = [[0.473684, 0.45, 0.428571],
                [0.409091, 0.391304, 0.375],
                [0.36, 0.346154, 0.333333]]
    np.testing.assert_array_almost_equal(res, expected)

def test_min2200(crism_img):
    res = crism.min2200(crism_img)
    expected =  [[0.473684, 0.45, 0.428571],
                [0.409091, 0.391304, 0.375],
                [0.36, 0.346154, 0.333333]]
    np.testing.assert_array_almost_equal(res, expected)

@pytest.mark.parametrize("use_kernels, expected", [
        (True, np.zeros((3, 3))),
        (False, [[0.257143, 0.239362, 0.223881],
                    [0.21028, 0.198238, 0.1875],
                    [0.177866, 0.169173, 0.16129 ]])
])
def test_bd2210(crism_img, use_kernels, expected):
    res = crism.bd2210(crism_img, use_kernels)
    np.testing.assert_array_almost_equal(res, expected)

def test_d2200(crism_img):
    with pytest.raises(NotImplementedError):
        crism.d2200(crism_img)

'''def test_bd2290(crism_img):
    res = crism.bd2290(crism_img)
    assert False

def test_d2300(crism_img):
    res = crism.d2300(crism_img)
    assert False

def test_sindex(crism_img):
    res = crism.d2300(crism_img)
    assert False

def test_sindex(crism_img):
    res = crism.sindex(crism_img)
    assert False

def test_icer2(crism_img):
    res = crism.icer2(crism_img)
    assert False

def test_bdcarb(crism_img):
    res = crism.bdcarb(crism_img)
    assert False

def test_bd3000(crism_img):
    res = crism.bd3000(crism_img)
    assert False

def test_bd3100(crism_img):
    res = crism.bd3100(crism_img)
    assert False

def test_bd3200(crism_img):
    res = crism.bd3200(crism_img)
    assert False

def test_bd3400(crism_img):
    res = crism.bd3400(crism_img)
    assert False

def test_cindex(crism_img):
    res = crism.cindex(crism_img)
    assert False'''
