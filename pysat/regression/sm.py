# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 20:15:46 2016

@author: rbanderson
"""
import numpy as np
import scipy.optimize as opt


class sm:
    def __init__(self, blendranges, submodels):
        self.blendranges = blendranges
        self.submodels = submodels

    def do_blend(self, predictions, truevals=None):

        # create the array indicating which models to blend for each blend range
        # For three models, this creates an array like: [[0,0],[0,1],[1,1],[1,2],[2,2]]
        # Which indicates that in the first range, just use model 0
        # In the second range, blend models 0 and 1
        # in the third range, use model 1
        # in the fourth range, blend models 1 and 2
        # in the fifth range, use model 2

        self.toblend = []
        for i in range(len(predictions) - 1):
            self.toblend.append([i, i])
            if i < len(predictions) - 2:
                self.toblend.append([i, i + 1])

        # If the true compositions are provided, then optimize the ranges over which the results are blended to minimize the RMSEC
        # get the ranges that are not the reference model (assumed to be the last model)
        catchall = self.blendranges[-1]
        ranges_sub = self.blendranges[:-1]
        blendranges = np.array(ranges_sub).flatten()  # squash them to be a 1d array
        blendranges.sort()  # sort the entries. These will be used by submodels_blend to decide how to combine the predictions

        if truevals is not None:
            print('Optimizing blending ranges')
            truevals = np.squeeze(np.array(truevals))
            result = opt.minimize(self.get_rmse, blendranges, (predictions, truevals))
            self.blendranges = result.x
        else:
            self.blendranges = blendranges

        # calculate the blended results
        blended = self.submodels_blend(predictions, self.blendranges, overwrite=False)
        return blended

    def get_rmse(self, blendranges, predictions, truevals):
        blendranges[1:-1][blendranges[1:-1] < 0] = 0.0  # ensure range boundaries don't drift below zero
        blendranges[1:-1][blendranges[1:-1] > 100] = 100  # ensure range boundaries don't drift above 100
        blendranges.sort()  # ensure range boundaries stay in order

        print('Blend ranges: ' + str(blendranges))  # show the blendranges being used for the current calculation
        blended = self.submodels_blend(predictions, blendranges, overwrite=False)
        RMSE = np.sqrt(np.mean((blended - truevals) ** 2))  # calculate the RMSE
        print('RMSE=' + str(RMSE))
        return RMSE
        
    def submodels_blend(self,predictions,blendranges,overwrite=False):
        blended=np.squeeze(np.zeros_like(predictions[0]))
        
        #format the blending ranges
        blendranges=np.hstack((blendranges,blendranges[1:-1])) #duplicate the middle entries
        blendranges.sort() #re-sort them
        blendranges=np.reshape(blendranges,(int(len(blendranges)/2),int(2)))  #turn the vector into a 2d array (one pair of values for each submodel)
        self.toblend.append([len(predictions)-1,len(predictions)-1])
        blendranges=np.vstack((blendranges,[-9999999,999999]))

        for i in range(len(blendranges)): #loop over each composition range
            for j in range(len(predictions[0])): #loop over each spectrum
                ref_tmp=predictions[-1][j]   #get the reference model predicted value
                #check whether the prediction for the reference spectrum is within the current range            
                inrangecheck=(ref_tmp>blendranges[i][0])&(ref_tmp<blendranges[i][1])
     
                if inrangecheck: 
                    if self.toblend[i][0]==self.toblend[i][1]: #if the results being blended are identical, no blending necessary!
                        blendval=predictions[self.toblend[i][0]][j]

                    else:
                        weight1 = 1 - (ref_tmp - blendranges[i][0]) / (
                            blendranges[i][1] - blendranges[i][0])  # define the weight applied to the lower model
                        weight2 = (ref_tmp - blendranges[i][0]) / (
                            blendranges[i][1] - blendranges[i][0])  # define the weight applied to the higher model
                        # calculated the blended value (weighted sum)
                        blendval = weight1 * predictions[self.toblend[i][0]][j] + weight2 * \
                                                                                  predictions[self.toblend[i][1]][j]
                    if overwrite:
                        blended[j] = blendval  # If overwrite is true, write the blended result no matter what
                    else:
                        # If overwrite is false, only write the blended result if there is not already a result there
                        if blended[j] == 0:
                            blended[j] = blendval

        return blended

    def predict(self, x):
        # x is a list of data frames to feed into each submodel.
        # This allows different normalizations to be used with each submodel
        predictions = []
        for i, k in enumerate(self.submodels):
            try:
                xtemp = x[i]
            except:
                pass
            predictions.append(k.predict(xtemp))
        return predictions
