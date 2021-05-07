import numpy as np
import pandas as pd
from libpyhat.examples import get_path
import libpyhat.regression.cv as cv
from libpyhat.utils.folds import stratified_folds
from sklearn.model_selection import ParameterGrid
np.random.seed(1)



def test_cv_nofolds():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    params = {'n_components': [1, 2, 3],
              'scale': [False]}
    paramgrid = list(ParameterGrid(params))

    cv_obj = cv.cv(paramgrid)
    results = cv_obj.do_cv(df, xcols='wvl', ycol=[('comp', 'SiO2')],
                                                                  method='PLS', yrange=[0, 100], calc_path=False,
                                                                  alphas=None)
    assert results[0].shape == df.shape
    assert results[1].shape == (0,0)
    assert results[2] == []
    assert results[3] == []
    assert results[4] == []


def test_cv():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    df = stratified_folds(df, nfolds=3, sortby=('comp', 'SiO2'))

    params = {'n_components': [1,2,3],
                      'scale': [False]}
    paramgrid = list(ParameterGrid(params))


    cv_obj = cv.cv(paramgrid)
    df_out, output, models, modelkeys, predictkeys = cv_obj.do_cv(df,xcols='wvl',ycol=('comp','SiO2'),method='PLS',
                                                                  yrange=None,calc_path=False,alphas=None)

    expected_predicts = [56.55707481, 57.93716105, 59.34785052, 60.59708391, 55.83934129, 56.7456989 ]
    expected_output_rmsec = [18.6509206, 14.64015186, 13.80182457]

    np.testing.assert_array_almost_equal(expected_predicts,np.array(df_out['predict'].iloc[0,:]))
    np.testing.assert_array_almost_equal(expected_output_rmsec,np.array(output[('cv','RMSEC')]))
    assert output.shape==(3,8)
    assert len(models)==3
    assert len(modelkeys)==3
    assert modelkeys[0]=='PLS - SiO2 - (0.0, 98.57) {\'n_components\': 1, \'scale\': False}'
    assert len(predictkeys)==6
    assert predictkeys[0]=='"PLS- CV -{\'n_components\': 1, \'scale\': False}"'

def test_cv_badfit():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    df = stratified_folds(df, nfolds=3, sortby=('comp', 'SiO2'))

    params = {'n_nonzero_coefs': [1000,2000]}
    paramgrid = list(ParameterGrid(params))

    cv_obj = cv.cv(paramgrid)
    df_out, output, models, modelkeys, predictkeys = cv_obj.do_cv(df,xcols='wvl',ycol=[('comp','SiO2')],method='OMP',
                                                                  yrange=None,calc_path=False,alphas=None)
    expected_predicts = np.nan
    np.testing.assert_array_almost_equal(expected_predicts,np.array(df_out['predict'].iloc[0,0]))


def test_cv_local_regression():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    df = df.iloc[0:20,:]  #make data set smaller so this test runs faster
    df = stratified_folds(df, nfolds=3, sortby=('comp', 'SiO2'))

    params = {'n_neighbors': [5, 6],
              'fit_intercept': [True],
              'positive': [False],
              'random_state': [1],
              'tol': [1e-2],
              'l1_ratio':[.1, .7, .95, 1],
              'verbose':[False]
              }
    paramgrid = list(ParameterGrid(params))

    cv_obj = cv.cv(paramgrid)
    df_out, output, models, modelkeys, predictkeys = cv_obj.do_cv(df, xcols='wvl', ycol=('comp', 'SiO2'),
                                                                  method='Local Regression', yrange=[0, 100],
                                                                  calc_path=False, alphas=None)

    expected_predicts = [51.83360028, 54.24957492, 46.05024927, 54.21137841, 51.314045]
    expected_output_rmsec = [10.23372859, 10.9200063]

    np.testing.assert_array_almost_equal(expected_predicts, np.array(df_out['predict'].iloc[5, 0:5]))
    np.testing.assert_array_almost_equal(expected_output_rmsec, np.array(output[('cv', 'RMSEC')])[0:2])
    assert output.shape == (8, 13)
    assert len(models) == 8
    assert len(modelkeys) == 8
    assert modelkeys[0] == 'Local Regression - SiO2 - (0, 100) {\'fit_intercept\': True, \'l1_ratio\': 0.1, \'positive\': False, \'random_state\': 1, \'tol\': 0.01} n_neighbors: 5'
    assert len(predictkeys) == 16
    assert predictkeys[0] == '"Local Regression- CV -{\'fit_intercept\': True, \'l1_ratio\': 0.1, \'positive\': False, \'random_state\': 1, \'tol\': 0.01} n_neighbors: 5"'