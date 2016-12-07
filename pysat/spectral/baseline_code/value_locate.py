# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 20:00:30 2014
Translated to Python by Ryan Anderson
@author: rbanderson


#+
# NAME:
#   VALUE_LOCATE
#
# AUTHOR:
#   Richard Schwartz, richard.schwartz@gsfc.nasa.gov
#   Documentation taken from Craig Markwardt's version.
# PURPOSE:
#
#   Locate one or more values in a reference array (IDL LE 5.2 compatibility)
#
# CALLING SEQUENCE:
#
#   INDICES = VALUE_LOCATE(REF, VALUES)
#
# DESCRIPTION: 
#
#   VALUE_LOCATE locates the positions of given values within a
#   reference array.  The reference array need not be regularly
#   spaced.  This is useful for various searching, sorting and
#   interpolation algorithms.
#
#   The reference array should be a monotonically increasing or
#   decreasing list of values which partition the real numbers.  A
#   reference array of NBINS numbers partitions the real number line
#   into NBINS+1 regions, like so:
#
#
# REF:           X[0]         X[1]   X[2] X[3]     X[NBINS-1]
#      <----------|-------------|------|---|----...---|--------------->
# INDICES:  -1           0          1    2       3        NBINS-1
#
#
#   VALUE_LOCATE returns which partition each of the VALUES falls
#   into, according to the figure above.  For example, a value between
#   X[1] and X[2] would return a value of 1.  Values below X[0] return
#   -1, and above X[NBINS-1] return NBINS-1.  Thus, besides the value
#   of -1, the returned INDICES refer to the nearest reference value
#   to the left of the requested value.
#
#   If the reference array is monotonically decreasing then the
#   partitions are numbered starting at -1 from the right instead (and
#   the returned INDICES refer to the nearest reference value to the
#   *right* of the requested value).  If the reference array is
#   neither monotonically increasing or decreasing the results of
#   VALUE_LOCATE are undefined.
#
#   VALUE_LOCATE appears as a built-in funcion in IDL v5.3 and later.
#   This version of VALUE_LOCATE should work under IDL v4 and later,
#   and is intended to provide a portable solution for users who do
#   not have the latest version of IDL.  The algrorithm in this file
#   is slower but not terribly so, than the built-in version.
#
#   Users should be able to place this file in their IDL path safely:
#   under IDL 5.3 and later, the built-in function will take
#   precedence# under IDL 5.2 and earlier, this function will be used.
#
# INPUTS:
#
#   REF - the reference array of monotonically increasing or
#         decreasing values.
#
#   VALUES - a scalar value or array of values to be located in the
#            reference array.
#
#
# KEYWORDS:
#
#   L64 -  for compatibility with built-in version. 
#
#  
# RETURNS:
#
#   An array of indices between -1L and NBINS-1.  If VALUES is an
#   array then the returned array will have the same dimensions.
#
#
# EXAMPLE:
#
#   Cast random values into a histogram with bins from 1-10, 10-100,
#   100-1000, and 1000-10,000.
#
#     ## Make bin edges - this is the ref. array
#     xbins = 10D^dindgen(5)  
#
#     ## Make some random data that ranges from 1 to 10,000
#     x     = 10D^(randomu(seed,1000)*4)
#
#     ## Find the bin number of each random value
#     ii    = value_locate(xbins, x)
#
#     ## Histogram the data
#     hh    = histogram(ii)
#
#
# SEE ALSO:
#
#   VALUE_LOCATE (IDL 5.3 and later), HISTOGRAM, CMHISTOGRAM
#
#
# MODIFICATION HISTORY:
#   Written and documented, 7-aug-2006
#   Case of XBINS having only one element, CM, 29 Apr 2001
#   Handle case of VALUES exactly hitting REF points, CM, 13 Oct 2001
#   19-Oct-2006 - modified to return array with same dimensions as
#    second argument as with the IDL intrinsic
#   1-nov-2006, ras, protect against differing input dimensions
#	causing concatenation problems
# 
#  
#
#-
# Copyright (C) 2006, richard schwartz
# This software is provided as is without any warranty whatsoever.
# Permission to use, copy, modify, and distribute modified or
# unmodified copies is granted, provided this copyright and disclaimer
# are included unchanged.
#-
"""
import numpy
"""
def is_defined(var): 
    # debug,'V1.0 FH 1998-01-20' 
    a = var.shape 
    n = a.size 
    return a[n - 2] != 0 


def is_scalar(var):
    # debug,'V1.0 FH 1998-01-23' 
    return var.shape[0]==0 and is_defined(var) 
""" 


def val_loc_inc(x, u):
    

    nx  = x.size
    nu  = u.size
    mm  = max(x[-1],max(u))*1.01
    xx  = numpy.append([x],[mm])
    c1   = numpy.append([xx],[u])
    
    ord1 = numpy.argsort(c1)
    d1   = numpy.append([-1],numpy.append(numpy.where(ord1<nx), nx))
    out=numpy.zeros(nu)
    

    j0  = d1+1
    j1  = d1[1:]-1
    nouti = j1-j0[:len(j1)]+1
    oldout=out
    for i in list(range(0,int(nx)+1)):
        if nouti[i] >= 1:
            tmp=ord1[j0[i]:j1[i]+1]-nx
            #print(tmp)            
            out[tmp]= int(i-1)
    #check boundaries
    nlow = 1
    itst = 0
    while nlow >= 1:
        xxout=[]
        for i in out+1:
            xxout.append(xx[i])
        bound = numpy.where(numpy.all(numpy.array([xxout<= u,xxout==u]),axis=0)==True)[0]
        nlow=bound.size
        if nlow>= 1: 
            out[bound]=out[bound]+1
    	
        itst = itst + 1
        if itst > numpy.float32(999999): print('Boundary Check Failed')
    	
    for i in out:
        i = min(i,(nx-2))
    if u.shape[0] == 0: out = out[0]
    return out
    

def value_locate(x,u1,l64=False):
    
    #increasing or decreasing
    #default, l64,0
    

  #  if is_scalar(u):
  #      out=0
  #  else:
    if l64:
        arrtype='float64'
    else:
        arrtype='float32'
    out=numpy.zeros(u1.shape,dtype=arrtype)

    if x[-1] < x[0]:
        temp=x.size-2-val_loc_inc(x[::-1],u1,l64=l64)
    else:
        temp = val_loc_inc(x, u1)
    
    out = out + temp
    return out
    
