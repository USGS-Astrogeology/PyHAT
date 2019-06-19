import numpy as np
from pandas import Index
import pytest

import libpyhat
from libpyhat import Spectrum

@pytest.fixture
def basic_spectrum():
    return Spectrum([1,2,3,4],
                    index=[2.2, 3.3, 4.4, 5.5],
                    wavelengths=[2.2, 3.3, 4.4, 5.5])

# Fixtures were fixed according to: https://docs.pytest.org/en/latest/deprecations.html#calling-fixtures-directly
# ---
@pytest.fixture
def long_spectrum():
    return Spectrum([1, 1.5, 2, 2.5, 5, 3, 3.5, 7, 4, 4.5, 5],
                    index=np.arange(1,12),
                    wavelengths=np.arange(1,12))
@pytest.fixture
def metadata_spectrum():
    return Spectrum([1,2,3,4, 'a', 'b', 'c'],
                    index=[2.2, 3.3, 4.4, 5.5, 'foo', 'bar', 'bat'],
                    wavelengths=[2.2, 3.3, 4.4, 5.5],
                    metadata=['foo', 'bar', 'bat'])
@pytest.fixture
def floatwv_spectrum():
    return Spectrum([1,2,3],
                    index=[1.10001, 2.222222, 3.33300015],
                    wavelengths=[1.10001, 2.222222, 3.33300015])
@pytest.fixture
def floatwv_metadata_spectrum():
    return Spectrum([1,2,3, 'a', 'b', 'c'],
                    index=[1.10001, 2.222222, 3.33300015, 'foo', 'bar', 'bat'],
                    wavelengths=[1.10001, 2.222222, 3.33300015],
                    metadata=['foo', 'bar', 'bat'])

def test_slice_return_spectrum(basic_spectrum):
    assert isinstance(basic_spectrum[1:2], Spectrum)

def test_get_data_type(metadata_spectrum):
    assert isinstance(metadata_spectrum.data, Spectrum)

def test_get_data(metadata_spectrum, basic_spectrum):
    assert metadata_spectrum.data.equals(basic_spectrum)

def test_get_metadata_type(metadata_spectrum):
    assert isinstance(metadata_spectrum, Spectrum)

def test_get_metadata(metadata_spectrum):
    assert metadata_spectrum.metadata.equals(Spectrum(['a', 'b', 'c'],
                                                   index=['foo', 'bar', 'bat']))

def test_get_metadata_slice(metadata_spectrum):
    assert metadata_spectrum[1:].metadata.equals(Spectrum(['a', 'b', 'c'],
                                                   index=['foo', 'bar', 'bat']))

def test_get_metadata_slice_type(metadata_spectrum):
    assert isinstance(metadata_spectrum[1:].metadata, Spectrum)

def test_unary_operation(basic_spectrum):
    basic_spectrum[2.2] += 1
    assert isinstance(basic_spectrum, Spectrum)
    assert basic_spectrum[2.2] == 2

    basic_spectrum[2.2] -= 1
    basic_spectrum += 1
    assert isinstance(basic_spectrum, Spectrum)
    assert basic_spectrum.equals(Spectrum([2, 3,4,5],
                    index=[2.2, 3.3, 4.4, 5.5],
                    wavelengths=[2.2, 3.3, 4.4, 5.5]))

def test_approximate_indexer(basic_spectrum):
    assert basic_spectrum.iloc[basic_spectrum.index.get_loc(2.1, tolerance=0.11, method='nearest')] == 1

@pytest.mark.parametrize("tolerance, expected",
                        [(5, Index([1.10001, 2.22222, 3.33300, 'foo', 'bar', 'bat'])),
                         (1, Index([1.1, 2.2, 3.3, 'foo', 'bar', 'bat']))])
def test_set_metadata_tolerance(floatwv_metadata_spectrum, tolerance, expected):
    floatwv_metadata_spectrum.tolerance = tolerance
    assert isinstance(floatwv_metadata_spectrum, Spectrum)
    np.testing.assert_array_equal(floatwv_metadata_spectrum.index, expected)

@pytest.mark.parametrize("tolerance, expected",
                        [(5, Index([1.10001, 2.22222, 3.33300])),
                         (1, Index([1.1, 2.2, 3.3]))])
def test_set_floatwv_tolerance(floatwv_spectrum, tolerance, expected):
    floatwv_spectrum.tolerance = tolerance
    assert isinstance(floatwv_spectrum, Spectrum)
    np.testing.assert_array_equal(floatwv_spectrum.index, expected)


@pytest.mark.parametrize("tolerance",
                        [(np.float64(12.1)),
                         (np.int64(1))])
def test_set_bad_metadata_tolerance(floatwv_metadata_spectrum, tolerance):
    with pytest.raises(TypeError) as e:
        floatwv_metadata_spectrum.tolerance = tolerance

@pytest.mark.parametrize("tolerance",
                        [('a'),
                         ([1,2,3])])
def test_set_bad_floatwv_tolerance(floatwv_spectrum, tolerance):
    with pytest.raises(TypeError) as e:
        floatwv_spectrum.tolerance = tolerance

def test_generic_return(basic_spectrum):
    m = basic_spectrum.take([2, 3])
    assert isinstance(m, Spectrum)
    assert m.equals(Spectrum([3, 4], index=[4.4, 5.5]))

    m = basic_spectrum.sort_index()
    assert isinstance(m, Spectrum)

@pytest.mark.parametrize("func",
                         [(libpyhat.transform.smooth.boxcar),
                          (libpyhat.transform.smooth.gaussian)])
def test_smoothing_return_type(long_spectrum, func):
    ss = long_spectrum.smooth(func=func)
    assert isinstance(ss, Spectrum)

@pytest.mark.parametrize("func, kwargs",
                         [(libpyhat.transform.continuum.linear, {}),
                          (libpyhat.transform.continuum.regression, {}),
                          (libpyhat.transform.continuum.polynomial, {'order':1})
                          ])
def test_continumm_correction_long_spectrum_return_type(long_spectrum, func, kwargs):
    cc, denom = long_spectrum.continuum_correct(func=func, **kwargs)
    assert isinstance(cc, Spectrum)
    assert isinstance(denom, Spectrum)

@pytest.mark.parametrize("func, kwargs",
                          [(libpyhat.transform.continuum.regression, {})])
def test_continumm_correction_long_spectrum_return_type(metadata_spectrum, func, kwargs):
    cc, denom = metadata_spectrum.continuum_correct(func=func, **kwargs)
    assert isinstance(cc, Spectrum)
    assert isinstance(denom, Spectrum)

@pytest.mark.parametrize("func, metadata, expected",
                         [(libpyhat.transform.continuum.linear, True, None),
                          (libpyhat.transform.continuum.regression, False, None)])
def test_continuum_correction_long(long_spectrum, func, metadata, expected):
    cc, denom = long_spectrum.continuum_correct(func=func, preserve_metadata=metadata)
    if expected is None:
        assert cc.metadata is expected
    else:
        assert cc._metadata_index.tolist() == expected


@pytest.mark.parametrize("func, metadata, expected",
                         [(libpyhat.transform.continuum.regression, True, ['foo', 'bar', 'bat']),
                          (libpyhat.transform.continuum.regression, False, None)])
def test_continuum_correction_metadata(metadata_spectrum, func, metadata, expected):
    cc, denom = metadata_spectrum.continuum_correct(func=func, preserve_metadata=metadata)
    if expected is None:
        assert cc.metadata is expected
    else:
        assert cc._metadata_index.tolist() == expected
