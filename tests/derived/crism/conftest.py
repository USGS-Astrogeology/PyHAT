from unittest import mock
import pytest
import numpy as np

from libpyhat.io import io_crism as icsm
from . crism_wv import crism_wv

@pytest.fixture
def crism_img():
    crism = mock.Mock(spec=icsm.Crism)

    def create(m):
        ndim = len(m[0])
        return np.arange(1,(9*ndim+1)).reshape(-1, 3, 3)

    def create_dense(_):
        return np.arange(1, 4402).reshape(489, 3, 3)

    crism.loc.__getitem__ = mock.MagicMock(side_effect=create)
    crism.iloc.__getitem__ = mock.MagicMock(side_effect=create)
    crism.__getitem__ = mock.MagicMock(side_effect=create_dense)
    wv = np.asarray(list(crism_wv.values()))
    type(crism).wavelengths = mock.PropertyMock(return_value=wv)

    return crism
