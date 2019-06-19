import pytest
import numpy as np

def n_dim(n):
    return np.repeat(np.arange(1, n + 2), (25)).reshape(1,-1,5)

@pytest.fixture(name='n_dim')
def n_dim_fixture(n):
    return n_dim(n)

@pytest.fixture
def one_dim():
    return n_dim(1)
