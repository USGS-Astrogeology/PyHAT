import pytest

from libpysat.derived import utils, m3, crism

def test_m3_add_derived_funcs(m3_functions):
    res = utils.add_derived_funcs(m3).keys()
    assert list(res) == m3_functions

def test_crism_add_derived_funcs(crism_functions):
    res = utils.add_derived_funcs(crism).keys()
    assert list(res) == crism_functions
