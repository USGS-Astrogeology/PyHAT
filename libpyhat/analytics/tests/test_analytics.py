import pytest

import numpy as np
from numpy.testing import assert_array_equal

import libpyhat as phat
from libpyhat.analytics import analytics
from libpyhat.examples import get_path

@pytest.fixture
def random_vector():
    return np.random.RandomState(seed=12345).random_sample(25)

def test_band_minima(random_vector):
    minidx, minvalue = analytics.band_minima(random_vector)
    assert minidx == 12
    assert minvalue == pytest.approx(0.008388297)

@pytest.mark.parametrize("lower_bound, upper_bound, expected_idx, expected_val", [
                                            (0, 7, 2, 0.18391881),
                                            pytest.param(6, 1, 0, 0, marks=pytest.mark.xfail)]
)
def test_band_minima_bounds(random_vector, lower_bound, upper_bound, expected_idx, expected_val):
    minidx, minvalue = analytics.band_minima(random_vector, lower_bound, upper_bound)
    assert minidx == expected_idx
    assert minvalue == pytest.approx(expected_val)

@pytest.mark.parametrize("spectrum, expected_zero_idx, expected_neg_one_idx, expected_center", [
                                            (np.random.RandomState(seed=12345).random_sample(25), 0.56293697, 0.42828491, [12]),
                                            (np.ones(24), 1, 1, np.array(range(24)))]
)
def test_band_center(spectrum, expected_zero_idx, expected_neg_one_idx, expected_center):
    center, center_fit = analytics.band_center(spectrum)
    assert center_fit[0] == pytest.approx(expected_zero_idx)
    assert center_fit[-1] == pytest.approx(expected_neg_one_idx)
    assert_array_equal(center[0], expected_center)

def test_band_area():
    x = np.arange(-2, 2, 0.1)
    y = x ** 2
    parabola = y
    area = analytics.band_area(parabola)
    assert area == [370.5]

@pytest.mark.parametrize("spectrum, expected_val", [
                                            (np.random.RandomState(seed=12345).random_sample(25), 0),
                                            (np.ones(24), 0)]
)
def test_band_asymmetry(spectrum, expected_val):
    assymetry = analytics.band_asymmetry(spectrum)
    assert assymetry == pytest.approx(expected_val)


@pytest.mark.parametrize("expected_val", [(14715.763)]
)
def test_run_analytics_band_area(expected_val):
    spectra = phat.Spectra.from_file(get_path('SP_2C_02_02358_S138_E3586.spc'))
    area = analytics.run_analytics(spectra, analytics.band_area)
    assert area.mean() == pytest.approx(expected_val)


@pytest.mark.parametrize("expected_wavelengths, expected_values", [(2256.103,
                                                                    909.947)]
)
def test_run_analytics_band_minima(expected_wavelengths, expected_values):
    spectra = phat.Spectra.from_file(get_path('SP_2C_02_02358_S138_E3586.spc'))
    minima = analytics.run_analytics(spectra, analytics.band_minima)
    wavelengths = [np.mean(val[0]) for val in minima]
    values = [val[1] for val in minima]
    assert np.mean(wavelengths) == pytest.approx(expected_wavelengths)
    assert np.mean(values) == pytest.approx(expected_values)


@pytest.mark.parametrize("expected_center, expected_wavelengths, expected_values", [(2358.452,
                                                                                     2256.103,
                                                                                     909.947)]
)
def test_run_analytics_band_center(expected_center, expected_wavelengths, expected_values):
    spectra = phat.Spectra.from_file(get_path('SP_2C_02_02358_S138_E3586.spc'))
    center, center_fit = analytics.run_analytics(spectra, analytics.band_center)
    wavelengths = [np.mean(val[0]) for val in center]
    values = [np.mean(val[1]) for val in center]
    # print(center_fit)
    center_fit = [center_fit[spectrum] for spectrum in center_fit]
    assert np.mean(center_fit) == pytest.approx(expected_center)
    assert np.mean(wavelengths) == pytest.approx(expected_wavelengths)
    assert np.mean(values) == pytest.approx(expected_values)


@pytest.mark.parametrize("expected_center, expected_wavelengths, expected_values", [(0.1391204,
                                                                                     2563.98,
                                                                                     0.0)]
)
def test_run_analytics_band_center_spectrum(expected_center, expected_wavelengths, expected_values):
    spectra = phat.Spectra.from_file(get_path('SP_2C_02_02358_S138_E3586.spc'))
    spectrum = spectra[spectra.columns[1]]
    center, center_fit = analytics.run_analytics(spectrum, analytics.band_center, 512.6, 2587.9)
    assert center_fit.mean() == pytest.approx(expected_center)
    assert np.mean(center[0]) == pytest.approx(expected_wavelengths)
    assert np.mean(center[1]) == expected_values


@pytest.mark.parametrize("expected_values", [(0.99974371)]
)
def test_run_analytics_band_asymmetry_spectrum(expected_values):
    spectra = phat.Spectra.from_file(get_path('SP_2C_02_02358_S138_E3586.spc'))
    spectrum = spectra[spectra.columns[1]]
    asymmetry = analytics.run_analytics(spectrum, analytics.band_asymmetry, 512.6, 2587.9)
    assert asymmetry == pytest.approx(expected_values)


@pytest.mark.parametrize("expected_values", [(35912)]
)
def test_run_analytics_band_area_spectrum(expected_values):
    spectra = phat.Spectra.from_file(get_path('SP_2C_02_02358_S138_E3586.spc'))
    spectrum = spectra[spectra.columns[1]]
    asymmetry = analytics.run_analytics(spectrum, analytics.band_area, 512.6, 2587.9)
    assert asymmetry == pytest.approx(expected_values)
