# -*- coding: utf-8 -*-

import copy
import traceback
import numpy as np
from sklearn.linear_model import LassoCV
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import GroupKFold

class LocalRegression:
    """This class implements "local" regression. Given a set of training data and a set of unknown data,
           iterate through each unknown spectrum, find the nearest training spectra, and generate a model.
           Each of these local models is optimized using built-in cross validation methods from scikit."""
    def __init__(self, params, n_neighbors = 250):
        """Initialize LocalRegression

        Arguments:
        params = Dict containing the keywords and parameters for the regression method to be used.

        Keyword arguments:
        n_neighbors = User-specified number of training spectra to use to generate the local regression model for each
                      unknown spectrum.

        """
        self.model = LassoCV(**params) # For now, the only option is LASSO. Other methods to be added in the future
                                       # params is a dict containing the keywords and parameters for LassoCV

        self.neighbors = NearestNeighbors(n_neighbors=n_neighbors)

    def fit_predict(self,x_train,y_train, x_predict):
        """Use local regression to predict values for unknown data.

        Arguments:
            x_train = The training data spectra.
            y_train = The values of the quantity being predicted for the training data
            x_predict = The unknown spectra for which y needs to be predicted.
        """
        self.neighbors.fit(x_train)
        predictions = []
        coeffs = []
        intercepts = []
        for i in range(x_predict.shape[0]):
            print('Predicting spectrum ' + str(i + 1))
            x_temp = np.array(x_predict)[i,:]
            foo, ind = self.neighbors.kneighbors([x_temp])
            x_train_local = np.squeeze(np.array(x_train)[ind])
            y_train_local = np.squeeze(np.array(y_train)[ind])
            cv = GroupKFold(n_splits=3)
            cv = cv.split(x_train_local, y_train_local,
                          groups=y_train_local)
            self.model.fit(x_train_local, y_train_local)
            predictions.append(self.model.predict([x_temp])[0])
            coeffs.append(self.model.coef_)
            intercepts.append(self.model.intercept_)
        return predictions, coeffs, intercepts

