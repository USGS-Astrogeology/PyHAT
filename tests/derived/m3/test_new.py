import pytest
import numpy as np
from libpyhat.examples import get_path
from libpyhat.pyhat_io.io_moon_mineralogy_mapper import M3
from libpyhat.derived.m3 import new

def test_mustard(m3_img):
    res = new.mustard(m3_img)
    np.testing.assert_array_almost_equal(res,
                                         np.array([[[  4.94065646e-324,   9.88131292e-324,   1.48219694e-323],
                                                    [  1.97626258e-323,   2.47032823e-323,   2.96439388e-323],
                                                    [  3.45845952e-323,   3.95252517e-323,   4.44659081e-323]],
                                                    [[  4.94065646e-323,   5.43472210e-323,   5.92878775e-323],
                                                    [  6.42285340e-323,   6.91691904e-323,   7.41098469e-323],
                                                    [  7.90505033e-323,   8.39911598e-323,   8.89318163e-323]],
                                                    [[  9.38724727e-323,   9.88131292e-323,   1.03753786e-322],
                                                    [  1.08694442e-322,   1.13635099e-322,   1.18575755e-322],
                                                    [  1.23516411e-322,   1.28457068e-322,   1.33397724e-322]]]))
