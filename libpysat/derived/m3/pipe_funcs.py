from math import e
import numpy as np

# Generic Function for all RXXX formulas
def reflectance_func(bands):
    return bands[0]

def uvvis_func(bands):
    R419, R749 = bands

    return R419 / R749

def visuv_func(bands):
    R419, R749 = bands

    return R749 / R419

def visnir_func(bands):
    R699, R1579 = bands

    return R699 / R1579

def r950_750_func(bands):
    R749, R949 = bands

    return R949 / R749

# Generic Function for all BDXXX formulas
def bd_func(bands, wvs):
    return 1 - (bands[1] / ((bands[2] - bands[0]) / (wvs[2] - wvs[0]) * (wvs[1] - wvs[0]) + bands[0]))

def bdi_func(bands, wvs=[0,0]):
    lower_array, band_array, upper_array = bands
    lower_bound, y, upper_bound = wvs

    return band_array / (((upper_array - lower_array)/ \
           (upper_bound - lower_bound)) * (y - lower_bound) + lower_array)

def oneum_min_slope_func(bands):
    R890, R1349 = np.min(bands), np.max(bands)
    m = (R1349 - R890) / (1349 - 890)
    x = np.array(bands) - R890
    b = R890

    return (m * x) + b

def oneum_min_func(bands):
    R890, R1349 = np.min(bands), np.max(bands)
    max_band = (1 - (bands / oneum_min_slope_func(bands)))
    max_band = np.max(max_band, axis=0)

    return max_band

def oneum_sym_func(bands):

    def oneum_fwhm_func():
        Rc = oneum_min_slope_func(bands)
        long = np.max((0.5 * 1 - (bands / Rc)), axis=0)
        short = np.min((0.5 * 1 - (bands / Rc)), axis=0)

        return long, short

    long, short = oneum_fwhm_func()
    oneum_min = oneum_min_func(bands)
    a = oneum_min - short
    b = long - oneum_min

    return b/a

def bd1umratio_func(bands):
    R699, R929, R989, R1579 = bands

    BD930 = 1 - ((R929) / (((R1579 - R699)/(1579 - 699)) * (929-699) + R699))
    BD990 = 1 - ((R989) / (((R1579 - R699)/(1579 - 699)) * (989-699) + R699))
    return BD930 / BD990

def twoum_ratio_func(bands):
    R1578, R2538 = bands

    return R1578 / R2538

def bd2umratio_func(bands):
    R1578, R1898, R2298, R2578 = bands

    a = 1 - ((R1898) / (((R2578 - R1578)/(2578 - 1578)) * (1898-1578) + R1578))
    b = 1 - ((R2298) / (((R2578 - R1578)/(2578 - 1578)) * (2298-1578) + R1578))
    return a/b

def thermal_ratio_func(bands):
    R2538, R2978 = bands

    return R2538 / R2978

def bd3000_func(bands):
    R1578, R2538, R2978 = bands

    return 1 - ((R2978) / (((R2538 - R1578) / (2538 - 1578)) * (2978 - 1578) + R1578))

def visslope_func(bands):
    R419, R749 = bands

    return (R749 - R419) / (749-419)

def oneum_slope_func(bands):
    R699, R1579 = bands

    return (R1579 - R699) / (1579 - 699)

def olindex_func(bands):
    R650, R860, R1047, R1230, R1750 = bands

    return 10 * (0.1 * ((((R1750 - R650) / (1750 - 650)) * (860 - 650) + R650) / R860)) + \
            (0.5 * ((((R1750 - R650) / (1750 - 650)) * (1047 - 650) + R650) / R1047)) + \
            (0.25 * ((((R1750 - R650) / (1230 - 650)) * (860 - 650) + R650) / R1230))

def twoum_slope_func(bands):
    R1578, R2538 = bands

    return (R2538 - R1578) / (2538 - 1578)

def thermal_slope_func(bands):
    R2538, R2978 = bands

    return (R2978 - R2538) / (2978 - 2538)

def nbd1400_func(bands):
    R1348, R1408, R1428, R1448, R1578 = bands

    RC = (R1348 + R1578) / 2
    LC = (R1428 + R1448) / 2
    BB = R1408
    return 1 - 2 * (BB / (RC + LC))

def nbd1480_func(bands):
    R1428, R1448, R1488, R1508, R1528 = bands

    RC = (R1428 + R1448) / 2
    LC = (R1508 + R1528) / 2
    BB = R1488
    return 1 - 2 * (BB / (RC + LC))

def nbd2300_func(bands):
    R2218, R2258, R2378, R2418, R2298, R2338 = bands

    RC = (R2218 + R2258) / 2
    LC = (R2378 + R2418) / 2
    BB = (R2298 + R2338) / 2
    return 1 - 2 * (BB / (RC + LC))

def nbd2700_func(bands):
    R2578, R2618, R2658, R2698, R2738 = bands

    RC = (R2578 + R2618 + R2658) / 3
    BB = (R2698 + R2738) / 2
    return 1 - (BB / RC)

def nbd2850_func(bands):
    R2538, R2578, R2618, R2817, R2857, R2897 = bands

    RC = (R2538 + R2578 + R2618) / 3
    BB = (R2817 + R2857 + R2897) / 3
    return 1 - (BB / RC)

def hlnd_isfeo_func(bands):
    R749, R889 = bands

    return e**((1.82 - (R749 / R889)) / 0.057)
