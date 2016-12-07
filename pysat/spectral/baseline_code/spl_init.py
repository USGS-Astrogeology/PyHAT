# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 13:22:09 2014
Translated from IDL to Python by Ryan Anderson
@author: rbanderson


#+
# NAME:	
#             SPL_INIT
#
# DESCRIPTION:
#   Given arrays X and Y of length N containing a tabulated function, i.e.
#   Yi = f(Xi), with X1 > X2 > ... > Xn, and given values YP1 and YPN for the
#   first derivative of the interpolating function at points 1 and N,
#   respectively, this routine returns and array Y2 of length N which contains
#   the second derivatives of the interpolating function at the tabulated 
#   points Xi.  If YP1 and/or YPN are equal to 1.E30 or larger, the routine 
#   is signalled to set the corresponding boundary condition for a natural 
#   spline, with zero second derivative on that boundary.
#
#   This routine is a replacement for the IDL intrinsic function
#   to be used with GDL while this latter does not have it as an
#   intrinsic.
#
#   Note that the keyword DOUBLE of the IDL intrinsic function is ignored.
#   Tests in single precision have shown that the routine is exactly
#   similar to the IDL function.
#   SPL_INTERP is also recoded similarly.
#
# SOURCE:
#	Numerical Recipes, 1986. (page 88)
# 
# CALLING SEQUENCE:
#	y2 = SPL_INIT( x, y, YP0=yp1, YPN_1=ypn)
#
# INPUTS:
#	x - independent variable vector
#	y - dependent variable vector
#	yp1 - first derivative at x(0)
#	ypn - first derivative at x(n-1)
#
# OUTPUTS:
#	y2 - second derivatives at all x, of length n
#
# HISTORY:
#	converted to IDL, D. Neill, October, 1991
#       arranged as a substitution for SPL_INIT (for use in GDL)
#       Ph. Prugniel, 2008/02/29
#
# -----------------------------------------------------------------------------
# NOTE:
# Name this function: spl_init to use it as a replacement of the IDL intrinsic
#      when using GDL
# But, to make a comparison of numerical results with the IDL intrinsic
# function, as it is made in the attached program: test_splf, change its
# name in "psplinf", so that IDL can execute either its intrinsic or
# the substitute.
# Anyway, this comparison has been made with success and if you just
# want to use this function in GDL ... ignore this remark
# -----------------------------------------------------------------------------

#function PSPLINF, x, y, YP0=yp1, YPN_1=ypn, DOUBLE=double
"""
import numpy
def shift(array,amount):
    return numpy.append([array[-amount:]],[array[:-amount]])

def spl_init( x, y, yp1=None, ypn=None):
    import numpy
    n = len(x)

    y2 = numpy.zeros(n)
    u = numpy.zeros(n)
    #
    # The lower boundary condition is set either to be "natural"
    #
    if yp1 == None:
        y2[0] = 0.
        u[0] = 0.
    ##
    ## or else to have a specified first derivative
    ##
    if yp1 != None:
        y2[0] = -0.5
        u[0] = (3./(x[1]-x[0]))*((y[1]-y[0])/(x[1]-x[0])-yp1)
    
    
    # I suppose we can also take advantage here of the TRISOL function
    # from IDL... we can remove the for loops
    #
    # This is the decomposition loop of the tridiagonal algorithm.  Y2 and
    # U are used for temporary storage of the decomposed factors.
    #
    
 #   x_neg1=numpy.append([x[1:]],[x[0]])
  #  x_pos1=numpy.append([x[-1]],[x[1:]])
   # y_neg1=numpy.append([y[1:]],[y[0]])
    #y_pos1=numpy.append([y[-1]],[y[1:]])
   # print x_neg1.shape
   # print x_pos1.shape
   # print x.shape
    
    psig = ((x - shift(x,-1))) / (shift(x,1) - shift(x,-1))
    
    pu = ((shift(y,-1) - y) / (shift(x,-1) - x) - (y - shift(y,1)) / (x - shift(x,1))) / (shift(x,-1)- shift(x,1))
    
    for i in range(1,n-1):
        p = psig[i] * y2[i-1] + 2.
        y2[i] = ( psig[i]-1. ) / p
        u[i]=( 6. * pu[i] - psig[i]*u[i-1] ) / p
    
    
    #
    # The upper boundary condition is set either to be "natural"
    #
    if ypn==None: 
        qn=0.
        un=0.
    #
    # or else to have a specified first deriviative
    #
    if ypn !=None:
        qn=0.5
        dx=x[n-1]-x[n-2]
        un=(3./dx)*(ypn-(y[n-1]-y[n-2])/dx)
    
    #
    y2[n-1] = ( un - qn * u[n-2] ) / ( qn * y2[n-2] + 1. )
    
    #
    # This is the backsubstitution loop of the tridiagonal algorithm
    #
    
    for k in range(n-2,-1,-1):
        y2[k] = y2[k] * y2[k+1] + u[k]
    
    
    
    return y2

    
