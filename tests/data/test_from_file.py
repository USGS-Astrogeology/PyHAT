import pytest

from libpysat.examples import get_path
from libpysat import Spectra


@pytest.fixture
def spectral_profiler_2c():
    return get_path('SP_2C_02_02358_S138_E3586.spc')


def test_read_sp(spectral_profiler_2c):
    s = Spectra.from_file(spectral_profiler_2c)
    assert len(s.data.index) == 269
    assert len(s.metadata.index) == 139
    assert isinstance(s, Spectra)
    assert isinstance(s.data, Spectra)
    