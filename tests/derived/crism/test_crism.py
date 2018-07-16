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
    

'''def test_bd530(crism_img):
    res = crism.bd530(crism_img)
    assert False

def test_sh600(crism_img):
    res = crism.sh600(crism_img)
    assert isinstance(res, np.ndarray)

def test_bd640(crism_img):
    res = crism.bd640(crism_img)
    assert False

def test_bd860(crism_img):
    res = crism.bd860(crism_img)
    assert False

def test_bd920(crism_img):
    res = crism.bd920(crism_img)
    assert False

def test_rpeak1(crism_img):
    with pytest.raises(NotImplementedError):
        crism.rpeak1(crism_img)

def test_bdi1000VIS(crism_img):
    with pytest.raises(NotImplementedError):
        crism.bdi1000VIS(crism_img)

def test_bdi1000IR(crism_img):
    with pytest.raises(NotImplementedError):
        crism.bdi1000IR(crism_img)

def test_bdi1000IR(crism_img):
    with pytest.raises(NotImplementedError):
        crism.bdi1000IR(crism_img)

def test_ira(one_dim, wv_array, expected):
    res = crism.ira(crism_img)
    assert False

def test_olivine_index(crism_img):
    res = crism.olivine_index(crism_img)
    assert False

def test_olivine_index2(crism_img):
    with pytest.raises(NotImplementedError):
        crism.olivine_index2(crism_img)

def test_hcp_index(crism_img):
    res = crism.hcp_index(crism_img)
    assert False

def test_lcp_index(crism_img):
    res = crism.lcp_index(crism_img)
    assert False

def test_var(crism_img):
    with pytest.raises(NotImplementedError):
        crism.var(crism_img)

def test_islope1(crism_img):
    res = crism.islope1(crism_img)
    assert False

def test_bd1435(crism_img):
    res = crism.bd1435(crism_img)
    assert False

def test_bd1500(crism_img):
    res = crism.bd1500(crism_img)
    assert False

def test_icer1(crism_img):
    res = crism.icer1(crism_img)
    assert False

def test_bd1750(crism_img):
    res = crism.bd1750(crism_img)
    assert False

def test_bd1900(crism_img):
    res = crism.bd1900(crism_img)
    assert False

def test_bdi2000(crism_img):
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
