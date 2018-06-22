import numpy as np

from . import crism_funcs as cf
from ..utils import generic_func


def r770(data, **kwargs):
    """
    Name: R770
    Parameter: 0.77micron reflectance
    Formulation: R770
    Kernel Width:
      - R770: 5
    Rationale: Higher value more dusty or icy
    Caveats: Sensitive to slope effects, clouds

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [770]
    kernels = {770:5}

    return generic_func(data, wv, kernels=kernels, func = cf.rockdust1_func, **kwargs)


def rbr(data, **kwargs):
    """
    Name: RBR
    Parameter: Red/Blue Ratio
    Formulation: R770 / R440
    Kernel Width:
      - R440: 5
      - R770: 5
    Rationale: Higher value indicates more npFeOx
    Caveats: Sensitive to dust in atmosphere

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [440, 770]
    kernels = {440:5,
               770:5}

    return generic_func(data, wv, kernels=kernels, func=cf.rockdust2_func, **kwargs)


def bd530(data, use_kernels = True, **kwargs):
    """
    NAME: BD530
    PARAMETER: 0.53 micron band depth
    FORMULATION *: 1 - (R530/(a*R709+b*R440))
    RATIONALE: Crystalline ferric minerals

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [440, 530, 716]
    kernels = {}

    if use_kernels:
        wv = [440, 530, 614]
        kernels[440] = 5
        kernels[530] = 5
        kernels[614] = 5

    return generic_func(data, wv, func = cf.bd_func1, kernels = kernels, **kwargs)


def sh600(data, use_kernels = True, **kwargs):
    """
    NAME: SH600
    PARAMETER: 0.60 micron shoulder height
    FORMULATION *: 1 - (a * R530 + b * R709) / R600
    FORMULATION (with kernels) *: 1 - (a * R533 + b * R716) / R600
    RATIONALE: select ferric minerals

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [530, 600, 709]
    kernels = {}

    if use_kernels:
        wv = [533, 600, 716]
        kernels[533] = 5
        kernels[600] = 5
        kernels[716] = 3

    return generic_func(data, wv, func=cf.sh_func, kernels = kernels, **kwargs)


def sh770(data, **kwargs):
    """
    NAME: SH770
    PARAMETER: 0.77 micron shoulder height
    FORMULATION (with kernels) *: 1 - (a * R716 + b * R860) / R775
    RATIONALE: select ferric minerals

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [716, 775, 860]
    kernels = {716: 3,
               775: 5,
               860: 5}

    return generic_func(data, wv, func=cf.sh_func, kernels = kernels, **kwargs)


def bd640(data, use_kernels = True, **kwargs):
    """
    NAME: BD640
    PARAMETER: 0.64 micron band depth
    FORMULATION *: 1 - (R648 / (a * R600 + b * R709))
    FORMULATION (with kernels) *: 1 - (R624 / (a * R600 + b * R760))
    RATIONALE: select ferric minerals, especially maghemite

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [600, 648, 709]
    kernels = {}

    if use_kernels:
        wv = [600, 624, 760]
        kernels[600] = 5
        kernels[624] = 3
        kernels[760] = 5

    return generic_func(data, wv, func = cf.bd_func2, kernels = kernels, **kwargs)


def bd860(data, use_kernels = True, **kwargs):
    """
    NAME: BD860
    PARAMETER: 0.86 micron band depth
    FORMULATION *: 1 - (R860 / (a * R800 + b * R984))
    FORMULATION (with kernels) *: 1 - (R860 / (a * R755 + b * R977))
    RATIONALE: select ferric minerals ('hematite band')

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [800, 860, 984]
    kernels = {}

    if use_kernels:
        wv = [755, 860, 977]
        kernels[755] = 5
        kernels[860] = 5
        kernels[977] = 5

    return generic_func(data, wv, func = cf.bd_func2, kernels = kernels, **kwargs)


def bd920(data, use_kernels = True, **kwargs):
    """
    NAME: BD920
    PARAMETER: 0.92 micron band depth
    FORMULATION *: 1 - ( R920 / (a * R800 + b * R984) )
    FORMULATION (with kernels) *: 1 - ( R920 / (a * R807 + b * R984) )
    RATIONALE: select ferric minerals ('Pseudo BDI1000 VIS')

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray

    """
    wv = [800,920,984]
    kernels = {}

    if use_kernels:
        wv = [807, 920, 984]
        kernels[807] = 5
        kernels[920] = 5
        kernels[984] = 5

    return generic_func(data, wv, func = cf.bd_func2, kernels = kernels, **kwargs)


# TODO: rpeak1
def rpeak1(data, **kwargs):
    """
    NAME: BDI1000VIS
    PARAMETER: 1 micron integrated band depth; VIS wavelengths
    FORMULATION *: divide R830, R860, R890, R915 by RPEAK1 then
      integrate over (1 -  normalized radiances)
    RATIONALE: crystalline Fe+2 or Fe+3 minerals
    """
    raise NotImplementedError

# TODO: bdi1000VIS
def bdi1000VIS(data, **kwargs):
    """
    NAME: BDI1000VIS
    PARAMETER: 1 micron integrated band depth; VIS wavelengths
    FORMULATION *: divide R830, R860, R890, R915 by RPEAK1 then
      integrate over (1 -  normalized radiances)
    RATIONALE: crystalline Fe+2 or Fe+3 minerals
    """
    raise NotImplementedError

# TODO: bdi1000IR
def bdi1000IR(data, **kwargs):
    """
    NAME: BDI1000IR
    PARAMETER: 1 micron integrated band depth; IR wavelengths
    FORMULATION *: divide R1030, R1050, R1080, R1150
     by linear fit from peak R  between 1.3 - 1.87 microns to R2530
     extrapolated backwards, then integrate over (1 -  normalized
     radiances)
    RATIONALE: crystalline Fe+2 minerals; corrected for overlying
    aerosol induced slope
    """
    raise NotImplementedError


def r1330(data, **kwargs):
    """
    NAME: R1330
    PARAMETER: IR albedo
    FORMULATION *: R1330
    RATIONALE: IR albedo (ices > dust > unaltered mafics)

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [1330]
    kernels = {1330: 11}

    return generic_func(data, wv, func = (lambda x, y : x[0]), kernels = kernels, **kwargs)


def bd1300(data, **kwargs):
    """
    NAME: BD1300
    PARAMETER: 1.3 μm absorption associated with Fe2+ substitution in
        plagioclase
    FORMULATION (with kernels) *: 1 - ( R1320 / (a * R1080 + b * R1750) )
    RATIONALE: Plagioclase with Fe2+ substitution

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [1080, 1320, 1750]
    kernels = {1370: 5,
               1432: 15,
               1470: 5}

    return generic_func(data, wv, func = cf.bd_func2, kernels = kernels, **kwargs)


'''def ira(data, **kwargs):
    """
    NAME: IRA
    PARAMETER: 1.3 micron reflectance
    FORMULATION *: R1330
    RATIONALE: IR albedo

    Parameters
    ----------
    data : ndarray
           (n,m,p) array
    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array
    Returns
    -------
     : ndarray
       the processed ndarray

    """
    wv = [1330]
    return(generic_func(data, wv, func = cf.ira_func, **kwargs))

def olivine_index(data, **kwargs):
    """
    NAME: OLINDEX (prior to TRDR version 3)
    PARAMETER: olivine index
    FORMULATION *: (R1695 / (0.1*R1080 + 0.1*R1210 + 0.4*R1330 +
      0.4*R1470)) - 1
    RATIONALE: olivine will be strongly +; based on fayalite

    Parameters
    ----------
    data : ndarray
           (n,m,p) array
    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array
    Returns
    -------
     : ndarray
       the processed ndarray

    """
    wv = [1080,1210,1330,1470,1695]
    return(generic_func(data, wv, func = cf.olivine_index_func, **kwargs))

#@@TODO olivine_index2 (labeled olivine_index3 in JPL doc?
def olivine_index2(data, **kwargs):
    """
    NAME: OLINDEX2 (beginning with TRDR version 3)
    PARAMETER: olivine index with less sensitivity to illumination
    FORMULATION *: (((RC1054 ? R1054)/RC1054) * 0.1)
      + (((RC1211 ? R1211)/(RC1211) * 0.1)
      + (((RC1329 ? R1329)/RC1329) * 0.4)
      + (((RC1474 ? R1474)/RC1474) * 0.4)
    RATIONALE: olivine will be strongly positive
    """
    raise NotImplementedError'''


def lcp_index(data, **kwargs):
    """
    NAME: LCPINDEX
    PARAMETER: LCP index
    FORMULATION *: ((R1330 - R1050)/(R1330 + R1050)) *
                   ((R1330 - R1815)/(R1330 + R1815))
    RATIONALE: Pyroxene is strongly +; favors LCP
    Algorithm differs from published - coded as per CAT <--- What?

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [1080, 1330, 1815]
    return generic_func(data, wv, func = cf.index1_func, **kwargs)


def lcp_index2(data, **kwargs):
    """
    NAME: LCPINDEX2
    PARAMETER: Detect broad absorption centered at 1.81 μm
    FORMULATION (with kernels) *:
        RB1690 * 0.20 + RB1750 * 0.20 + RB1810 * 0.30 + RB1870 * 0.30
        Anchored at R1560 and R2450
    RATIONALE: Pyroxene is strongly +; favors LCP
    Algorithm differs from published - coded as per CAT <--- What?

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [1690, 1750, 1810, 1870]
    kernels = {1560: 7,
               1690: 7,
               1750: 7,
               1810: 7,
               1870: 7,
               2450: 7}
    raise NotImplementedError


def hcp_index(data, **kwargs):
    """
    NAME: HCPXINDEX
    PARAMETER: pyroxene index
    FORMULATION *: 100 * ((R1470 - R1050) / (R1470 + R1050)) *
                         ((R1470 - R2067) / (R1470 + R2067))
    RATIONALE: pyroxene is strongly +; favors high-Ca pyroxene
    Algorithm differs from published - coded as per CAT <--- What?

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [1050, 1470, 2067]
    return generic_func(data, wv, func = cf.index1_func, **kwargs)


def hcp_index2(data, **kwargs):
    """
    NAME: HCPXINDEX
    PARAMETER: pyroxene index
    FORMULATION *: 100 * ((R1470 - R1050) / (R1470 + R1050)) *
                         ((R1470 - R2067) / (R1470 + R2067))
    RATIONALE: pyroxene is strongly +; favors high-Ca pyroxene
    Algorithm differs from published - coded as per CAT <--- What?

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [2120, 2140, 2230, 2250, 2430, 2460]
    kernels = {1810: 7,
               2120: 5,
               2140: 7,
               2230: 7,
               2250: 7,
               2430: 7,
               2460: 7,
               2530: 7}
    raise NotImplementedError


'''#@@TODO var
def var(data, **kwargs):
    """
    NAME: VAR
    PARAMETER: spectral variance
    FORMULATION *: find variance from a line fit from 1 - 2.3 micron
      by summing in quadrature over the intervening wavelengths
    RATIONALE: Ol & Px will have high values; Type 2 areas will have
      low values
    """
    raise NotImplementedError'''


def islope1(data, **kwargs):
    """
    NAME: ISLOPE1
    PARAMETER: -1 * spectral slope1
    FORMULATION *: (R1815-R2530) / (2530-1815)
    RATIONALE: ferric coating on dark rock

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [1815, 2530]
    kernels = {1815: 5,
               2530: 5}

    return generic_func(data, wv, func = cf.islope1_func, kernels = kernels, **kwargs)


def bd1400(data, **kwargs):
    """
    NAME: BD1400
    PARAMETER: 1.4 micron H2O and OH band depth
    FORMULATION *: 1 - ( R1395 / (a * R1330 + b * R1467) )
    RATIONALE: Hydrated or hydroxylated minerals

    Parameters
    ----------
    data : ndarray
           (n,m,p) array
    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array
    Returns
    -------
     : ndarray
       the processed ndarray

    """
    wv = [1330, 1395, 1467]
    kernels = {1370: 5,
               1432: 3,
               1470: 5}
    return generic_func(data, wv, func = cf.bd_func2, kernels = kernels, **kwargs)


def bd1435(data, **kwargs):
    """
    NAME: BD1435
    PARAMETER: 1.435 micron band depth
    FORMULATION *: 1 - ( R1435 / (a * R1370 + b * R1470) )
    RATIONALE: CO2 ice, some hydrated minerals

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [1370, 1435, 1470]
    kernels = {1370: 3,
               1432: 1,
               1470: 3}

    return generic_func(data, wv, func = cf.bd_func2, kernels = kernels, **kwargs)


def bd1500(data, use_kernels = True, **kwargs):
    """
    NAME: BD1500
    PARAMETER: 1.5 micron H2O ice band depth
    FORMULATION *: 1.0 - ((R1505 + R1558) / (R1808 + R1367))
    FORMULATION (with kernels) *: 1.0 - (R1525 / (b * R1808 + a * R1367))
    RATIONALE: H2O surface ice
    Algorithm differs from published - coded as per CAT (reduced instrument noise)

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    if use_kernels:
        wv = [1367, 1525, 1808]
        kernels = {1367: 5,
                          1525: 11,
                          1808: 5}

        return generic_func(data, wv, func = cf.bd_func2, kernels = kernels, **kwargs)

    wv = [1367, 1505, 1558, 1808]
    return generic_func(data, wv, func = cf.bd1500_func, **kwargs)


def icer1(data, **kwargs):
    """
    NAME: ICER1
    PARAMETER: 1.5 micron and 1.43 micron band ratio
    FORMULATION (with kernels) *: R1510 / R1430
    RATIONALE: CO2, H20 ice mixtures

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [1430, 1510]
    kernels = {1430: 5,
               1510: 5}

    return generic_func(data, wv, func = cf.rockdust2_func, kernels = kernels, **kwargs)


def icer1_2(data, **kwargs):
    """
    NAME: ICER1_2
    PARAMETER: 1.5 micron and 1.43 micron band ratio
    FORMULATION *: 1 - ((1 - bd1435) / (1 - bd1500))
    RATIONALE: CO2, H20 ice mixtures

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    bd1435_val = bd1435(data)
    bd1500_val = bd1500(data, use_kernels = False)

    return 1 - ((1 - bd1435_val) / (1 - bd1500_val))


def bd1750(data, use_kernels = True, **kwargs):
    """
    NAME: BD1750
    PARAMETER: 1.7 micron band depth
    FORMULATION *: 1 - ( R1750 / (a * R1550 + b * R1815) )
    FORMULATION (with kernels) *: 1 - ( R1750 / (a * R1690 + b * R1815) )
    RATIONALE: gypsum

    Parameters
    ----------
    data : ndarray
           (n,m,p) array
    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array
    Returns
    -------
     : ndarray
       the processed ndarray

    """
    wv = [1550, 1750, 1815]
    kernels = {}

    if use_kernels:
        wv = [1690, 1750, 1815]
        kernels[1690] = 5
        kernels[1750] = 3
        kernels[1815] = 5

    return generic_func(data, wv, func = cf.bd_func2, kernels = kernels, **kwargs)


def bd1900(data, **kwargs):
    """
    NAME: BD1900
    PARAMETER: 1.9 micron band depth
    FORMULATION *: 1.0 - ((R1985 + R1930)/(R2067 + R1875))
    RATIONALE: H2O, chemically bound or adsorbed
    Algorithm differs from published - coded as per CAT (reduced instrument noise)

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [1875, 1930, 1985, 2067]
    return generic_func(data, wv, func = cf.bd1900_func, **kwargs)

def bd1900_2(data, **kwargs):
    """
    NAME: BD1900_2
    PARAMETER: 1.9 micron band depth
    FORMULATION (with kernels) *:
        .5 * (1 - (R1930 / (a * R1850 + b * R2067))) +
        .5 * (1 - (R1985 / (a * R1850 + b * R2067)))
    RATIONALE: H2O, chemically bound or adsorbed
    Algorithm differs from published - coded as per CAT (reduced instrument noise)

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv_set1 = [1850, 1930, 2067]
    kernel_set1 = {1850: 5,
                   1930: 5,
                   2046: 5}

    wv_set2 = [1850, 1985, 2067]
    kernel_set2 = {1850: 5,
                   1985: 5,
                   2046: 5}

    bd_1 = generic_func(data, wv_set1, func = cf.bd_func2, kernels = kernel_set1, **kwargs)
    bd_2 = generic_func(data, wv_set2, func = cf.bd_func2, kernels = kernel_set2, **kwargs)

    return .5 * (1 - bd_1) + .5 * (1 - bd_2)

def bd1900r(data, **kwargs):
    """
    NAME: BD1900r
    PARAMETER: 1.9 micron band depth
    FORMULATION *: 1.0 - ((R1908 + R1914 + R1921 + R1928 + R1934 + R1941) /
                          (R1862 + R1869 + R1875 + R2112 + R2120 + R2126))
    RATIONALE: H2O, chemically bound or adsorbed
    Algorithm differs from published - coded as per CAT (reduced instrument noise)

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [1908, 1914, 1921, 1928, 1934, 1941,
          1862, 1869, 1875, 2112, 2120, 2126]

    return generic_func(data, wv, func = cf.bd1900r_func, **kwargs)

def bd1900r2(data, **kwargs):
    """
    NAME: BD1900r2
    PARAMETER: 1.9 micron band depth
    FORMULATION *:
1 - ((R1908 / RC1908 + R1914 / RC1914 + R1921 / RC1921 + R1928 / RC1928 + R1934 / RC1934 + R1941 / RC1941) /
      (R1862 / RC1862 + R1869 / RC1869 + R1875 / RC1875 + R2112 / RC2112 + R2120 / RC2120 + R2126 / RC2126))
    RATIONALE: H2O, chemically bound or adsorbed
    Algorithm differs from published - coded as per CAT (reduced instrument noise)

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [1908, 1914, 1921, 1928, 1934, 1941,
          1862, 1869, 1875, 2112, 2120, 2126]

    raise NotImplementedError

# TODO:  bdi2000
def bdi2000(data, **kwargs):
    """
    NAME: BDI2000
    PARAMETER: 2 micron integrated band depth
    FORMULATION *: divide R1660, R1815, R2140, R2210, R2250, R2290,
      R2330, R2350, R2390, R2430, R2460 by linear fit from peak R
      between 1.3 - 1.87 microns to R2530, then integrate over
     (1 -  normalized radiances)
    RATIONALE: pyroxene abundance and particle size
    """
    raise NotImplementedError


def bd2100(data, use_kernels = True, **kwargs):
    """
    NAME: BD2100
    PARAMETER: 2.1 micron band depth
    FORMULATION *: 1 - ( ((R2120 + R2140) * 0.5) / (a * R1930 + b * R2250) )
    FORMULATION (with kernels) *: 1 - ( R2132 / (a * R1930 + b * R2250) )
    RATIONALE: monohydrated minerals

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    if use_kernels:
        wv = [1930, 2132, 2250]
        kernels = {1930: 3,
                          2132: 5,
                          2250: 3}

        return generic_func(data, wv, func = cf.bd_func2, kernels = kernels, **kwargs)

    wv = [1930, 2120, 2130, 2250]
    return generic_func(data, wv, func = cf.bd2100_func, **kwargs)

def bd2165(data, **kwargs):
    """
    NAME: BD2165
    PARAMETER: 2.165 micron Al-OH band depth
    FORMULATION (with kernels) *: 1 - ( R2165 / (a * R2120 + b * R2230) )
    RATIONALE: Pyrophyllite Kaolinite group

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [2120, 2165, 2230]
    kernels = {2120: 5,
                      2165: 3,
                      2230: 3}

    return generic_func(data, wv, func = cf.bd_func2, kernels = kernels, **kwargs)

def bd2190(data, **kwargs):
    """
    NAME: BD2190
    PARAMETER: 2.190 micron Al-OH band depth
    FORMULATION (with kernels) *: 1 - ( R2185 / (a * R2120 + b * R2250) )
    RATIONALE: Beidellite Allophane Imogolite

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [2120, 2185, 2250]
    kernels = {2120: 5,
                      2185: 3,
                      2250: 3}

    return generic_func(data, wv, func = cf.bd_func2, kernels = kernels, **kwargs)

def doub2200h(data, **kwargs):
    """
    NAME: DOUB2200H
    PARAMETER: 2.16 micron Si-OH band depth and 2.21 micron H-bound Si-OH band
        depth (doublet)
    FORMULATION (with kernels) *: 1 - ((R2205 + R2258) / (R2172 + R2311))
    RATIONALE: Opal and other Al-OH minerals

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [2172, 2205, 2258, 2311]
    kernels = {2172: 5,
                      2205: 3,
                      2258: 3,
                      2311: 5}

    return generic_func(data, wv, func = cf.doub2200h_func, kernels = kernels, **kwargs)

def min2200(data, **kwargs):
    wv_set1 = [2120, 2165, 2350]
    kernel_set1 = {2120: 5, 2165: 3, 2350: 5}

    wv_set2 = [2120, 2210, 2350]
    kernel_set2 = {2120: 5, 2210: 3, 2350: 5}

    bd_1 = generic_func(data, wv_set1, func = cf.bd_func2, kernels = kernel_set1, **kwargs)
    bd_2 = generic_func(data, wv_set2, func = cf.bd_func2, kernels = kernel_set2, **kwargs)

    return np.minimum(bd_1, bd_2)

def bd2210(data, use_kernels = True, **kwargs):
    """
    NAME: BD2210
    PARAMETER: 2.21 micron band depth
    FORMULATION *: 1 - ( R2210 / (a*R2140+b*R2250) )
    RATIONALE: Al-OH minerals: monohydrated minerals

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [2120, 2210, 2250]
    kernels = {}

    if use_kernels:
        wv = [2165, 2210, 2250]
        kernels[2165] = 5
        kernels[2210] = 5
        kernels[2250] = 5

    return generic_func(data, wv, func = cf.bd_func2, kernels = kernels, **kwargs)

def d2200(data, **kwargs):
    """
    NAME: D2200
    PARAMETER: 2.2 micron dropoff
    FORMULATION (with kernels) *: 1 - (((R2210 / RC2210) + (R2230 / RC2230)) / (2 * (R2165 / RC2165)))
        Slope for RC#### anchored at R1815 and R2430.
    RATIONALE: Al-OH minerals

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [1815, 2210, 2230, 2165, 2430]
    kernels = {1815: 7, 2165: 5, 2210: 7, 2230: 7, 2430: 7}

    raise NotImplementedError

def bd2230(data, **kwargs):
    wv = [2210, 2235, 2252]
    kernels = {2210: 3,
                      2235: 3,
                      2252: 3}

    return generic_func(data, wv, func = cf.bd_func2, kernels = kernels, **kwargs)

def bd2250(data, **kwargs):
    wv = [2120, 2245, 2340]
    kernels = {2120: 5,
                      2245: 7,
                      2340: 3}

    return generic_func(data, wv, func = cf.bd_func2, kernels = kernels, **kwargs)

def min2250(data, **kwargs):
    wv_set1 = [2165, 2210, 2350]
    kernel_set1 = {2165: 5, 2210: 3, 2350: 5}

    wv_set2 = [2165, 2265, 2350]
    kernel_set2 = {2165: 5, 2265: 5, 2350: 5}

    bd_1 = generic_func(data, wv_set1, func = cf.bd_func2, kernels = kernel_set1, **kwargs)
    bd_2 = generic_func(data, wv_set2, func = cf.bd_func2, kernels = kernel_set2, **kwargs)

    return np.minimum(bd_1, bd_2)

def bd2265(data, **kwargs):
    wv = [2210, 2265, 2340]
    kernels = {2210: 5, 2265: 3, 2340: 5}

    return generic_func(data, wv, func = cf.bd_func2, kernels = kernels, **kwargs)

def bd2290(data, **kwargs):
    """
    NAME: BD2290
    PARAMETER: 2.29 micron band depth
    FORMULATION *: 1 - ( R2290 / (a*R2250+b*R2350) )
    RATIONALE: Mg,Fe-OH minerals (at 2.3); also CO2 ice

    Parameters
    ----------
    data : ndarray
           (n,m,p) array
    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array
    Returns
    -------
     : ndarray
       the processed ndarray

      (at 2.292  microns)
    """
    wv = [2250, 2290, 2350]
    kernels = {2250: 5,
                      2290: 5,
                      2350: 5}

    return generic_func(data, wv, func = cf.bd2290_func, kernels = kernels, **kwargs)


def d2300(data, **kwargs):
    """
    NAME: D2300
    PARAMETER: 2.3 micron drop
    FORMULATION *: 1 - ( (CR2290+CR2320+CR2330) /
      (CR2140+CR2170+CR2210) ) (CR values are observed R values
      divided by values fit along the slope as determined between 1.8
      and 2.53 microns - essentially continuum corrected))
    RATIONALE: hydrated minerals; particularly clays

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray

    """
    wv = [1815, 2120, 2170, 2210, 2290, 2320, 2330, 2530]
    kernels = {1815: 5,
                      2120: 5,
                      2170: 5,
                      2210: 5,
                      2290: 3,
                      2320: 3,
                      2330: 3,
                      2530: 5}

    return generic_func(data, wv, func = cf.d2300_func, kernels = kernels, **kwargs)

def bd2355(data, **kwargs):
    wv = [2300, 2355, 2450]
    kernels = {2300: 5, 2355: 5, 2450: 5}

    return generic_func(data, wv, func = cf.bd_func2, kernels =kernels, **kwargs)

def sindex(data, **kwargs):
    """
    NAME: SINDEX
    PARAMETER: Convexity at 2.29 microns  due to absorptions at
      1.9/2.1 microns and 2.4 microns
    FORMULATION *: 1 - (R2100 + R2400) / (2 * R2290) CR
      values are observed R values divided by values fit along the
      slope as determined between 1.8 - 2.53 microns (essentially
      continuum corrected))
    RATIONALE: hydrated minerals; particularly sulfates

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [2100, 2400, 2290]

    return generic_func(data, wv, func = cf.sindex_func, **kwargs)

def sindex2(data, **kwargs):
    wv = [2120, 2290, 2400]
    kernels = {2120: 5, 2290: 7, 2400: 3}

    return generic_func(data, wv, func =cf.sh_func, kernels = kernels, **kwargs)

def icer2(data, **kwargs):
    """
    NAME: ICER2
    PARAMETER: gauge 2.7 micron band
    FORMULATION *: R2530 / R2600
    RATIONALE: CO2 ice will be >>1, H2O ice and soil will be about 1

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [2530, 2600]
    return generic_func(data, wv, func = cf.rockdust2_inverse_func, **kwargs)

'''def bdcarb(data, **kwargs):
    """
    NAME: BDCARB
    PARAMETER: overtone band depth
    FORMULATION *: 1 - ( sqrt [ ( R2330 / (a*R2230+b*R2390) ) *
      ( R2530/(c*R2390+d*R2600) ) ] )
    RATIONALE: carbonate overtones

    Parameters
    ----------
    data : ndarray
           (n,m,p) array
    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array
    Returns
    -------
     : ndarray
       the processed ndarray

    """
    wv = [2230,2330,2390,2530,2600]
    return(generic_func(data, wv, func = cf.bdcarb_func, **kwargs))

def bd3000(data, **kwargs):
    """
    NAME: BD3000
    PARAMETER: 3 micron band depth
    FORMULATION *: 1 - ( R3000 / (R2530*(R2530/R2210)) )
    RATIONALE: H2O, chemically bound or adsorbed

    Parameters
    ----------
    data : ndarray
           (n,m,p) array
    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array
    Returns
    -------
     : ndarray
       the processed ndarray

    """
    wv = [2210,2530,3000]
    return(generic_func(data, wv, func = cf.bd3000_func, **kwargs))

def bd3100(data, **kwargs):
    """
    NAME: BD3100
    PARAMETER: 3.1 micron band depth
    FORMULATION *: 1 - ( R3120 / (a*R3000+b*R3250) )
    RATIONALE: H2O ice

    Parameters
    ----------
    data : ndarray
           (n,m,p) array
    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array
    Returns
    -------
     : ndarray
       the processed ndarray

    """
    wv = [3000,3120,3250]
    return(generic_func(data, wv, func = cf.bd3100_func, **kwargs))

def bd3200(data, **kwargs):
    """
    NAME: BD3200
    PARAMETER: 3.2 micron band depth
    FORMULATION *: 1 - ( R3320 / (a*R3250+b*R3390) )
    RATIONALE: CO2 ice

    Parameters
    ----------
    data : ndarray
           (n,m,p) array
    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array
    Returns
    -------
     : ndarray
       the processed ndarray

    """
    wv = [3250,3320,3390]
    return(generic_func(data, wv, func = cf.bd3200_func, **kwargs))

def bd3400(data, **kwargs):
    """
    NAME: BD3400
    PARAMETER: 3.4 micron band depth
    FORMULATION *: 1 - ( (a*R3390+b*R3500) / (c*R3250+d*R3630) )
    RATIONALE: carbonates; organics

    Parameters
    ----------
    data : ndarray
           (n,m,p) array
    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array
    Returns
    -------
     : ndarray
       the processed ndarray

    """
    wv = [3250,3390,3500,3630]
    return(generic_func(data, wv, func = cf.bd3400_func, **kwargs))

def cindex(data, **kwargs):
    """
    NAME: CINDEX
    PARAMETER: gauge 3.9 micron band
    FORMULATION *: ( R3750 + (R3750-R3630) / (3750-3630) *
      (3920-3750) ) / R3950 - 1
    RATIONALE: carbonates

    Parameters
    ----------
    data : ndarray
           (n,m,p) array
    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array
    Returns
    -------
     : ndarray
       the processed ndarray

    Algorithm differs from published - coded as per CAT
    """
    wv = [3630,3750,3950]
    return(generic_func(data, wv, func = cf.cindex_func, **kwargs))'''
