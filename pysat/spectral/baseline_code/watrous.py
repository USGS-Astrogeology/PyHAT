# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 18:21:47 2014
Translated to Python from IDL by Ryan Anderson
@author: rbanderson
"""
import numpy 
import scipy
import scipy.signal


def watrous(z,scale,kernel=numpy.array([1.,4.,6.,4.,1.])/16.):
    z=numpy.float32(z)
    s=z.shape
    sk=kernel.shape[0]

    if len(s) == 1:
        n=s[0]
        w=numpy.zeros((s[0]*3,scale),dtype=numpy.float)
        temp=z[0:n]
        temp=temp[::-1]
        w[0:n,0]=temp
        w[n:s[0]+n,0]=z
        temp=z[s[0]-n:]
        temp=temp[::-1]
        w[s[0]+n:,0]=temp
        for i in range(0,scale-1):
           # print i
            k1=numpy.zeros((sk-1)*2.**i+1,dtype=numpy.float)
            i1=numpy.array((numpy.arange(sk))*2.**i,dtype=numpy.int)
            k1[i1]=kernel
         
            tsmooth=numpy.convolve(w[:,i],k1,mode='same')
            #tsmooth=scipy.signal.fftconvolve(w[:,i],k1,mode='same')    
            #print tsmooth[1000]
            w[:,i]=w[:,i]-tsmooth
            w[:,i+1]=tsmooth
        
        w=w[n:s[0]+n,:]
    
    elif len(s)==2:
        w=numpy.zeros((s[0],s[1],scale),dtype=numpy.float)
        w[:,:,0]=z

        for i in range(0,scale-1):
            k1=numpy.zeros((sk-1)*2.**i+1,dtype=numpy.float)
            i1=numpy.array((numpy.arange(sk))*2.**i,dtype=numpy.int)
            k1[i1]=kernel
            k2=numpy.dot(k1,k1)
            tsmooth=numpy.convolve(w[:,:,i],k2,mode='same')
            #tsmooth=scipy.signal.fftconvolve(w[:,:,i],k2,mode='same')            
            w[:,:,i]=w[:,:,i]-tsmooth            
            w[:,:,i+1]=tsmooth
    
    elif len(s)==3:
        w=numpy.zeros((s[0],s[1],s[2]),dtype=numpy.float)
        for l in range(0,s[2]):
            w[:,:,l,0]=z[:,:,l]
            for i in range(0,scale-1):
                k1=numpy.zeros((sk-1)*2.**i+1,dtype=numpy.float)
                i1=numpy.array((numpy.arange(sk))*2.**i,dtype=numpy.int)
                k1[i1]=kernel
                k2=numpy.dot(k1,k1)
                tsmooth=numpy.convolve(w[:,:,l,i],k2,mode='same')
                #tsmooth=scipy.signal.fftconvolve(w[:,:,l,i],k2,mode='same')                
                w[:,:,l,i]=w[:,:,l,i]-tsmooth
                w[:,:,l,i+1]=tsmooth
    else:
        print("Wrong dimensions!")
        return -1
    return w
