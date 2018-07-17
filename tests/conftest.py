import pytest
import numpy as np


@pytest.fixture
def m3_functions():
    return ['bd1900', 'bd1umratio', 'bd2300', 'bd2umratio', 'bd620', 'bdi1000',
            'bdi2000', 'bdi_generic', 'calc_bdi_band', 'curvature', 'fe_est',
            'fe_mare_est', 'generic_func', 'h2o1', 'h2o2', 'h2o3', 'h2o4',
            'h2o5', 'ice', 'iralbedo', 'luceyc_amat', 'luceyc_omat',
            'mafic_abs', 'mare_omat', 'mustard', 'olindex', 'omh', 'oneum_min',
            'oneum_slope', 'reflectance1', 'reflectance2', 'reflectance3',
            'reflectance4', 'thermal_ratio', 'thermal_slope', 'tilt',
            'twoum_ratio', 'twoum_slope', 'uvvis', 'visnir', 'visslope', 'visuv']

@pytest.fixture
def crism_functions():
    return ['bd1300', 'bd1400', 'bd1435', 'bd1500', 'bd1750', 'bd1900',
            'bd1900_2', 'bd1900r', 'bd1900r2', 'bd2100', 'bd2165', 'bd2190',
            'bd2210', 'bd2230', 'bd2250', 'bd2265', 'bd2290', 'bd2355',
            'bd2500h', 'bd2600', 'bd3000', 'bd3100', 'bd3200', 'bd3400',
            'bd530', 'bd640', 'bd860', 'bd920', 'bdcarb', 'bdi1000IR',
            'bdi1000VIS', 'bdi2000', 'cindex', 'cindex2', 'd2200', 'd2300',
            'doub2200h', 'generic_func', 'hcp_index', 'hcp_index2', 'icer1',
            'icer1_2', 'icer2', 'irr1', 'irr2', 'irr3', 'islope1', 'lcp_index',
            'lcp_index2', 'min2200', 'min2250', 'min2295_2480', 'min2345_2537',
            'olivine_index2', 'olivine_index3', 'r1080', 'r1330', 'r1506',
            'r2529', 'r3920', 'r440', 'r530', 'r600', 'r770', 'rbr', 'rpeak1',
            'sh600', 'sh770', 'sindex', 'sindex2']

@pytest.fixture
def n_dim(n):
    return np.repeat(np.arange(1, n + 1), (25)).reshape(n,-1,5)

@pytest.fixture
def eighty_three_dim():
    return n_dim(83)

@pytest.fixture
def thirty_dim():
    return n_dim(30)

@pytest.fixture
def twenty_five_dim():
    return n_dim(25)

@pytest.fixture
def eight_dim():
    return n_dim(8)

@pytest.fixture
def six_dim():
    return n_dim(6)

@pytest.fixture
def five_dim():
    return n_dim(5)

@pytest.fixture
def four_dim():
    return n_dim(4)

@pytest.fixture
def three_dim():
    return n_dim(3)

@pytest.fixture
def two_dim():
    return n_dim(2)

@pytest.fixture
def one_dim():
    return n_dim(1)
