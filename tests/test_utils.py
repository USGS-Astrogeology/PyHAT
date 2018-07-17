import pytest

from libpysat.derived import utils, m3, crism

def test_m3_add_derived_funcs(m3_functions):
    res = utils.get_derived_funcs(m3)
    res = list(res.keys())
    res.sort()
    assert res == m3_functions

def test_crism_add_derived_funcs(crism_functions):
    res = utils.get_derived_funcs(crism)
    res = list(res.keys())
    res.sort()
    assert res == crism_functions
