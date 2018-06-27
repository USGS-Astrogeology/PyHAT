import numpy as np
import warnings
from .import pipe_funcs as pf
from ..utils import generic_func, warn_m3

@warn_m3
def r750(data, **kwargs):
    """
    Name: R750
    Parameter: 0.75 um reflectance
    Formulation:
    R750 = R749
    Rationale: Reference I/F
    Bands: R749

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
    wavelengths = [749]
    return generic_func(data, wavelengths, func = pf.reflectance_func, **kwargs)

@warn_m3
def uvvis(data, **kwargs):
    """
    Name: UVVIS
    Parameter: Ultraviolet Visible Ratio
    Formulation:
    VISUV = R419/R749
    Rationale: UV-Visible Spectral Ratio
    Bands: R419, R749

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
    wavelengths = [419, 749]
    return generic_func(data, wavelengths, func = pf.uvvis_func, **kwargs)

@warn_m3
def visuv(data, **kwargs):
    """
    Name: VISUV
    Parameter: Ultraviolet Visible Ratio
    Formulation:
    VISUV = R749/R419
    Rationale: Visible-UV Spectral Ratio
    Bands: R419, R749

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
    wavelengths = [419, 749]
    return generic_func(data, wavelengths, func = pf.visuv_func, **kwargs)

@warn_m3
def visnir(data, **kwargs):
    """
    Name: VISNIR
    Parameter: Visible-nearIR Ratio
    Formulation:
    VISUV = R699/R1579
    Rationale: Optical Maturity and mare-highland
    Bands: R699, R1579

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
    wavelengths = [699, 1579]
    return generic_func(data, wavelengths, func = pf.visnir_func, **kwargs)

@warn_m3
def r950_750(data, **kwargs):
    """
    Name: R950_750
    Parameter: Ratio of 950nm to 750nm, mafic absorption
    Formulation:
    VISUV = R949/R749
    Rationale: Quick look at mafic absorption
    Bands: R749, R949

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
    wavelengths = [749, 950]
    return generic_func(data, wavelengths, func = pf.r950_750_func, **kwargs)

@warn_m3
def bd620(data, **kwargs):
    """
    Name: BD620
    Parameter: Band Depth at 620 nm
    Formulation:
    Numerator = R619
    Denominator = ((R749 - R419) / (749 - 419)) * (619 - 419) + R419
    BD620 = 1 - [Numerator/Denominator]
    Rationale: Possible Ti or Impact Melt
    Bands: R419, R619, R749

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
    wavelengths = [419, 619, 749]
    return generic_func(data, wavelengths, func = pf.bd_func, pass_wvs=True, **kwargs)

@warn_m3
def bd950(data, **kwargs):
    def bd620(data, **kwargs):
        """
        Name: BD950
        Parameter: Band Depth at 950 nm
        Formulation:
        Numerator = R949
        Denominator = ((R1579 - R749) / (1579 - 749)) * (949 - 749) + R749
        BD620 = 1 - [Numerator/Denominator]
        Rationale: OPX Comparison with Kaguya
        Bands: R749, R949, R1579

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
    wavelengths = [749, 949, 1579]
    return generic_func(data, wavelengths, func = pf.bd_func, pass_wvs=True, **kwargs)

@warn_m3
def bd1050(data, **kwargs):
    """
    Name: BD1050
    Parameter: Band Depth at 1050 nm
    Formulation:
    Numerator = R1049
    Denominator = ((R1579 - R749) / (1579 - 749)) * (1049 - 749) + R749
    BD620 = 1 - [Numerator/Denominator]
    Rationale: OLV Comparison with Kaguya
    Bands: R749, R1049, R1579

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
    wavelengths = [749, 1049, 1579]
    return generic_func(data, wavelengths, func = pf.bd_func, pass_wvs=True, **kwargs)

@warn_m3
def bd1250(data, **kwargs):
    """
    Name: BD1250
    Parameter: Band Depth at 1250 nm
    Formulation:
    Numerator = R1249
    Denominator = ((R1579 - R749) / (1579 - 749)) * (1249 - 749) + R749
    BD620 = 1 - [Numerator/Denominator]
    Rationale: PLAG Comparison with Kaguya
    Bands: R749, R1249, R1579

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
    wavelengths = [749, 1249, 1579]
    return generic_func(data, wavelengths, func = pf.bd_func, pass_wvs=True, **kwargs)

@warn_m3
def r1580(data, **kwargs):
    """
    Name: R1580
    Parameter: 1.6 um reflectance
    Formulation:
    R1580 = R1579
    Rationale: IR Albedo
    Bands: R1579

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
    wavelengths = [1579]
    return generic_func(data, wavelengths, func = pf.reflectance_func, **kwargs)

def calc_bdi_band(data, iteration, initial_band, step, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    iteration : int
                Number of steps to add to the new band calculation

    initial_band : int
                   Initial band to use to calculate the new band

    step : int
           Length between bands to calculate

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    y = initial_band + (step * iteration)
    wv_array = data.wavelengths
    vals = np.abs(data.wavelengths-y)
    minidx = np.argmin(vals)
    wavelengths = [wv_array[minidx - 3], y, wv_array[minidx + 3]]
    wvlims = [wavelengths[0], y, wavelengths[-1]]
    return generic_func(data, wavelengths, func=pf.bdi_func, pass_wvs=wvlims, **kwargs)

def bdi_generic(data, upper_limit, initial_band, step):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    upper_limit : int
                  Upper limit on the number of wavelengths to be used

    initial_band : int
                   The band to use as a starting point to extract the other
                   0 to upper_limit bands
    step : int
           The step size inbetween the 0 to upper limit bands

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    limit = range(0, upper_limit)
    band_list = [1 - calc_bdi_band(data, i, initial_band, step) for i in limit]

    return np.sum(band_list, axis = 0)

@warn_m3
def bdi1000(data, **kwargs):
    """
    Name: BDI1000
    Parameter: 1 um integrated band depth
    Formulation:
    BDI1000 = Sum with n values 0-26: (1 - [R(789 + 20n) / Rc(789 + 20n)])
    Rationale: Fe Mineralogy
    Bands: R789 - R1308 (in steps of 20)

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
    return bdi_generic(data, 27, 789, 20)

# TODO: Implment This
# max( m(R - lower) + lower)
@warn_m3
def oneum_min(data, **kwargs):
    """
    Name: 1um_Min
    Parameter: 1 um band center
    Formulation:
    Rl = R Lambda
    1um_Min = Max of [1 - (R_lambda / Rc_lambda)] with wavlenghts between 890-1349 nm
    Rationale: Fe Mineralogy
    Bands: R890 - R1349

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
    wavelengths = [890, 1349]
    return generic_func(data, wavelengths, func=pf.oneum_min_func, **kwargs)

# TODO: Implement This
@warn_m3
def oneum_fwhm(data, **kwargs):
    """
    Name: 1um_FWHM
    Parameter: 1 um band width
    Formulation:
    1um_FWHM = 0.5 * 1 - [R(1um_Min) / Rc(1um_Min)]
    Rationale: Fe Mineralogy
    Bands: 1um_Min Band

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
    wavelengths = [890, 1349]
    return generic_func(data, wavelengths, func=pf.oneum_fwhm_func, **kwargs)

# TODO: Implement This
@warn_m3
def oneum_sym(data, **kwargs):
    """
    Name: 1um_Sym
    Parameter: 1 um symmetry
    Formulation:
    a = 1um_min - short wavelength point found in 1um_FWHM
    b = long wavelength point found in 1um_FWHM - 1um_Min
    1um_Sym = b/a
    Rationale: Numbers greater than 1 may be enriched in olivine
    Bands: R(1um_Min), R(1um_FWHM)

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
    wavelengths = [890, 1349]
    return generic_func(data, wavelengths, func=pf.oneum_sym_func, **kwargs)

@warn_m3
def bd1umratio(data, **kwargs):
    """
    Name: BD1um Ratio
    Parameter: BD930 / BD990
    Formulation:
    BD930 = 1 - ((R929) / (((R1579 - R699)/(1579 - 699)) * (929-699) + R699))
    BD990 = 1 - ((R989) / (((R1579 - R699)/(1579 - 699)) * (989-699) + R699))
    BDRatio = BD930 / BD990
    Rationale: Possible Ti or impact melt
    Bands: R699, R929, R989, R1579

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
    wavelengths = [699, 929, 989, 1579]
    return generic_func(data, wavelengths, func = pf.bd1umratio_func, **kwargs)

@warn_m3
def twoum_ratio(data, **kwargs):
    """
    Name: 2um_Ratio
    Parameter: 2 um ratio
    Formulation:
    2um_Ratio = R1578/R2538
    Rationale: N/A
    Bands: R1578, R2538

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
    wavelengths = [1578, 2538]
    return generic_func(data, wavelengths, func = pf.twoum_ratio_func, **kwargs)

# TODO: Check if this works with bdi_generic
@warn_m3
def bdi2000(data, **kwargs):
    """
    Name: BDI2000
    Parameter: 2 um integrated band depth
    Formulation:
    BDI1000 = Sum with n values 0-21: (1 - [R(1658 + 40n) / Rc2(1658 + 40n)])
    Rationale: Fe Mineralogy
    Bands: R1658 - R2498 (in steps of 40)

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
    return bdi_generic(data, 22, 1658, 40)

@warn_m3
def bd2umratio(data, **kwargs):
    """
    Name: BD2um Ratio
    Parameter:2um band depth ratio
    Formulation:
    a = 1 - ((R1898) / (((R2578 - R1578)/(2578 - 1578)) * (1898-1578) + R1578))
    b = 1 - ((R2298) / (((R2578 - R1578)/(2578 - 1578)) * (2298-1578) + R1578))
    BD2um_ratio = a/b
    Rationale: Possible Ti or impact melt
    Bands: R1578, R1898,R2298, R2578

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
    wavelengths = [1578, 1898, 2298, 2578]
    return generic_func(data, wavelengths, func = pf.bd2umratio_func, **kwargs)

@warn_m3
def thermal_ratio(data, **kwargs):
    """
    Name: Thermal_Ratio
    Parameter: N/A
    Formulation:
    Thermal_Ratio = R2538/2978
    Rationale: N/A
    Bands: R2538, R2978

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
    wavelengths = [2538, 2978]
    return generic_func(data, wavelengths, func = pf.thermal_ratio_func, **kwargs)

@warn_m3
def bd3000(data, **kwargs):
    """
    Name: BD3000
    Parameter: 3 um band depth using 2um continuum
    Formulation:
    Numerator = R2978
    Denominator = ((R2538 - R1578) / (2538 - 1578)) * (2978 - 1578) + R1578
    BD620 = 1 - [Numerator/Denominator]
    Rationale: H2O
    Bands: R1578, R2538, R2978

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
    wavelengths = [1578, 2538, 2978]
    return generic_func(data, wavelengths, func = pf.bd3000_func, **kwargs)

def r540(data, **kwargs):
    """
    Name: R540
    Parameter: 0.55 um reflectance
    Formulation:
    R750 = R539
    Rationale: Reference I/F
    Bands: R539

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
    wavelengths = [539]
    return generic_func(data, wavelengths, func = pf.reflectance_func, **kwargs)

def visslope(data, **kwargs):
    """
    Name: Vis_Slope
    Parameter: UV-visible continuum slope
    Formulation:
    Vis_Slope = (R749 - R419) / (749 - 419)
    Rationale: UV-Vis Slope (%/nm)
    Bands: R419, R749

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
    wavelengths = [419, 749]
    return generic_func(data, wavelengths, func = pf.visslope_func, **kwargs)

def oneum_slope(data, **kwargs):
    """
    Name: 1um_Slope
    Parameter: continuum slope between 0.70 and 1.6 um
    Formulation:
    1um_Slope = (R1579 - R699) / (1579 - 699)
    Rationale: Vis-NIR Slope (%/nm)
    Bands: R699, R1579

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
    wavelengths = [699, 1579]
    return generic_func(data, wavelengths, func = pf.oneum_slope_func, **kwargs)

def r2780(data, **kwargs):
    """
    Name: R2780
    Parameter: 2.8 um reflectance
    Formulation:
    R750 = R2778
    Rationale: Reference I/F
    Bands: R2778

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
    wavelengths = [2778]
    return generic_func(data, wavelengths, func = pf.reflectance_func, **kwargs)

def olindex(data, **kwargs):
    """
    Name: OLINDEX
    Parameter: Olivine Index
    Formulation:
    slope = (R1750 - R650) / (1750 - 650)
    a = 0.1 * [(slope * (860-650) + R650) / R860]
    b = 0.5 * [(slope * (1047-650) + R650) / R1047]
    c = 0.25 * [(slope * (1230-650) + R650) / R1230]
    OLINDEX = a + b + c
    Rationale: Olivine will be strongly positive
    Bands: R650, R860, R1047, R1230, R1750

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
    wavelengths = [650, 860, 1047, 1230, 1750]
    return generic_func(data, wavelengths, func = pf.olindex_func, **kwargs)

def bd1900(data, **kwargs):
    """
    Name: BD1900
    Parameter: Band Depth at 1900 nm: low Ca pyroxene index
    Formulation:
    Numerator = R1898
    Denominator = ((R2498 - R1408) / (2498 - 1408)) * (1898 - 1408) + R1408
    BD620 = 1 - [Numerator/Denominator]
    Rationale: pyroxene will be positive; favors LCP
    Bands: R1408, R1898, R2498

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
    wavelengths = [1408, 1898, 2498]
    return generic_func(data, wavelengths, func = pf.bd_func, pass_wvs=True, **kwargs)

def bd2300(data, **kwargs):
    """
    Name: BD2300
    Parameter: Band Depth at 2300 nm: low Ca pyroxene index
    Formulation:
    Numerator = R2298
    Denominator = ((R2578 - R1578) / (2578 - 1578)) * (2298 - 1578) + R1578
    BD620 = 1 - [Numerator/Denominator]
    Rationale: pyroxene will be positive; favors LCP
    Bands: R1578, R2298, R2578

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
    wavelengths = [1578, 2298, 2578]
    return generic_func(data, wavelengths, func = pf.bd_func, pass_wvs=True, **kwargs)

def twoum_slope(data, **kwargs):
    """
    Name: 2um_Slope
    Parameter: continuum slope between 1.6 and 2.5 um
    Formulation:
    21um_Slope = (R2538 - R1578) / (2538 - 1578)
    Rationale: NIR Slope
    Bands: R1578, R2538

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
    wavelengths = [1578, 2538]
    return generic_func(data, wavelengths, func = pf.twoum_slope_func, **kwargs)

def thermal_slope(data, **kwargs):
    """
    Name: Thermal_Slope
    Parameter: N/A
    Formulation:
    21um_Slope = (R2978 - R2538) / (2978 - 2538)
    Rationale: Thermal Slope (% / nm)
    Bands: R1578, R2538

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
    wavelengths = [2538, 2978]
    return generic_func(data, wavelengths, func = pf.thermal_slope_func, **kwargs)

def nbd1400(data, **kwargs):
    """
    Name: NBD1400
    Parameter:1.4um OH Band
    Formulation:
    RC = (R1348 + R1578) / 2
    LC = (R1428 + R1448) / 2
    BB = R1408
    NBD1400 = 1 - 2 * (BB / (RC + LC))
    Rationale: H2O
    Bands: R1348, R1428, R1448, R1578

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
    wavelengths = [1348, 1408, 1428, 1448, 1578]
    return generic_func(data, wavelengths, func = pf.nbd1400_func, **kwargs)

def nbd1480(data, **kwargs):
    """
    Name: NBD1480
    Parameter:1.48um OH Band
    Formulation:
    RC = (R1428 + R1448) / 2
    LC = (R1508 + R1528) / 2
    BB = R1488
    NBD1400 = 1 - 2 * (BB / (RC + LC))
    Rationale: H2O
    Bands: R1428, R1448, R1488, R1508, R1528

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
    wavelengths = [1428, 1448, 1488, 1508, 1528]
    return generic_func(data, wavelengths, func = pf.nbd1480_func, **kwargs)

def nbd2300(data, **kwargs):
    """
    Name: NBD2300
    Parameter: 2.3um OH Band
    Formulation:
    RC = (R2218 + R2258) / 2
    LC = (R2378 + R2418) / 2
    BB = (R2298 + R2338) / 2
    NBD2300 = 1 - 2 * (BB / (RC + LC))
    Rationale: H2O
    Bands: R2218, R2258, R2378, R2418, R2298, R2338

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
    wavelengths = [2218, 2258, 2378, 2418, 2298, 2338]
    return generic_func(data, wavelengths, func = pf.nbd2300_func, **kwargs)

def nbd2700(data, **kwargs):
    """
    Name: HBD2700
    Parameter:2.7um OH Band
    Formulation:
    RC = (R2578 + R2618 + R2658) / 3
    BB = (R2698 + R2738) / 2
    HBD2700 = 1 - (BB / RC)
    Rationale: H2O
    Bands: R2578, R2618, R2658, R2698, R2738

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
    wavelengths = [2578, 2618, 2658, 2698, 2738]
    return generic_func(data, wavelengths, func = pf.nbd2700_func, **kwargs)

def nbd2850(data, **kwargs):
    """
    Name: HBD2850
    Parameter:3um Ice Band
    Formulation:
    RC = (R2538 + R2578 + R2618) / 3
    BB = (R2817 + R2857 + R2897) / 3
    HBD2700 = 1 - (BB / RC)
    Rationale: Ice
    Bands: R2538, R2578, R2618, R2817, R2857, R2897

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
    wavelengths = [2538, 2578, 2618, 2817, 2857, 2897]
    return generic_func(data, wavelengths, func = pf.nbd2850_func, **kwargs)

def hlnd_isfeo(data, **kwargs):
    """
    Name: Hlnd_IsFeO
    Parameter: Optical Maturity Highlands
    Formulation:
    IsFeo = e ** [(1.82 - (R749/R889)) / 0.057]
    Rationale: Based on Fischer
    Bands: R1578, R2538

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
    wavelengths = [749, 889]
    return generic_func(data, wavelengths, func = pf.hlnd_isfeo_func, **kwargs)
