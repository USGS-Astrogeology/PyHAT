# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 19:54:18 2014
Translated to Python by Ryan Anderson Nov 2014 and Oct 2016
@author: rbanderson


#+
# NAME:	
#             SPL_INTERP
#
# DESCRIPTION:
#   Given arrays XA and YA of length N, which tabulate a function (with the
#   XA's in order), and given the array Y2A, which is the output from
#   SPLINE.PRO, this routine returns the cubic-spline interpolated values
#   at the locations of the array X.
#
#   Note that the keyword DOUBLE of the IDL intrinsic function is ignored.
#   Tests in single precision have shown that the routine is exactly
#   similar to the IDL function.
#   SPL_INIT is also recoded similarly.
#
# SOURCE:
#	Numerical Recipes, 1986. (page 89)
# 
# CALLING SEQUENCE:
#	y = spl_interp(xa,ya,y2a,x)
#
# INPUTS:
#	xa - independent variable vector
#	ya - dependent variable vector
#	y2a- second derivative vector from SPLINF.PRO
#	x  - x value of interest
#
# OUTPUTS:
#	y  - cubic-spline interpolated value at x
#
# HISTORY:
#	converted to IDL, D. Neill, October, 1991
#       arranged as a substitution for SPL_INTERP (for use in GDL)
#       Ph. Prugniel, 2008/02/29
#-
# -----------------------------------------------------------------------------
# NOTE:
# Name this function: spl_init to use it as a replacement of the IDL intrinsic
#      when using GDL
# But, to make a comparison of numerical results with the IDL intrinsic
# function, as it is made in the attached program: test_splt, change its
# name in:
#   function psplint,xa,ya,y2a,x   # name used to make comparison test with IDL
# so that IDL can execute either its intrinsic or the substitute.
# Anyway, this comparison has been made with success and if you just
# want to use this function in GDL ... ignore this remark
# -----------------------------------------------------------------------------
"""

import numpy
#function PSPLINT, xa, ya, y2a, x, DOUBLE=double
def spl_interp(xa, ya, y2a, x):
    
    n = xa.size

#    valloc=baseline_code.value_locate.value_locate(xa, x)
    valloc=numpy.digitize(x,xa)-1 #The numpy routine digitize appears to basically do what value_locate does in IDL
    klo=[]
    for i in valloc:
        klo.append(min(max(i,0),(n-2)))
    klo=numpy.array(klo)
    khi = klo + 1
    #
    # KLO and KHI now bracket the input value of X
    #
    
    if min(xa[khi]-xa[klo])==0: print('SPLINT - XA inputs must be distinct')
    #
    # Cubic spline polynomial is now evaluated
    #
    h = xa[khi] - xa[klo]
    
    a = ( xa[khi] - x ) / h
    b = ( x - xa[klo] ) / h
    output=a*ya[klo]+b*ya[khi]+((a**3.-a)*y2a[klo]+(b**3.-b)*y2a[khi])*(h**2.)/6.
    return output
    
    	# spl_interp.pro

