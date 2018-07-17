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
