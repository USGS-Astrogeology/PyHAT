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
    return ['generic_func', 'r770', 'rbr']

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
