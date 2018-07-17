import numpy as np
from scipy.misc import derivative
from ..utils import compute_b_a, compute_slope, line_fit

def rockdust1_func(bands):
    R770, = bands
    return R770

def rockdust2_func(bands):
    return bands[1] / bands[0]

def rockdust2_inverse_func(bands):
    return bands[0] / bands[1]

def bd_func1(bands, wv):
    b, a = compute_b_a(wv)
    return 1.0 - (bands[1] / ((a * bands[2]) + (b * bands[0])))

def bd_func2(bands, wv):
    b, a = compute_b_a(wv)
    return 1.0 - (bands[1] / ((a * bands[0]) + (b * bands[2])))

def sh_func(bands, wv):
    b, a = compute_b_a(wv)
    return 1.0 - (((a * bands[0]) + (b * bands[2])) / bands[1])

def rpeak1_func(data, wv):
    def func(x):
        return a * x**5 + b * x**4 + c * x**3 + d * x**2 + e * x + f

    for i, band in enumerate(data):
        band = band.flatten()
        wavelength = np.full(len(band), wv[i])
        a, b, c, d, e, f = np.polyfit(band, wavelength, 5)
        derivation = derivative(func, 1.0, dx=1e-6, n = 1)

        if derivation == 0:
            return wv[i]

#@@TODO bdi1000vis

def olivine_index2_func(bands):
    b1080, b1210, b1330, b1470, b1750, b2400 = bands

    slope = compute_slope(1750, 2400, b1750, b2400)

    rc1080 = line_fit(slope, (1080 - 1750), b1750)
    rc1210 = line_fit(slope, (1210 - 1750), b1750)
    rc1330 = line_fit(slope, (1330 - 1750), b1750)
    rc1470 = line_fit(slope, (1470 - 1750), b1750)

    rb1080 = (rc1080 - b1080) / rc1080
    rb1210 = (rc1210 - b1210) / rc1210
    rb1330 = (rc1330 - b1330) / rc1330
    rb1470 = (rc1470 - b1470) / rc1470

    return (rb1080 * .1) + (rb1210 * .1) + (rb1330 * .4) + (rb1470  *.4)

def olivine_index3_func(bands):
    b1080, b1152, b1210, b1250, b1263, b1276, \
    b1330, b1368, b1395, b1427, b1470, b1750, b2400 = bands

    slope = compute_slope(1750, 2400, b1750, b2400)

    rc1080 = line_fit(slope, (1080 - 1750), b1750)
    rc1152 = line_fit(slope, (1152 - 1750), b1750)
    rc1210 = line_fit(slope, (1210 - 1750), b1750)
    rc1250 = line_fit(slope, (1250 - 1750), b1750)
    rc1263 = line_fit(slope, (1263 - 1750), b1750)
    rc1276 = line_fit(slope, (1276 - 1750), b1750)
    rc1330 = line_fit(slope, (1330 - 1750), b1750)
    rc1368 = line_fit(slope, (1368 - 1750), b1750)
    rc1395 = line_fit(slope, (1395 - 1750), b1750)
    rc1427 = line_fit(slope, (1427 - 1750), b1750)
    rc1470 = line_fit(slope, (1470 - 1750), b1750)

    rb1080 = (rc1080 - b1080) / rc1080
    rb1152 = (rc1152 - b1152) / rc1152
    rb1210 = (rc1210 - b1210) / rc1210
    rb1250 = (rc1250 - b1250) / rc1250
    rb1263 = (rc1263 - b1263) / rc1263
    rb1276 = (rc1276 - b1276) / rc1276
    rb1330 = (rc1330 - b1330) / rc1330
    rb1368 = (rc1368 - b1368) / rc1368
    rb1395 = (rc1395 - b1395) / rc1395
    rb1427 = (rc1427 - b1427) / rc1427
    rb1470 = (rc1470 - b1470) / rc1470

    return (rb1080 * 0.03 + rb1152 * 0.03 + rb1210 * 0.03 + rb1250 * 0.03 +
    rb1263 * 0.07 + rb1276 * 0.07 + rb1330 * 0.12 + rb1368 * 0.12 +
    rb1395 * 0.14 + rb1427 * 0.18 + rb1470 * 0.18)

def index1_func(bands):
    return (100 * ((bands[1] - bands[0]) / (bands[1] + bands[0])) * \
                  ((bands[1] - bands[2]) / (bands[1] + bands[2])))

def lcp_index2_func(bands):
    b1560, b1690, b1750, b1810, b1870, b2450 = bands

    slope = compute_slope(1560, 2450, b1560, b2450)

    rc1690 = line_fit(slope, (1690 - 1560), b1560)
    rc1750 = line_fit(slope, (1750 - 1560), b1560)
    rc1810 = line_fit(slope, (1810 - 1560), b1560)
    rc1870 = line_fit(slope, (1870 - 1560), b1560)

    rb1690 = (rc1690 - b1690) / rc1690
    rb1750 = (rc1750 - b1750) / rc1750
    rb1810 = (rc1810 - b1810) / rc1810
    rb1870 = (rc1870 - b1870) / rc1870

    return (rb1690 * .2) + (rb1750 * .2) + (rb1810 * .3) + (rb1870  *.3)

def hcp_index2_func(bands):
    b1810, b2120, b2140, b2230, b2250, b2430, b2460, b2530 = bands

    slope = compute_slope(1810, 2530, b1810, b2530)

    rc2120 = line_fit(slope, (2120 - 1810), b1810)
    rc2140 = line_fit(slope, (2140 - 1810), b1810)
    rc2230 = line_fit(slope, (2230 - 1810), b1810)
    rc2250 = line_fit(slope, (2250 - 1810), b1810)
    rc2430 = line_fit(slope, (2430 - 1810), b1810)
    rc2460 = line_fit(slope, (2460 - 1810), b1810)
    rc2530 = line_fit(slope, (2530 - 1810), b1810)

    rb2120 = (rc2120 - b2120) / rc2120
    rb2140 = (rc2140 - b2140) / rc2140
    rb2230 = (rc2230 - b2230) / rc2230
    rb2250 = (rc2250 - b2250) / rc2250
    rb2430 = (rc2430 - b2430) / rc2430
    rb2460 = (rc2460 - b2460) / rc2460
    rb2530 = (rc2530 - b2530) / rc2530

    return ((rb2120 * .1) + (rb2140 * .1) + (rb2230 * .15) +
               (rb2250 * .30) + (rb2430 * .2) + (rb2460 * .15))

#@@TODO var

def islope1_func(bands, wv):

    return (bands[0] - bands[1])/(wv[1] - wv[0])

def bd1500_func(bands):
    b1367, b1505, b1558, b1808 = bands
    return 1.0 - ((b1558 + b1505) / (b1808 + b1367))

def bd1900_func(bands, wv):
    b1875, b1930, b1985, b2067 = bands
    wv = [wv[0], ((wv[1] + wv[2] )/2), wv[3]]
    b, a = compute_b_a(wv)

    return (1.0 - (((b1985 + b1930) / 2) / (b * 2067 + a * 1875)))

def bd1900r_func(bands):
    R1908, R1914, R1921, R1928, R1934, R1941, \
    R1862, R1869, R1875, R2112, R2120, R2126 = bands

    numerator = (R1908 + R1914 + R1921 + R1928 + R1934 + R1941)
    denominator = (R1862 + R1869 + R1875 + R2112 + R2120 + R2126)

    return 1 - (numerator / denominator)

def bd1900r2_func(bands, wv):
    b1850, b1862, b1869, b1875, b1908, b1914, b1921,\
    b1928, b1934, b1941, b2060, b2112, b2120, b2126= bands

    slope = compute_slope(1850, 2060, b1850, b2060)

    rc1862 = line_fit(slope, (1862 - 1850), b1850)
    rc1869 = line_fit(slope, (1869 - 1850), b1850)
    rc1875 = line_fit(slope, (1875 - 1850), b1850)
    rc1908 = line_fit(slope, (1908 - 1850), b1850)
    rc1914 = line_fit(slope, (1914 - 1850), b1850)
    rc1921 = line_fit(slope, (1921 - 1850), b1850)
    rc1928 = line_fit(slope, (1928 - 1850), b1850)
    rc1934 = line_fit(slope, (1934 - 1850), b1850)
    rc1941 = line_fit(slope, (1941 - 1850), b1850)
    rc2112 = line_fit(slope, (2112 - 1850), b1850)
    rc2120 = line_fit(slope, (2120 - 1850), b1850)
    rc2126 = line_fit(slope, (2126 - 1850), b1850)

    numerator = (b1908 / rc1908 + b1914 / rc1914 + b1921 / rc1921 + \
                          b1928 / rc1928 + b1934 / rc1934 + b1941 / rc1941)
    denominator = (b1862 / rc1862 + b1869 / rc1869 + b1875 / rc1875 + \
                          b2112 / rc2112 + b2120 / rc2120 + b2126 / rc2126)

    return 1 - (numerator / denominator)
#@@TODO bdi2000

def bd2100_func(bands, wv):
    b1930, b2120, b2130, b2250 = bands
    wv = [wv[0], ((wv[1] + wv[2]) / 2), wv[3]]
    bands = [bands[0], ((bands[1] + bands[2]) * .5), bands[3]]

    return bd_func2(bands, wv)

def doub2200h_func(bands):
    b2172, b2205, b2258, b2311 = bands

    return (1 - ((b2205 + b2258) / (b2172 + b2311)))

def d2200_func(bands):
    b1815, b2165, b2210, b2230, b2430 = bands

    slope = compute_slope(1815, 2430, b1815, b2430)

    rc2165 = line_fit(slope, (2165 - 1815), b1815)
    rc2210 = line_fit(slope, (2210 - 1815), b1815)
    rc2230 = line_fit(slope, (2230 - 1815), b1815)

    return 1 - (((b2210 / rc2210) + (b2230 / rc2230)) / (2 * b2165 / rc2165))

def d2300_func(bands):
    b1815, b2120, b2170, b2210, b2290, b2320, b2330, b2530 = bands

    slope = compute_slope(1815, 2530, b1815, b2530)
    cr2290 = line_fit(slope, (2290 - 1815), b1815)
    cr2320 = line_fit(slope, (2320 - 1815), b1815)
    cr2330 = line_fit(slope, (2330 - 1815), b1815)
    cr2120 = line_fit(slope, (2120 - 1815), b1815)
    cr2170 = line_fit(slope, (2170 - 1815), b1815)
    cr2210 = line_fit(slope, (2210 - 1815), b1815)

    return (1.0 - (((b2290 / cr2290) + (b2320 / cr2320) + (b2330 / cr2330)) /
                   ((b2120 / cr2120) + (b2170 / cr2170) + (b2210 / cr2210))))

def sindex_func(bands):
    b2100, b2400, b2290 = bands
    return (1.0 - ((b2100 + b2400) / (2 * b2290)))

def bd2500h_func(bands):
    b2380, b2500, b2510, b2540 = bands

    return 1.0 - ((b2500 + b2510) / (b2540 + b2380))

def bd3000_func(bands) :
    b2210, b2530, b3000 = bands
    return ( 1 - (b3000 / (b2530 * (b2530 / b2210))))

def bd3400_func(bands, wv):
    b3250, b3390, b3500, b3630 = bands
    b, a = compute_b_a([wv[0], ((wv[1] + wv[2]) / 2), wv[3]])
    d = (((wv[1] + wv[2]) * .5) - wv[0]) / (wv[3] - wv[0])
    c = 1.0 - d
    return 1.0 - ((((a * b3390) + (b * b3500)) * .5) / ((c * b3250) + (d * b3630)))


def cindex_func(bands):
    b3630, b3750,b3950 = bands
    return (((b3750 + ((b3750 - b3630) / ((3750 - 3630) * (3950 - 3750))))) / b3950 - 1)
