import pytest
import numpy as np


@pytest.fixture
def n_dim(n):
    return np.repeat(np.arange(1, n + 2), (25)).reshape(1,-1,5)

@pytest.fixture
def one_dim():
    return n_dim(1)
