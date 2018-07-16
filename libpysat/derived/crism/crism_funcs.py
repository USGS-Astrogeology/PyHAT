from numpy import sqrt



def rockdust1_func(bands):
    b770, = bands
    return b770

def rockdust2_func(bands):
    b440,b770 = bands
    return b770 / b440

'''def bd530_func(bands, _):
    b440, b530, b709 = bands

    b = (530 - 440) / (709 - 440)
    a = 1.0 - b
    return 1.0 - (b530/((a*b709)+(b*b440)))

def sh600_func(bands, _):
    b533, b600, b710 = bands

    a = (600 - 533) / (710 - 533)
    b = 1.0 - a
    return 1.0 - (((b * b533)+(a*b710))/b600)

def bd640_func(bands, _):
    b600, b648, b709 = bands

    a = (648 - 600) / (709 - 600)
    b = 1.0 - a
    return (1.0 - (b648/((b*b600)+(a*b709))))

def bd860_func(bands, _):
    b800, b860, b984 = bands

    a = (860 - 800) / (984 - 800)
    b = 1.0 - a

    return (1.0 - (b860/((b*b800)+(a*b984))))

def bd920_func(bands, _):
    b800,b920,b984 = bands

    a = (920 - 800) / (984 - 800)
    b = 1.0 - a
    return (1.0 - b920/((b*b800)+(a*b984)))

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

def lcp_index_func(bands, _):
    b1080, b1330, b1815 = bands

    return (100 * ((b1330 - b1080)/(b1330 + b1080)) * ((b1330 - b1815)/(b1330+b1815)))

#@@TODO var

def islope1_func(bands, _):
    b1815, b2530 = bands

    #715 = 2530-1815
    return (b1815 - b2530)/(715)


def bd1435_func(bands, _):
    b1370, b1430, b1470 = bands
    #.6 = (1430 - 1370) / (1470 - 1370)
    a = .6
    #.4 = 1.0 - .6
    b = .4
    return (1.0 - (b1430/((b*b1370)+(a*b1470))))

def bd1500_func(bands, _):
    b1367, b1505, b1558, b1808 = bands
    return (1.0 - ((b1558 + b1505)/(b1808 + b1367)))

def icer1_func(bands, _):
    b1430,b1510 = bands
    return b1430/b1510

def bd1750_func(bands, _):
    b1557, b1750, b1815 = bands
    a = (1750 - 1557) / (1815 - 1557)
    b = 1.0 - a
    return (1.0 - (b1750/((b*b1557)+(a*b1815))))


def bd1900_func(bands, _):
    b1874,b1927,b1972,b2006 = bands
    return (1.0 - ((b1972 + b1927)/(b2006 + b1874)))

#@@TODO bdi2000

def bd2100_func(bands, _):
    b1930, b2120, b2140, b2250 = bands

    a = (((2120 + 2140 / 2) - 1930) / (2250 - 1930))
    b = 1.0 - a
    return (1.0 -(((b2120 + b2140)*.5)/((b*b1930)+(a*b2250))))


def bd2210_func(bands, _):
    b2140,b2210,b2250 = bands
    a = (2210 - 2140) / (2250 - 2140)
    b = 1.0 - a
    return (1.0 - ((b2210)/((b*b2140)+(a*b2250))))


def bd2290_func(bands, _):
    b2250, b2290, b2350 = bands

    a = (2290 - 2250) / (2350 - 2250)
    b = 1.0 - a

    return (1.0 - ((b2290)/((b*b2250)+(a*b2350))))


def d2300_func(bands, _):
    b1815, b2120, b2170, b2210, b2290, b2320, b2330, b2530 = bands

    slope = (b2530 - b1815) / (2530 - 1815)
    cr2290 = b1815 + slope * (2290 - 1815)
    cr2320 = b1815 + slope * (2320 - 1815)
    cr2330 = b1815 + slope * (2330 - 1815)
    cr2120 = b1815 + slope * (2120 - 1815)
    cr2170 = b1815 + slope * (2170 - 1815)
    cr2210 = b1815 + slope * (2210 - 1815)

    return (1.0 - (((b2290/cr2290)+(b2320/cr2320)+(b2330/cr2330))/
                   ((b2120/cr2120)+(b2170/cr2170)+(b2210/cr2210))))

def sindex_func(bands, _):
    b2100, b2400, b2290 = bands
    return (1.0 - ((b2100 + b2400) / (2*b2290)))

def icer2_func(bands, _):
    b2530, b2600 = bands
    return (b2530 / b2600)

def bdcarb_func(bands, _ ):
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
