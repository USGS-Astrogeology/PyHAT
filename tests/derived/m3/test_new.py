import pytest
import numpy as np

from libpysat.derived.m3 import new
from libpysat import HCube

@pytest.fixture
def test_params(wavelengths):
    return (np.array(wavelengths), 1)

full_wavelengths = [540,  580,  620,  660,  700,
                    730,  750,  770,  790,  810,
                    830,  850,  870,  890,  910,
                    930,  950,  970,  989, 1009,
                   1029, 1049, 1069, 1089, 1109,
                   1129, 1149, 1169, 1189, 1209,
                   1229, 1249, 1269, 1289, 1309,
                   1329, 1349, 1369, 1389, 1409,
                   1429, 1449, 1469, 1489, 1508,
                   1528, 1548, 1578, 1618, 1658,
                   1698, 1738, 1778, 1818, 1858,
                   1898, 1938, 1978, 2018, 2057,
                   2097, 2137, 2177, 2217, 2257,
                   2297, 2337, 2377, 2417, 2457,
                   2497, 2537, 2576, 2616, 2656,
                   2696, 2736, 2776, 2816, 2856,
                   2896, 2936, 2976]

@pytest.mark.parametrize('wv_array, expected',
                          [test_params(full_wavelengths)])

def test_mustard(eighty_three_dim, wv_array, expected):
    data = HCube(eighty_three_dim, wv_array, waxis = 0, tolerance = 2)
    res = new.mustard(data, wv_array)
    for i in range(len(res)):
        assert res[i].all() == expected
