# -*- coding: utf-8 -*-
"""
Translation to Python begun on Tue Nov 04 16:31:33 2014 by Ryan Anderson

;+
; NAME:
;       REMOVE_CONTINUUM
; PURPOSE:
;       This routine removes the continuum from a Libs spectrum
;
; CALLING SEQUENCE: 
;       REMOVE_CONTINUUM, Wavelength, Spectrum, Wavelet_Scale1, Wavelet_Scale2, interpolation_Flaog

; INPUTS: 
;       Wavelength: One dimensional array of wavelengths
;       Spectrum: One dimensional array of libs intensity (same size as wavelength)
;       Wavelet_Scale1: Integer; Largest wavelet scale to start with
;       (2^Wavelet_scale) LT wavelength size)
;       Wavelet_Scale2: Integer; Lowest wavelet scale to look at (must be GE 2)
;       Interpolation_Flag: Integer; Flag to select interpolation method
;       between convex hull points
;         0: linear interpolation    
;         1: quadratic interpolation    
;         2: spline interpolation
    
; OPTIONAL INPUTS:
;
; KEYWORD PARAMETERS:
;
; OUTPUTS:
;
; OPTIONAL OUTPUTS:
;
; COMMON BLOCKS:
;
; SIDE EFFECTS:
;     The input spectrum is replaced by the spectrum - continuum
;
; RESTRICTIONS:
;
; PROCEDURE:
;
; EXAMPLE:
;     Remove_Continuum,wl, sp, 6, 4, 0
; MODIFICATION HISTORY:
;      Olivier Forni IRAP
;      First Version  June 2009
;      Add interpolation Flag October 2009
;      Modify convex hull October 2011
;      Translated to Python by Ryan Anderson Nov 2014
;      

"""
import numpy
import scipy
import pysat.spectral.baseline_code.watrous
import pysat.spectral.baseline_code.spl_init
import pysat.spectral.baseline_code.spl_interp 
from pysat.spectral.baseline_code.common import Baseline
# import pywt <- this needs to be fixed, it doesn't exist in and outside pysat
     
def chemcam_continuum(x,sp,int_flag,lvmin=-9999):
    n=len(sp)
    lv=int(numpy.log(n-1)/numpy.log(2))
    sp1=sp
    #sp1=scipy.signal.medfilt(sp1,kernel_size=9)
    w=baseline_code.watrous.watrous(sp1,lv)
    lvmn=lv-1
    if lvmin != -9999:
        if lvmin<lv:
            lvmn=lvmin
        else:
            lvmn=lv-1
    si=w[:,lvmn]
    ii=numpy.zeros(n)
   # print(range(1,n-2)
    for i in range(1,n-1):

        if si[i]<si[i+1] and si[i]<si[i-1]:
            ii[i]=1
    ii[0]=1
    ii[n-1]=1
    i0=numpy.squeeze((numpy.array(numpy.where(ii==1))))
    
    n0=len(i0)
    yi=numpy.zeros(n0)
    yi[0]=sp[0]
    yi[n0-1]=sp[n-1]
    
    for i in range(0,n0):
        dx1=i0[i]-2**(lvmn)

        if dx1<0:
            dx1=0
        dx2=i0[i]+2**(lvmn)

        if dx2 >= n:
            dx2=n-1
        yi[i]=min(sp[dx1:dx2])
   # print(x[i0])
   # print(yi)
    #if len(i0)==2: int_flag=0 #If there are only 2 points, just use a linear fit
    if int_flag==0:
        yf=scipy.interpolate.interp1d(x[i0],yi)
        yf=yf(x)
    elif int_flag==1:
        if n0 >=3:
            yf=scipy.interpolate.interp1d(x[i0],yi,kind='quadratic')
            yf=yf(x)
        else:
            yf=scipy.interpolate.interp1d(x[i0],yi)
            yf=yf(x)
    elif int_flag==2:
        #tck=scipy.interpolate.splrep(x[i0],yi,k=3,s=0)
        #yf=scipy.interpolate.splev(x,tck)
        """
        print('Working in decimals')
        xi_dec=decimalVectorList.decimalvector(len(i0))
        x_dec=decimalVectorList.decimalvector(len(x))
        yi_dec=decimalVectorList.decimalvector(len(yi))
        for i in range(len(xi_dec)): xi_dec[i]=decimalVectorList.Decimal(x[i0[i]])
        for i in range(len(yi_dec)): yi_dec[i]=decimalVectorList.Decimal(yi[i]) 
        for i in range(len(x)): x_dec[i]=decimalVectorList.Decimal(x[i])
        y=decimalpy.NaturalCubicSpline(xi_dec,yi_dec)    
        yf=numpy.array(y(x_dec),dtype='float')
        """
        #TODO: There are probably python spline interpolation functions that would give the same result
        #But for now, use the translated functions from IDL
        
        y=baseline_code.spl_init.spl_init(x[i0],yi)
        yf=baseline_code.spl_interp.spl_interp(x[i0],yi,y,x)
        
        
        
    return yf
        

def ccam_remove_continuum(x,y,lv,lvmin=2,int_flag=2):
    x=numpy.array(x,dtype='float64')
    y=numpy.array(y,dtype='float64')    
    y_old=y    
    if len(x.shape) != 1:
        print("Wavelength must be a 1D array!")
        return
    
    if len(y) != len(x):
        print("Intensity and wavelength must have the same size!")
        return
    
    if lvmin<2:
        print("Lowest wavelet scale must be greater than or equal to 2")
        return
    
    n=len(x)
    lvmax=int(numpy.log(n-1)/numpy.log(2))
    if lv>lvmax:
        print("Largest wavelet scale must be less than or equal to :"+str(lvmax))
        return
    
    if lvmin>lv:
        print("Lowest wavelet scale must be less than or equal to largest wavelet scale")
        return
    
    if int_flag<0 or int_flag>2:
        print("Valid values of the interpolation flag are 0, 1, or 2")
        return
    
    stdb0=numpy.std(y,ddof=1)
    stdb=stdb0
    y_old=y
    
    for il in range(lv,lvmin-1,-1):
        counter=0
        while stdb > stdb0*1e-2:
            sc=chemcam_continuum(x,y,int_flag,lvmin=il)
            counter=counter+1
            #print(il,counter)
            #print(sc[1000])
            y=y-sc
            stdb=numpy.std(sc,ddof=1)
        stdb0=numpy.std(y,ddof=1)
        stdb=stdb0
        y=y-sc
    
    baseline=y_old-y
    return baseline
        

class ccam_br(Baseline):
  def __init__(self,lv=10,lvmin=2,int_flag=2):
    self.lv_ = lv
    self.lvmin_ = lvmin
    self.int_flag_ = int_flag
    

  def _fit_one(self, x, y):
    return ccam_remove_continuum(x,y, self.lv_, lvmin=self.lvmin_,
                           int_flag=self.int_flag_)

 
                
        
