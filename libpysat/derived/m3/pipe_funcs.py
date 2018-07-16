from math import e

def bd620_func(bands):
    R419, R619, R749 = bands

    return 1 - ((R619) / (((R749 - R419) / (749 - 419)) * (619 - 419) + R419))

def bdi_func(bands, wvs=[0,0]):
    lower_array, band_array, upper_array = bands
    lower_bound, y, upper_bound = wvs
    return band_array / (((upper_array - lower_array)/\
           (upper_bound - lower_bound)) * (y - lower_bound) + lower_array)

def bd1900_func(bands):
    R1408, R1898, R2498 = bands

    return 1 - ((R1898) / (((R2498 - R1408) / (2498 - 1408)) * (1898 - 1408) + R1408))

def bd2300_func(bands):
    R1578, R2298, R2578 = bands

    return 1 - ((R2298) / (((R2578 - R1578) / (2578 - 1578)) * (2298 - 1578) + R1578))

def h2o1_func(bands):
    R1578, R2538, R2978 = bands

    return 1 - ((R2978) / (((R2538 - R1578) / (2538 - 1578)) * (2978 - 1578) + R1578))

def iralbedo_func(bands):
    R1579 = bands[0]

    return R1579

def mafic_abs_func(bands):
    R749, R949 = bands

    return R949 / R749

def omh_func(bands):
    R749, R889 = bands

    return e**((1.82 - (R749 / R889)) / 0.057)

def olindex_func(bands):
    R650, R860, R1047, R1230, R1750 = bands

    return 10 * (0.1 * ((((R1750 - R650) / (1750 - 650)) * (860 - 650) + R650) / R860)) + \
            (0.5 * ((((R1750 - R650) / (1750 - 650)) * (1047 - 650) + R650) / R1047)) + \
            (0.25 * ((((R1750 - R650) / (1230 - 650)) * (860 - 650) + R650) / R1230))

def oneum_slope_func(bands):
    R699, R1579 = bands

    return (R1579 - R699) / (1579 - 699)

def reflectance_func(bands):
    return bands[0]

def thermal_ratio_func(bands):
    R2538, R2978 = bands

    return R2538 / R2978

def thermal_slope_func(bands):
    R2538, R2978 = bands

    return (R2978 - R2538) / (2978 - 2538)

def twoum_ratio_func(bands):
    R1578, R2538 = bands

    return R1578 / R2538

def twoum_slope_func(bands):
    R1578, R2538 = bands

    return (R2538 - R1578) / (2538 - 1578)

def uvvis_func(bands):
    R419, R749 = bands

    return R419 / R749

def visslope_func(bands):
    R419, R749 = bands

    return (R749 - R419) / (749-419)

def visuv_func(bands):
    R419, R749 = bands

    return R749 / R419

def visnir_func(bands):
    R699, R1579 = bands

    return R699 / R1579
