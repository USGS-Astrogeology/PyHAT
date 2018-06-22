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
        (True, [[ 0.473684, 0.45, 0.428571],
                [ 0.409091, 0.391304, 0.375],
                [ 0.36, 0.346154, 0.333333]]),
        (False, [[0.096935, 0.088906, 0.082105],
                 [0.076271, 0.071211, 0.066781],
                 [0.062869, 0.059391, 0.056277]])
])
def test_bd640(crism_img, use_kernels, expected):
    res = crism.bd640(crism_img, use_kernels)
    np.testing.assert_array_almost_equal(res, expected)

@pytest.mark.parametrize("use_kernels, expected", [
        (True, np.zeros((3,3))),
        (False, [[0.2384106, 0.22153846, 0.20689655],
                 [0.19407008, 0.18274112, 0.17266187],
                 [0.16363636, 0.15550756, 0.14814815]])
])
def test_bd860(crism_img, use_kernels, expected):
    res = crism.bd860(crism_img, use_kernels)
    np.testing.assert_array_almost_equal(res, expected)

@pytest.mark.parametrize("use_kernels, expected", [
        (True, np.zeros((3,3))),
        (False, [[-0.37724551, -0.33157895, -0.29577465],
                 [-0.26694915, -0.24324324, -0.22340426],
                 [-0.20655738, -0.19207317, -0.17948718]])
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
    expected = np.zeros((3, 3))
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
    expected = [[0.996322, 0.996068, 0.995814],
                [0.995561, 0.995307, 0.995053],
                [0.9948, 0.994546, 0.994292]]
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

'''def test_bdi2000(crism_img):
    with pytest.raises(NotImplementedError):
        crism.bdi2000(crism_img)

def test_bd2100(crism_img):
    res = crism.bd2100(crism_img)
    eq = np.full(res.shape, expected)
    assert np.allclose(res,eq)

def test_bd2210(crism_img):
    res = crism.bd2210(crism_img)
    assert False

def test_bd2290(crism_img):
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
