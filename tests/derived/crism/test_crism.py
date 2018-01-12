import pytest
import numpy as np

from libpysat import HCube
from libpysat.derived.crism import crism

@pytest.fixture
def test_params(wavelengths, expected = 1):
    return(np.array(wavelengths), expected)

@pytest.mark.parametrize('wv_array, expected',
                         [test_params([770])])

def test_rockdust1(one_dim, wv_array, expected):
    data = HCube(one_dim, wv_array, waxis = 0)
    res = crism.rockdust1(data, wv_array)
    assert res.all() == expected


@pytest.mark.parametrize('wv_array, expected',
                         [test_params([440,770])])

def test_rockdust2(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0)
    res = crism.rockdust2(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                         [test_params([440,530,709])])

def test_bd530(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    res = crism.bd530(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                         [test_params([533,600,710])])

def test_sh600(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    res = crism.sh600(data, wv_array)
    assert res.all() == expected


@pytest.mark.parametrize('wv_array, expected',
                         [test_params([600,648,709])])

def test_bd640(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    res = crism.bd640(data, wv_array)
    assert res.all() == expected


@pytest.mark.parametrize('wv_array, expected',
                         [test_params([800,860,984])])

def test_bd860(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    res = crism.bd860(data, wv_array)
    assert res.all() == expected


@pytest.mark.parametrize('wv_array, expected',
                         [test_params([800,920,984])])

def test_bd920(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    res = crism.bd920(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                         [test_params([800,920,984])])

def test_rpeak1(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    with pytest.raises(NotImplementedError):
        crism.rpeak1(data, wv_array)

@pytest.mark.parametrize('wv_array, expected',
                         [test_params([800,920,984])])
def test_bdi1000VIS(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    with pytest.raises(NotImplementedError):
        crism.bdi1000VIS(data, wv_array)


@pytest.mark.parametrize('wv_array, expected',
                         [test_params([800,920,984])])
def test_bdi1000IR(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    with pytest.raises(NotImplementedError):
        crism.bdi1000IR(data, wv_array)

@pytest.mark.parametrize('wv_array, expected',
                         [test_params([800,920,984])])
def test_bdi1000IR(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    with pytest.raises(NotImplementedError):
        crism.bdi1000IR(data, wv_array)


@pytest.mark.parametrize('wv_array, expected',
                         [test_params([1330])])
def test_ira(one_dim, wv_array, expected):
    data = HCube(one_dim, wv_array, waxis = 0)
    res = crism.ira(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                         [test_params([1080,1210,1330,1470,1695])])
def test_olivine_index(five_dim, wv_array, expected):
    data = HCube(five_dim, wv_array, waxis = 0)
    res = crism.olivine_index(data, wv_array)
    assert res.all() == expected


@pytest.mark.parametrize('wv_array,expected',
                        [test_params([1080,1210,1330,1470,1695])])
def test_olivine_index2(five_dim, wv_array, expected):
    data = HCube(five_dim, wv_array, waxis = 0)
    with pytest.raises(NotImplementedError):
        crism.olivine_index2(data, wv_array)


@pytest.mark.parametrize('wv_array,expected',
                        [test_params([1080,1470,2067])])
def test_hcp_index(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    res = crism.hcp_index(data, wv_array)
    assert res.all() == expected


@pytest.mark.parametrize('wv_array,expected',
                        [test_params([1080,1330,1815])])
def test_lcp_index(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    res = crism.lcp_index(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array,expected',
                        [test_params([1080,1210,1330,1470,1695])])
def test_var(five_dim, wv_array, expected):
    data = HCube(five_dim, wv_array, waxis = 0)
    with pytest.raises(NotImplementedError):
        crism.var(data, wv_array)


@pytest.mark.parametrize('wv_array,expected',
                        [test_params([1815,2530])])
def test_islope1(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0)
    res = crism.islope1(data, wv_array)
    assert res.all() == expected


@pytest.mark.parametrize('wv_array,expected',
                        [test_params([1370,1430,1470])])
def test_bd1435(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    res = crism.bd1435(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array,expected',
                        [test_params([1367,1505,1558,1808],0)])
def test_bd1500(four_dim, wv_array, expected):
    data = HCube(four_dim, wv_array, waxis = 0)
    res = crism.bd1500(data, wv_array)
    assert res.all() == expected


@pytest.mark.parametrize('wv_array,expected',
                        [test_params([1430,1510])])
def test_icer1(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0)
    res = crism.icer1(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array,expected',
                        [test_params([1557,1750,1815])])
def test_bd1750(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    res = crism.bd1750(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array,expected',
                        [test_params([1874,1927,1973,2006],0)])
def test_bd1900(four_dim, wv_array, expected):
    data = HCube(four_dim, wv_array, waxis = 0)
    res = crism.bd1900(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array,expected',
                        [test_params([1080,1210,1330,1470,1695])])
def test_bdi2000(five_dim, wv_array, expected):
    data = HCube(five_dim, wv_array, waxis = 0)
    with pytest.raises(NotImplementedError):
        crism.bdi2000(data, wv_array)



@pytest.mark.parametrize('wv_array,expected',
                        [test_params([1930,2120,2140,2250],0.80487805)])
def test_bd2100(four_dim, wv_array, expected):
    data = HCube(four_dim, wv_array, waxis = 0)
    res = crism.bd2100(data, wv_array)
    eq = np.full(res.shape, expected)
    assert np.allclose(res,eq)


@pytest.mark.parametrize('wv_array,expected',
                        [test_params([2140,2210,2250])])
def test_bd2210(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    res = crism.bd2210(data, wv_array)
    assert res.all() == expected


@pytest.mark.parametrize('wv_array,expected',
                        [test_params([2250,2290,2350])])
def test_bd2290(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    res = crism.bd2290(data, wv_array)
    assert res.all() == expected


@pytest.mark.parametrize('wv_array,expected',
                        [test_params([1815,2120,2170,2210,2290,2320,2330,2530])])
def test_d2300(eight_dim, wv_array, expected):
    data = HCube(eight_dim, wv_array, waxis = 0)
    res = crism.d2300(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array,expected',
                        [test_params([2100,2400,2290])])
def test_sindex(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    res = crism.d2300(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array,expected',
                        [test_params([2100,2400,2290])])
def test_sindex(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    res = crism.sindex(data, wv_array)
    assert res.all() == expected


@pytest.mark.parametrize('wv_array,expected',
                        [test_params([2530,2600])])
def test_icer2(two_dim, wv_array, expected):
    data = HCube(two_dim, wv_array, waxis = 0)
    res = crism.icer2(data, wv_array)
    assert res.all() == expected


@pytest.mark.parametrize('wv_array,expected',
                        [test_params([2230,2330,2390,2530,2600])])
def test_bdcarb(five_dim, wv_array, expected):
    data = HCube(five_dim, wv_array, waxis = 0)
    res = crism.bdcarb(data, wv_array)
    assert res.all() == expected


@pytest.mark.parametrize('wv_array,expected',
                    [test_params([2210,2530,3000])])
def test_bd3000(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    res = crism.bd3000(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array,expected',
                    [test_params([3000,3120,3250])])
def test_bd3100(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    res = crism.bd3100(data, wv_array)
    assert res.all() == expected


@pytest.mark.parametrize('wv_array,expected',
                    [test_params([3250,3320,3390],0)])
def test_bd3200(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    res = crism.bd3200(data, wv_array)
    assert res.all() == expected


@pytest.mark.parametrize('wv_array,expected',
                    [test_params([3250,3390,3500,3630])])
def test_bd3400(four_dim, wv_array, expected):
    data = HCube(four_dim, wv_array, waxis = 0)
    res = crism.bd3400(data, wv_array)
    assert res.all() == expected


@pytest.mark.parametrize('wv_array,expected',
                    [test_params([3630,3750,3950])])
def test_cindex(three_dim, wv_array, expected):
    data = HCube(three_dim, wv_array, waxis = 0)
    res = crism.cindex(data, wv_array)
    assert res.all() == expected
