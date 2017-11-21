from regression.regression import regression


def test_PLS():
    regress = regression(method=['PLS'], yrange=[0.0, 100.0], params=[{'n_components': 0,
                                                                       'scale': False}], ransacparams={})


def test_GP():
    regress = regression(method=['GP'], yrange=[0.0, 100.0],
                         params=[{'reduce_dim': 'PCA',
                                  'n_components': 0,
                                  'random_start': 1,
                                  'theta0': 1.0,
                                  'thetaL': 0.1,
                                  'thetaU': 100.0}], ransacparams={})


def test_OLS():
    regress = regression(method=['OLS'], yrange=[0.0, 100.0], params=[{'fit_intercept': True}], ransacparams={})


def test_OMP():
    regress = regression(method=['OMP'], yrange=[0.0, 100.0], params=[{'fit_intercept': True,
                                                                       'n_nonzero_coefs': 615,
                                                                       'CV': True}],
                         ransacparams={})


def test_Lasso():
    regress = regression(method=['Lasso'], yrange=[0.0, 100.0],
                         params=[{'alpha': 1.0,
                                  'fit_intercept': True,
                                  'max_iter': 1000,
                                  'tol': 0.0001,
                                  'positive': False,
                                  'selection': 'random',
                                  'CV': True}], ransacparams={})


def test_Elastic_Net():
    regress = regression(method=['Elastic Net'], yrange=[0.0, 100.0],
                         params=[{'alpha': 1.0,
                                  'l1_ratio': 0.5,
                                  'fit_intercept': True,
                                  'normalize': False,
                                  'precompute': 'False',
                                  'max_iter': 1000,
                                  'copy_X': True,
                                  'tol': 0.0001,
                                  'warm_start': False,
                                  'positive': False,
                                  'selection': 'cyclic',
                                  'random_state': 'None'}],
                         ransacparams={})


def test_Ridge():
    regress = regression(method=['Ridge'], yrange=[0.0, 100.0],
                         params=[{'alpha': 1.0,
                                  'copy_X': True,
                                  'fit_intercept': True,
                                  'max_iter': 'None',
                                  'normalize': False,
                                  'solver': 'auto',
                                  'tol': 0.0,
                                  'random_state': ''}],
                         ransacparams={})


def test_Bayesian_Ridge():
    regress = regression(method=['Bayesian Ridge'], yrange=[0.0, 100.0],
                         params=[{'n_iter': 300,
                                  'tol': 0.001,
                                  'alpha_1': 0.001,
                                  'alpha_2': 1e-06,
                                  'lambda_1': 1e-06,
                                  'lambda_2': 1e-06,
                                  'compute_score': False,
                                  'fit_intercept': True,
                                  'normalize': False,
                                  'copy_X': True,
                                  'verbose': False}], ransacparams={})


def test_ARD():
    regress = regression(method=['ARD'], yrange=[0.0, 100.0],
                         params=[{'n_iter': 300,
                                  'tol': 0.001,
                                  'alpha_1': 0.001,
                                  'alpha_2': 1e-06,
                                  'lambda_1': 1e-06,
                                  'lambda_2': 1e-06,
                                  'compute_score': False,
                                  'threshold_lambda': 100000,
                                  'fit_intercept': True,
                                  'normalize': False,
                                  'copy_X': True,
                                  'verbose': False}],
                         ransacparams={})


def test_LARS():
    regress = regression(method=['LARS'], yrange=[0.0, 100.0],
                         params=[{'n_nonzero_coefs': 500,
                                  'fit_intercept': True,
                                  'positive': False,
                                  'verbose': False,
                                  'normalize': False,
                                  'precompute': True,
                                  'copy_X': True,
                                  'eps': 2.220445,
                                  'fit_path': True}], ransacparams={})


def test_Lasso_LARS():
    regress = regression(method=['Lasso LARS'], yrange=[0.0, 100.0],
                         params=[{'alpha': 0.0,
                                  'fit_intercept': True,
                                  'positive': False,
                                  'verbose': False,
                                  'normalize': True,
                                  'copy_X': True,
                                  'precompute': 'Auto',
                                  'max_iter': 500,
                                  'eps': 2.220446,
                                  'fit_path': True}], ransacparams={})


def test_SVR():
    regress = regression(method=['SVR'], yrange=[0.0, 100.0], params=[{'C': 1.0,
                                                                       'epsilon': 0.1,
                                                                       'kernel': 'rbf',
                                                                       'degree': 0,
                                                                       'gamma': 'auto',
                                                                       'coef0': 0.0,
                                                                       'shrinking': False,
                                                                       'tol': 0.001,
                                                                       'cache_size': 200,
                                                                       'verbose': False,
                                                                       'max_iter': -1}], ransacparams={})


def test_KRR():
    regress = regression(method=['KRR'], yrange=[0.0, 100.0],
                         params=[{'alpha': 0,
                                  'kernel': 'linear',
                                  'gamma': 'None',
                                  'degree': 3.0,
                                  'coef0': 1.0,
                                  'kernel_params': 'None'}], ransacparams={})


test_PLS()
test_GP()
test_OLS()
test_OMP()
test_Lasso()
test_Elastic_Net()
test_Ridge()
test_Bayesian_Ridge()
test_ARD()
test_LARS()
test_Lasso_LARS()
test_SVR()
test_KRR()
