from libpysat.transform import stretch

def test_linear_stretch(one_dim, expected = 1):
    res = stretch.linear_stretch(one_dim)
    assert res.all() == expected

def test_standard_deviation_stretch(one_dim, expected = 1):
    res = stretch.standard_deviation_stretch(one_dim)
    assert res.all() == expected

def test_inverse_stretch(one_dim, expected = 0):
    res = stretch.inverse_stretch(one_dim)
    assert res.all() == expected

def test_histequ_stretch(one_dim, expected = 1):
    res = stretch.histequ_stretch(one_dim)
    assert res.all() == expected
