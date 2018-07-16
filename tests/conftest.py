import pytest
import numpy as np


@pytest.fixture
def m3_functions():
    return ['bd1umratio', 'bd2umratio', 'generic_func', 'h2o2', 'h2o3', 'h2o4',
            'h2o5', 'ice', 'mustard', 'bd1900', 'bd2300', 'bd620', 'bdi1000',
            'bdi2000', 'bdi_generic', 'calc_bdi_band', 'h2o1', 'iralbedo',
            'mafic_abs', 'olindex', 'omh', 'oneum_min', 'oneum_slope', 'reflectance1',
            'reflectance2', 'reflectance3', 'reflectance4', 'thermal_ratio',
            'thermal_slope', 'twoum_ratio', 'twoum_slope', 'uvvis', 'visnir',
            'visslope', 'visuv', 'curvature', 'fe_est', 'fe_mare_est', 'luceyc_amat',
            'luceyc_omat', 'mare_omat', 'tilt']

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
