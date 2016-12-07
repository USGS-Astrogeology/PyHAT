from pysat.spectral.spectral_data import spectral_data
from pysat.regression import regression
from pysat.regression import cv
from pysat.plotting.plots import make_plot, pca_ica_plot
import pandas as pd
from PYSAT_UI_MODULES.Error_ import error_print
from PyQt4.QtCore import QThread
from PyQt4 import QtCore


class pysat_func(QThread):
    taskFinished = QtCore.pyqtSignal()
    def __init__(self):
        QThread.__init__(self)
        self.leftOff = 0
        self.data = {}  # initialize with an empty dict to hold data frames
        self.datakeys = []
        self.models = {}
        self.modelkeys = []
        self.model_xvars = {}
        self.figs = {}
        self.fignames = []
        self.fun_list = []
        self.arg_list = []
        self.kw_list = []
        self.greyedItems = []

    """
    Getter and setter functions below
    """

    # TODO: combine these three functions into one, they're all doing the same thing!
    # TODO>> Re: we don't want to do that, because we're only updating a single value
    # TODO>> And good programming practices say that we should keep them separate,
    # TODO>> this the geneal rule for getters and setters
    def set_fun_list(self, fun, replacelast=False):
        if replacelast:
            self.fun_list[-1] = fun
        else:
            self.fun_list.append(fun)

    def set_arg_list(self, args, replacelast=False):
        if replacelast:
            self.arg_list[-1] = args
        else:
            self.arg_list.append(args)

    def set_kw_list(self, kws, replacelast=False):
        if replacelast:
            self.kw_list[-1] = kws
        else:
            self.kw_list.append(kws)

    def getDataKeys(self):
        return self.datakeys

    def getModelKeys(self):
        return self.modelkeys

    def getData(self):
        return self.data

    def getModels(self):
        return self.models

    def set_grey_items(self, items):
        self.greyedItems.append(items)

    """
    Work functions below
    """

    def set_file_outpath(self, outpath):
        try:
            self.outpath = outpath
            print("Output path folder has been set")
        except Exception as e:
            error_print(e)

    def get_data(self, filename, keyname):
        try:
            print('Loading data file: ' + str(filename))
            self.data[keyname] = spectral_data(pd.read_csv(filename, header=[0, 1]))
            self.datakeys.append(keyname)
            pass
        except Exception as e:
            error_print('Problem reading data: {}'.format(e))

    def removenull(self,datakey,colname):
        try:
            print(self.data[datakey].df.shape)
            self.data[datakey]=spectral_data(self.data[datakey].df.ix[-self.data[datakey].df[colname].isnull()])
            print(self.data[datakey].df.shape)

        except Exception as e:
            error_print(e)

    def do_mask(self, datakey, maskfile):
        try:
            self.data[datakey].mask(maskfile)
            print("Mask applied")
        except Exception as e:
            error_print(e)

    def do_interp(self, datakey_to_interp, datakey_ref):
        print(self.data[datakey_ref].df.columns.levels[0])
        try:
            self.data[datakey_to_interp].interp(self.data[datakey_ref].df['wvl'].columns)
        except Exception as e:
            error_print(e)

    def do_pca(self, datakey, nc, col, load_fit=None):
        print(self.data[datakey].df.columns.levels[0])
        try:
            self.data[datakey].pca(col, nc=nc, load_fit=load_fit)
        except Exception as e:
            error_print(e)

    def do_ica(self, datakey, nc, col, load_fit=None):
        try:
            self.data[datakey].ica(col, nc=nc, load_fit=load_fit)
        except Exception as e:
            error_print(e)

    def do_ica_jade(self, datakey, nc, col, load_fit=None, corrcols=None):
        try:
            self.data[datakey].ica_jade(col, nc=nc, load_fit=load_fit, corrcols=corrcols)
        except Exception as e:
            error_print(e)

    def do_norm(self, datakey, ranges):
        print("{}".format(ranges))
        try:
            print(self.data[datakey].df.columns.levels[0])
            self.data[datakey].norm(ranges)
            print(self.data[datakey].df.columns.levels[0])
            print("Normalization has been applied to the ranges: " + str(ranges))
        except Exception as e:
            error_print(e)

    def do_strat_folds(self, datakey, nfolds, testfold, colname):
        self.data[datakey].stratified_folds(nfolds=nfolds, sortby=colname)

        self.data[datakey + '-Train'] = self.data[datakey].rows_match(('meta', 'Folds'), [testfold], invert=True)
        self.data[datakey + '-Test'] = self.data[datakey].rows_match(('meta', 'Folds'), [testfold])
        self.datakeys = self.data.keys()

        print(self.data.keys())
        print(self.data[datakey + '-Test'].df.index.shape)
        print(self.data[datakey + '-Train'].df.index.shape)

    def do_regression_train(self, datakey, xvars, yvars, method, params, ransacparams, modelkey=None):
        try:
            if modelkey is None:
                modelkey = method
            self.models[modelkey] = regression.regression([method], [params], i=0, ransacparams=[ransacparams])
            self.modelkeys.append(modelkey)
            self.models[modelkey].fit(self.data[datakey].df[xvars], self.data[datakey].df[yvars])
            self.model_xvars[modelkey] = xvars

        except Exception as e:
            error_print(e)
          
    def do_cv_train(self, datakey, xvars, yvars, method, params):
        
        try:
            
            cv_obj=cv.cv(params)
            self.data[datakey].df,self.cv_results=cv_obj.do_cv(self.data[datakey].df,xcols=xvars,ycol=yvars)
            self.data['CV Results']=self.cv_results

        except Exception as e:
            error_print(e)
            

    def do_regression_predict(self, datakey, modelkey, predictname):
        try:
            prediction = self.models[modelkey].predict(self.data[datakey].df[self.model_xvars[modelkey]])
            self.data[datakey].df[predictname] = prediction
            pass
        except Exception as e:
            error_print(e)

    def do_plot(self, datakey,
                       xvar, yvar,
                       figfile=None, xrange=None,
                       yrange=None, xtitle='Reference (wt.%)',
                       ytitle='Prediction (wt.%)', title=None,
                       lbl=None, one_to_one=False,
                       dpi=1000, color=None,
                       annot_mask=None,
                       cmap=None, colortitle='', figname=None,masklabel='',
                       marker='o',linestyle='None'
                       ):

        try:
            x = self.data[datakey].df[xvar]
            y = self.data[datakey].df[yvar]
        except:
            x=self.data[datakey][xvar]
            y=self.data[datakey][yvar]
        try:
            loadfig = self.figs[figname]
        except:
            loadfig = None
            # outpath=self.outpath
        try:
            outpath = self.outpath
        except:
            outpath='./'
        self.figs[figname] = make_plot(x, y, outpath, figfile, xrange=xrange, yrange=yrange, xtitle=xtitle,
                                         ytitle=ytitle, title=title,
                                         lbl=lbl, one_to_one=one_to_one, dpi=dpi, color=color,
                                         annot_mask=annot_mask, cmap=cmap,
                                         colortitle=colortitle, loadfig=loadfig,marker=marker,linestyle=linestyle)

    def do_pca_ica_plot(self, datakey,
                        x_component,
                        y_component,
                        figfile,
                        colorvar=None,
                        cmap='viridis',
                        method='PCA'
                        ):
        pca_ica_plot(self.data[datakey], x_component, y_component, colorvar=colorvar, cmap=cmap, method=method,
                     figpath=self.outpath, figfile=figfile)

    def __del__(self):
        self.wait()

    def run(self):
        # TODO this function will take all the enumerated functions and parameters and run them
        for i in range(self.leftOff, len(self.fun_list)):
            print(self.fun_list[i])
            self.fun_list[i](*self.arg_list[i], **self.kw_list[i])
            self.leftOff = i + 1

        self.taskFinished.emit()
