# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 20:15:46 2016

@author: rbanderson
"""
import numpy as np
import scipy.optimize as opt
from pysat.regression.regression import regression 
from pysat.spectral.within_range import within_range
class sm:
    def __init__(self,ranges,method,params,ransacparams=None):
        self.method=method 
        self.ranges=ranges
        self.ransacparams=ransacparams
        self.params=params
        self.submodels=[]
        for i,rangei in enumerate(ranges):
            self.submodels.append(regression(method,params,i=i,ransacparams=ransacparams))
        
    #This function does the fitting for each submodel.
    def fit(self,x,y):
        for i,model in enumerate(self.submodels):
            xtemp,ytemp=within_range(x[i],y[i],self.ranges[i])
            model.fit(xtemp,ytemp)
            
 
    def do_blend(self,predictions,truevals=None):

        #create the array indicating which models to blend for each blend range
        #For three models, this creates an array like: [[0,0],[0,1],[1,1],[1,2],[2,2]]
        #Which indicates that in the first range, just use model 0
        #In the second range, blend models 0 and 1
        #in the third range, use model 1
        #in the fourth range, blend models 1 and 2
        #in the fifth range, use model 2
        
        self.toblend=[]
        for i in range(len(predictions)-1):
            self.toblend.append([i,i])
            if i<len(predictions)-2:
                self.toblend.append([i,i+1])
            
        #If the true compositions are provided, then optimize the ranges over which the results are blended to minimize the RMSEC
        if truevals is not None:
            print('Optimizing blending ranges')
            #get the ranges that are not the reference model (assumed to be the last model)
            ranges_sub=self.ranges[:-1]
            blendranges=np.array(ranges_sub).flatten() #squash them to be a 1d array
            blendranges.sort()  #sort the entries. These will be used by submodels_blend to decide how to combine the predictions
         
            result=opt.minimize(self.get_rmse,blendranges,(predictions,truevals))
            self.blendranges=result.x

            
        #calculate the blended results
        blended=self.submodels_blend(predictions,self.blendranges,overwrite=False,noneg=False)
        return blended
        
    def get_rmse(self,blendranges,predictions,truevals):
        blendranges  #show the blendranges being used for the current calculation
        blended=self.submodels_blend(predictions,blendranges,overwrite=False,noneg=False)
        RMSE=np.sqrt(np.mean((blended-truevals)**2))  #calculate the RMSE
        return RMSE
        
    def submodels_blend(self,predictions,blendranges,overwrite=False,noneg=False):
        blended=np.squeeze(np.zeros_like(predictions[0]))
        
        #format the blending ranges
        blendranges=np.hstack((blendranges,blendranges[1:-1])) #duplicate the middle entries
        blendranges.sort() #re-sort them
        blendranges=np.reshape(blendranges,(len(blendranges)/2,2))  #turn the vector into a 2d array (one pair of values for each submodel)
        
        
        for i in range(len(blendranges)): #loop over each composition range
            for j in range(len(predictions[0])): #loop over each spectrum
                ref_tmp=predictions[-1][j]   #get the reference model predicted value
                #check whether the prediction for the reference spectrum is within the current range            
                inrangecheck=(ref_tmp>blendranges[i][0])&(ref_tmp<blendranges[i][1])
     
                if inrangecheck: 
                    if self.toblend[i][0]==self.toblend[i][1]: #if the results being blended are identical, no blending necessary!
                      
                        blendval=predictions[self.toblend[i][0]][j]
                    else:
                        weight1=1-(ref_tmp-blendranges[i][0])/(blendranges[i][1]-blendranges[i][0]) #define the weight applied to the lower model
                        weight2=(ref_tmp-blendranges[i][0])/(blendranges[i][1]-blendranges[i][0]) #define the weight applied to the higher model
                        blendval=weight1*predictions[self.toblend[i][0]][j]+weight2*predictions[self.toblend[i][1]][j] #calculated the blended value (weighted sum)
                    if overwrite:
                        blended[j]=blendval #If overwrite is true, write the blended result no matter what
                    else:
                        if blended[j]==0:  #If overwrite is false, only write the blended result if there is not already a result there
                            blended[j]=blendval                
        #Set any negative results to zero if noneg is true
        if np.min(blended)<0 and noneg==True:
            blended[blended<0]=0
    
        return blended
    
    def predict(self,x):
        #x is a list of data frames to feed into each submodel. 
        #This allows different normalizations to be used with each submodel
        predictions=[]
        for i,k in enumerate(self.submodels):
            try:
                xtemp=x[i]
            except:
                pass
            predictions.append(k.predict(xtemp))
        return predictions
