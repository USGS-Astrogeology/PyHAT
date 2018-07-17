import pytest
import numpy as np


@pytest.fixture
def m3_functions():
    return ['oneum_sym', 'bd620', 'mustard', 'bd1250', 'luceyc_amat', 'fe_est',
    'lscc_maturity', 'nbd2850', 'bdi2000', 'bd1umratio', 'oneum_slope', 'bd1050',
    'luceyc_omat', 'oneum_min', 'curvature', 'r1580', 'nbd1400', 'r2780',
    'mare_omat', 'thermal_slope', 'visslope', 'tilt', 'bd3000', 'hlnd_isfeo',
    'uvvis', 'bdi1000', 'nbd1480', 'r950_750', 'r750', 'fe_mare_est', 'bd2umratio',
    'olindex', 'nbd2700', 'visuv', 'twoum_ratio', 'nbd2300', 'bd950', 'visnir',
    'bd2300', 'thermal_ratio', 'twoum_slope', 'bd1900', 'r540']

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
