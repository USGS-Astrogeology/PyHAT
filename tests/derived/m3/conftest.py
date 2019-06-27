from unittest import mock

import numpy as np
from libpyhat.io import io_moon_minerology_mapper as iomm
import pytest

from . m3_wv import m3_wv

@pytest.fixture
def m3_img():
    m3 = mock.Mock(spec=iomm.M3)

    def create(m):
        ndim = len(m[0])
        return np.arange(1,(9*ndim+1)).reshape(-1,3,3)
    m3.loc.__getitem__ = mock.MagicMock(side_effect=create)

    wv = np.asarray(list(m3_wv.values()))
    type(m3).wavelengths = mock.PropertyMock(return_value=wv)
    return m3
