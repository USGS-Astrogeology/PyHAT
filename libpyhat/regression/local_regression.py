# -*- coding: utf-8 -*-

import numpy as np
from sklearn.linear_model import LassoCV, ElasticNetCV
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import GroupKFold
from joblib import Parallel, delayed

def fit_predict_parallel(i ,x_train = None, y_train = None, x_predict = None, model = None, neighbors = None, verbose = True):
    if verbose == True:
        print('Predicting spectrum ' + str(i + 1))
    x_temp = np.array(x_predict)[i, :]
    foo, ind = neighbors.kneighbors([x_temp])
    x_train_local = np.squeeze(np.array(x_train)[ind])
    y_train_local = np.squeeze(np.array(y_train)[ind])
    cv = GroupKFold(n_splits=3)
    cv = cv.split(x_train_local, y_train_local,
                  groups=y_train_local)
    model.fit(x_train_local, y_train_local)
    predictions = model.predict([x_temp])[0]
    coeffs = model.coef_
    intercepts = model.intercept_

    return predictions, coeffs, intercepts

class LocalRegression:
    """This class implements "local" regression. Given a set of training data and a set of unknown data,
           iterate through each unknown spectrum, find the nearest training spectra, and generate a model.
           Each of these local models is optimized using built-in cross validation methods from scikit."""
    def __init__(self, params, n_neighbors = 250, verbose = True):
        """Initialize LocalRegression

        Arguments:
        params = Dict containing the keywords and parameters for the regression method to be used.

        Keyword arguments:
        n_neighbors = User-specified number of training spectra to use to generate the local regression model for each
                      unknown spectrum.

        """
        self.model = ElasticNetCV(**params) # For now, the only option is Elastic Net. Other methods to be added in the future
                                       # params is a dict containing the keywords and parameters for ElasticNetCV

        self.neighbors = NearestNeighbors(n_neighbors=n_neighbors)
        self.verbose = verbose

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

        args = list(range(x_predict.shape[0]))
        kwargs = {'x_train':x_train,
                  'y_train':y_train,
                  'x_predict':x_predict,
                  'model': self.model,
                  'neighbors': self.neighbors,
                  'verbose':True}
        results = Parallel(n_jobs=-1)(delayed(fit_predict_parallel)(i, **kwargs) for i in args)

        for i in results:
            predictions.append(i[0])
            coeffs.append(i[1])
            intercepts.append(i[2])

        return predictions, coeffs, intercepts

