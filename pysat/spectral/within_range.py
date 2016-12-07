# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:11:37 2016

@author: rbanderson
"""
#def within_range(x,y,rangevals):
    #mask=(y>rangevals[0])&(y<rangevals[1])
    #return x.loc[mask],y.loc[mask]
    
def within_range(data,rangevals,col):
    mask=(data[('meta',col)]>rangevals[0])&(data[('meta',col)]<rangevals[1])
    return data.loc[mask]