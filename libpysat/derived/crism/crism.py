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
    res = generic_func(data, wv, kernels=kernels, func = cf.rockdust1_func, **kwargs)
    return res

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
    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array
    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wv = [440, 770]
    kernels = {440:5,
               770:5}
    return(generic_func(data, wv, kernels=kernels, func=cf.rockdust2_func, **kwargs))

def bd530(data, **kwargs):
    """
    NAME: BD530
    PARAMETER: 0.53 micron band depth
    FORMULATION *: 1 - (R530/(a*R709+b*R440))
    RATIONALE: Crystalline ferric minerals

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
    wv = [440, 530, 716]
    return(generic_func(data, wv, func = cf.bd530_func, **kwargs))

def bd530_2(data, **kwargs):
    """
    NAME: BD530_2
    PARAMETER: 0.53 micron band depth
    FORMULATION *: 1 - (R530/(a*R709+b*R440))
    RATIONALE: Crystalline ferric minerals

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
    wv = [440, 530, 614]
    kernels = {440: 5,
                      530: 5,
                      614: 5}
    return(generic_func(data, wv, kernels = kernels, func = cf.bd530_func, **kwargs))

def sh600(data, **kwargs):
    """
    NAME: SH600
    PARAMETER: 0.60 micron shoulder height
    FORMULATION *: R600/(a*R530+b*R709)
    RATIONALE: select ferric minerals

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
    wv = [530, 600, 709]
    return(generic_func(data, wv, func=cf.sh600_func, **kwargs))

def sh600_2(data, **kwargs):
    """
    NAME: SH600_2
    PARAMETER: 0.60 micron shoulder height
    FORMULATION *: R600/(a*R530+b*R709)
    RATIONALE: select ferric minerals

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
    wv = [533, 600, 710]
    kernels = {533: 5,
                      600: 5,
                      716: 3}
    return(generic_func(data, wv, kernels = kernels, func=cf.sh600_func, **kwargs))

def sh770(data, **kwargs):
    """
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
    wv = [716, 775, 860]
    kernels  = {716: 3,
                       775: 5,
                       860: 5}
    return (generic_func(data, wv, kernels = kernels, func = cf.sh770_func, **kwargs))

def bd640(data, **kwargs):
    """
    NAME: BD640
    PARAMETER: 0.64 micron band depth
    FORMULATION *: 1 - (R648/(a*R600+b*R709))
    RATIONALE: select ferric minerals, especially maghemite

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
    wv = [600,648,709]
    return(generic_func(data, wv, func = cf.bd640_func, **kwargs))


def bd640_2(data, **kwargs):
    """
    NAME: BD640_2
    PARAMETER: 0.64 micron band depth
    FORMULATION *: 1 - (R648/(a*R600+b*R709))
    RATIONALE: select ferric minerals, especially maghemite

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
    wv = [600,648,709]
    kernels = {600: 5,
                      624: 3,
                      760: 5}
    return(generic_func(data, wv, kernels = kernels, func = cf.bd640_func, **kwargs))

def bd860(data, **kwargs):
    """
    NAME: BD860
    PARAMETER: 0.86 micron band depth
    FORMULATION *: 1 - (R860/(a*R800+b*R984))
    RATIONALE: select ferric minerals ('hematite band')

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
    wv = [800,860,984]
    return(generic_func(data, wv, func = cf.bd860_func, **kwargs))

def bd920(data, **kwargs):
    """
    NAME: BD920
    PARAMETER: 0.92 micron band depth
    FORMULATION *: 1 - ( R920 / (a*R800+b*R984) )
    RATIONALE: select ferric minerals ('Pseudo BDI1000 VIS')

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
    wv = [800,920,984]
    return(generic_func(data, wv, func = cf.bd920_func, **kwargs))


#@@TODO rpeak1
def rpeak1(data, **kwargs):
    """
    NAME: BDI1000VIS
    PARAMETER: 1 micron integrated band depth; VIS wavelengths
    FORMULATION *: divide R830, R860, R890, R915 by RPEAK1 then
      integrate over (1 -  normalized radiances)
    RATIONALE: crystalline Fe+2 or Fe+3 minerals
    """
    raise NotImplementedError

#@@TODO bdi1000VIS
def bdi1000VIS(data, **kwargs):
    """
    NAME: BDI1000VIS
    PARAMETER: 1 micron integrated band depth; VIS wavelengths
    FORMULATION *: divide R830, R860, R890, R915 by RPEAK1 then
      integrate over (1 -  normalized radiances)
    RATIONALE: crystalline Fe+2 or Fe+3 minerals
    """
    raise NotImplementedError

#@@TODO bdi1000IR
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

def ira(data, **kwargs):
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
    raise NotImplementedError


def hcp_index(data, **kwargs):
    """
    NAME: HCPXINDEX
    PARAMETER: pyroxene index
    FORMULATION *: 100 * ((R1470 - R1080)/(R1470 + R1080)) *
                          ((R1470 - R2067)/(R1470+R2067))
    RATIONALE: pyroxene is strongly +; favors high-Ca pyroxene
    Algorithm differs from published - coded as per CAT

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
    wv = [1080,1470,2067]
    return(generic_func(data, wv, func = cf.hcp_index_func, **kwargs))


def lcp_index(data, **kwargs):
    """
     NAME: LCPINDEX
    PARAMETER: pyroxene index
    FORMULATION *: 100 * ((R1330 - R1080)/(R1330 + R1080)) *
                          ((R1330 - R1815)/(R1330+R1815))
    RATIONALE: pyroxene is strongly +; favors low-Ca pyroxene
    Algorithm differs from published - coded as per CAT

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
    wv = [1080,1330,1815]
    return(generic_func(data, wv, func = cf.lcp_index_func, **kwargs))


#@@TODO var
def var(data, **kwargs):
    """
    NAME: VAR
    PARAMETER: spectral variance
    FORMULATION *: find variance from a line fit from 1 - 2.3 micron
      by summing in quadrature over the intervening wavelengths
    RATIONALE: Ol & Px will have high values; Type 2 areas will have
      low values
    """
    raise NotImplementedError

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
    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array
    Returns
    -------
     : ndarray
       the processed ndarray

    """
    wv = [1815,2530]
    return(generic_func(data, wv, func = cf.islope1_func, **kwargs))

def bd1435(data, **kwargs):
    """
    NAME: BD1435
    PARAMETER: 1.435 micron band depth
    FORMULATION *: 1 - ( R1430 / (a*R1370+b*R1470) )
    RATIONALE: CO2 surface ice

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
    wv = [1370,1430,1470]
    return(generic_func(data, wv, func = cf.bd1435_func, **kwargs))


def bd1500(data, **kwargs):
    """
    NAME: BD1500
    PARAMETER: 1.5 micron band depth
    FORMULATION *: 1.0 - ((R1558 + R1505)/(R1808 + R1367))
    RATIONALE: H2O surface ice
    Algorithm differs from published - coded as per CAT (reduced instrument noise)

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
    wv = [1367,1505,1558,1808]
    return(generic_func(data, wv, func = cf.bd1500_func, **kwargs))


def icer1(data, **kwargs):
    """
    NAME: ICER1
    PARAMETER: 1.5 micron and 1.43 micron band ratio
    FORMULATION *: R1510 / R1430
    RATIONALE: CO2, H20 ice mixtures

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
    wv = [1430,1510]
    return(generic_func(data, wv, func = cf.icer1_func, **kwargs))


def bd1750(data, **kwargs):
    """
    NAME: BD1750
    PARAMETER: 1.75 micron band depth
    FORMULATION *: 1 - ( R1750 / (a*R1660+b*R1815) )
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
    wv = [1557,1750,1815]
    return(generic_func(data, wv, func = cf.bd1750_func, **kwargs))


def bd1900(data, **kwargs):
    """
    NAME: BD1900
    PARAMETER: 1.9 micron band depth
    FORMULATION *: 1.0 - ((R1972 + R1927)/(R2006 + R1874))
    RATIONALE: H2O, chemically bound or adsorbed
    Algorithm differs from published - coded as per CAT (reduced instrument noise)

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
    wv = [1874,1927,1973,2006]
    return(generic_func(data, wv, func = cf.bd1900_func, **kwargs))

#@@TODO bdi2000
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


def bd2100(data, **kwargs):
    """
    NAME: BD2100
    PARAMETER: 2.1 micron band depth
    FORMULATION *: 1 - ( ((R2120+R2140)*0.5) / (a*R1930+b*R2250) )
    RATIONALE: monohydrated minerals

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
    wv = [1930,2120,2140,2250]
    return(generic_func(data, wv, func = cf.bd2100_func, **kwargs))


def bd2210(data, **kwargs):
    """
    NAME: BD2210
    PARAMETER: 2.21 micron band depth
    FORMULATION *: 1 - ( R2210 / (a*R2140+b*R2250) )
    RATIONALE: Al-OH minerals: monohydrated minerals

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
    wv = [2140,2210,2250]
    return(generic_func(data, wv, func = cf.bd2210_func, **kwargs))

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
    wv = [2250,2290,2350]
    return(generic_func(data, wv, func = cf.bd2290_func, **kwargs))


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
    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array
    Returns
    -------
     : ndarray
       the processed ndarray

    """
    wv = [1815, 2120, 2170, 2210, 2290, 2320, 2330, 2530]
    return(generic_func(data, wv, func = cf.d2300_func, **kwargs))


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
    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array
    Returns
    -------
     : ndarray
       the processed ndarray

    """
    wv = [2100,2400,2290]
    return(generic_func(data, wv, func = cf.sindex_func, **kwargs))

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
    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array
    Returns
    -------
     : ndarray
       the processed ndarray

    """
    wv = [2530,2600]
    return(generic_func(data, wv, func = cf.icer2_func, **kwargs))

def bdcarb(data, **kwargs):
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
    return(generic_func(data, wv, func = cf.cindex_func, **kwargs))
