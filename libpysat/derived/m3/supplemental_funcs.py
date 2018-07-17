import numpy as np

def curv_func(bands):
    R749, R909, R1109 = bands

    return (R749 + R1109) / (2 * R909)


def fe_est_func(bands):
    R749, R949 = bands

    y0 = 1.19
    x0 = 0.08

    return (17.427 * ( -1 * (np.arctan(((R949 / R749) - y0) / (R749 - x0))))) - 7.565

def fe_mare_est_func(bands):
    R749, R949 = bands

    return -137.97 * ((R749 * 0.9834)+((R949 / R749)*0.1813)) + 57.46

def luceyc_amat_func(bands):
    R749, R949 = bands

    return (((R749-0.01)**2)+((R949/R749)-1.26)**2)**(1/2)

def luceyc_omat_func(bands):
    R749, R949 = bands
    return (((R749-0.08)**2)+((R949/R749)-1.19)**2)**(1/2)

def mare_omat_func(bands):
    R749, R949 = bands
    return (R749 * 0.1813) - ((R949/R749)*0.9834)

def tilt_func(bands):
    R909, R1009 = bands
    return R909 - R1009
