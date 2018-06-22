from numpy import sqrt
from ..utils import compute_b_a

def rockdust1_func(bands, _):
    R770, = bands
    return R770

def rockdust2_func(bands, _):
    return bands[1] / bands[0]

def rockdust2_inverse_func(bands, _):
    return bands[0] / bands[1]

def bd_func1(bands, wv):
    b, a = compute_b_a(wv)
    return 1.0 - (bands[1] / ((a * bands[2]) + (b * bands[0])))

def bd_func2(bands, wv):
    b, a = compute_b_a(wv)
    return 1.0 - (bands[1] / ((a * bands[0]) + (b * bands[2])))

def avg_bd_func(bands, wv):
    b, a = compute_b_a(wv)
    return 1.0 - (bands[1] / ((a * bands[0]) + (b * bands[2])))

def sh_func(bands, wv):
    b, a = compute_b_a(wv)
    return 1.0 - (((a * bands[0]) + (b * bands[2])) / bands[1])

#@@TODO rpeak1
#@@TODO bdi1000vis

def ira_func(bands,_):
    return bands

def olivine_index_func(bands, _):
    b1080, b1210, b1330, b1470, b1695 = bands

    return ((b1695 / (0.1*b1080 + 0.1*b1210 + .4*b1330 + 0.4*b1470))-1)

#@@TODO olivine_index2

def hcp_index_func(bands,_):
    b1080, b1470, b2067 = bands

    return (100 * ((b1470 - b1080) / (b1470+b1080)) * ((b1470 - b2067)/(b1470+b2067)))

def index1_func(bands, _):
    return (100 * ((bands[1] - bands[0]) / (bands[1] + bands[0])) * \
                  ((bands[1] - bands[2]) / (bands[1] + bands[2])))

#@@TODO var

def islope1_func(bands, wv):

    return (bands[0] - bands[1])/(wv[1] - wv[0])

def bd1500_func(bands, _):
    b1367, b1505, b1558, b1808 = bands
    return 1.0 - ((b1558 + b1505) / (b1808 + b1367))

def bd1900_func(bands, _):
    b1875, b1930, b1985, b2067 = bands
    # Is this the correct calculation for a, and b here?
    # Going off of the code present in the bd2100_func
    b = (((1985 + 1930) / 2) - 1875) / (2067 - 1875)
    a = 1 - b
    return (1.0 - (((b1985 + b1930) / 2) / (b * 2067 + a * 1875)))

def bd1900r_func(bands, _):
    R1908, R1914, R1921, R1928, R1934, R1941, \
    R1862, R1869, R1875, R2112, R2120, R2126 = bands

    numerator = (R1908 + R1914 + R1921 + R1928 + R1934 + R1941)
    denominator = (R1862 + R1869 + R1875 + R2112 + R2120 + R2126)

    return 1 - (numerator / denominator)

#@@TODO bdi2000

def bd2100_func(bands, wv):
    b1930, b2120, b2130, b2250 = bands
    wv = [wv[0], ((wv[1] + wv[2] )/2), wv[3]]
    bands = [bands[0], ((bands[1] + bands[2]) * .5), bands[3]]

    return bd_func2(bands, wv)

def doub2200h_func(bands, _):
    b2172, b2205, b2258, b2311 = bands

    return (1 - ((b2205 + b2258) / (b2172 + b2311)))

def d2300_func(bands, _):
    b1815, b2120, b2170, b2210, b2290, b2320, b2330, b2530 = bands

    slope = (b2530 - b1815) / (2530 - 1815)
    cr2290 = b1815 + slope * (2290 - 1815)
    cr2320 = b1815 + slope * (2320 - 1815)
    cr2330 = b1815 + slope * (2330 - 1815)
    cr2120 = b1815 + slope * (2120 - 1815)
    cr2170 = b1815 + slope * (2170 - 1815)
    cr2210 = b1815 + slope * (2210 - 1815)

    return (1.0 - (((b2290 / cr2290) + (b2320 / cr2320) + (b2330 / cr2330)) /
                   ((b2120 / cr2120) + (b2170 / cr2170) + (b2210 / cr2210))))

def sindex_func(bands, _):
    b2100, b2400, b2290 = bands
    return (1.0 - ((b2100 + b2400) / (2 * b2290)))

'''def bdcarb_func(bands, _ ):
    b2230, b2330, b2390, b2530, b2600 = bands
    a = (((2330 + 2120)*.5) - 2230 / (2390-2230))
    b = 1.0 - a
    c = (((2530 + 2120)*.5 - 2390) / (2600 - 2390))
    d = 1.0 - c
    return (1 - sqrt(b2330 / ((b * b2330) + (a*b2390)))*(b2530/((d*b2230)+(c*b2600))))

def bd3000_func(bands, _ ) :
    b2210, b2530, b3000 = bands
    return ( 1 - (b3000 / (b2530 * (b2530 / b2210))))


def bd3100_func(bands, _ ) :
    b3000, b3120, b3250 = bands
    a = ((3120 - 3000) / (3250 - 3000))
    b = 1.0 - a
    return (1.0 - (b3120/((b*b3000)+(a*b3250))))

def bd3200_func(bands, _ ):
    b3250,b3320,b3390 = bands
    a = (3320 - 3250)/ (3390 - 3250)
    b = 1.0 - a
    return (1.0 - (b3320/((b*b3250)+(a*b3390))))

def bd3400_func(bands, _ ):
    b3250, b3390, b3500, b3630 = bands
    c = (((3390 + 3500)*.5)-3250)/(3630-3250)
    d = 1.0 - c
    return ( 1.0 - (((b3390 + b3500)*.5)/((d*b3250)+(c*b3630))))


def cindex_func(bands, _):
    b3630, b3750,b3950 = bands
    return (((b3750+((b3750-b3630)/((3750-3630)*(3950-3750)))))/ b3950 -1)'''
