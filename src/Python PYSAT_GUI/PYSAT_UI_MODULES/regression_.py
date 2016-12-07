from PYSAT_UI_MODULES.Error_ import error_print
from PyQt4 import QtCore, QtGui
import inspect

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class regression_:
    def __init__(self, pysat_fun, verticalLayout_8):
        self.pysat_fun = pysat_fun
        self.verticalLayout_8 = verticalLayout_8
        self.main()

    def main(self):
        self.pysat_fun.set_fun_list(self.pysat_fun.do_regression_train)
        self.pysat_fun.set_arg_list([])
        self.pysat_fun.set_kw_list({})
        self.regression_ui()
        self.regression_ransac_checkbox.toggled.connect(
            lambda: self.make_ransac_widget(self.regression_ransac_checkbox.isChecked()))
        self.regression_choosealg.currentIndexChanged.connect(
            lambda: self.make_regression_widget(self.regression_choosealg.currentText()))

    def get_regression_parameters(self):

        method = self.regression_choosealg.currentText()
        datakey = self.regression_choosedata.currentText()
        xvars = [str(x.text()) for x in self.regression_train_choosex.selectedItems()]
        yvars = [('comp', str(y.text())) for y in self.regression_train_choosey.selectedItems()]
        params = {}
        ransacparams = {}
        kws = {}
        try:
            if method == 'PLS':
                params = {'n_components': self.reg_widget.pls_nc_spinbox.value(),
                          'scale': False}
                modelkey = method + ' (nc=' + str(self.reg_widget.pls_nc_spinbox.value()) + ')'
                kws = {'modelkey': modelkey}
            if method == 'GP':
                params = {'reduce_dim': self.reg_widget.gp_dim_red_combobox.currentText(),
                          'n_components': self.reg_widget.gp_dim_red_nc_spinbox.value(),
                          'random_start': self.reg_widget.gp_rand_starts_spin.value(),
                          'theta0': self.reg_widget.gp_theta0_spin.value(),
                          'thetaL': self.reg_widget.gp_thetaL_spin.value(),
                          'thetaU': self.reg_widget.gp_thetaU_spin.value()}
                modelkey = method  # TODO: make this somehow concisely summarize the GP parameters in a string label for the model
                kws = {'modelkey': modelkey}
        except:
            pass
        if self.regression_ransac_checkbox.isChecked():
            lossval = self.ransac_widget.ransac_lossfunc_combobox.currentText()
            if lossval == 'Squared Error':
                loss = 'squared_loss'
            if lossval == 'Absolute Error':
                loss = 'absolute_loss'
            ransacparams = {'residual_threshold': self.ransac_widget.ransac_thresh_spin.value(),
                            'loss': loss}

        args = [datakey, xvars, yvars, method, params, ransacparams]
        self.pysat_fun.set_arg_list(args, replacelast=True)
        self.pysat_fun.set_kw_list(kws, replacelast=True)

    def make_ransac_widget(self, isChecked):
        if not isChecked:
            self.ransac_widget.deleteLater()
        else:
            self.ransac_widget = QtGui.QWidget()
            self.ransac_widget.ransac_widget_hlayout = QtGui.QHBoxLayout(self.ransac_widget)
            self.ransac_widget.ransac_lossfunc_hlayout = QtGui.QHBoxLayout()
            self.ransac_widget.ransac_lossfunc_label = QtGui.QLabel(self.ransac_widget)
            self.ransac_widget.ransac_lossfunc_label.setText('Loss function:')
            self.ransac_widget.ransac_lossfunc_hlayout.addWidget(self.ransac_widget.ransac_lossfunc_label)
            self.ransac_widget.ransac_lossfunc_combobox = QtGui.QComboBox(self.ransac_widget)
            self.ransac_widget.ransac_lossfunc_combobox.addItem(_fromUtf8("Squared Error"))
            self.ransac_widget.ransac_lossfunc_combobox.addItem(_fromUtf8("Absolute Error"))
            self.ransac_widget.ransac_lossfunc_hlayout.addWidget(self.ransac_widget.ransac_lossfunc_combobox)
            self.ransac_widget.ransac_lossfunc_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                                          QtGui.QSizePolicy.Minimum)
            self.ransac_widget.ransac_lossfunc_hlayout.addItem(self.ransac_widget.ransac_lossfunc_spacer)
            self.ransac_widget.ransac_widget_hlayout.addLayout(self.ransac_widget.ransac_lossfunc_hlayout)
            self.ransac_widget.ransac_thresh_hlayout = QtGui.QHBoxLayout()
            self.ransac_widget.ransac_thresh_label = QtGui.QLabel(self.ransac_widget)
            self.ransac_widget.ransac_thresh_label.setText('Threshold:')
            self.ransac_widget.ransac_thresh_hlayout.addWidget(self.ransac_widget.ransac_thresh_label)
            self.ransac_widget.ransac_thresh_spin = QtGui.QDoubleSpinBox(self.ransac_widget)
            self.ransac_widget.ransac_thresh_hlayout.addWidget(self.ransac_widget.ransac_thresh_spin)
            self.ransac_widget.ransac_thresh_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                                        QtGui.QSizePolicy.Minimum)
            self.ransac_widget.ransac_thresh_hlayout.addItem(self.ransac_widget.ransac_thresh_spacer)
            self.ransac_widget.ransac_widget_hlayout.addLayout(self.ransac_widget.ransac_thresh_hlayout)
            self.ransac_hlayout.addWidget(self.ransac_widget)

            self.ransac_widget.ransac_lossfunc_combobox.currentIndexChanged.connect(
                lambda: self.get_regression_parameters())
            self.ransac_widget.ransac_thresh_spin.valueChanged.connect(lambda: self.get_regression_parameters())

    def make_regression_widget(self, alg):
        print(alg)
        try:
            self.reg_widget.deleteLater()
        except:
            pass
        self.reg_widget = QtGui.QWidget()
        if alg == 'PLS':
            self.reg_widget.pls_hlayout = QtGui.QHBoxLayout(self.reg_widget)
            self.reg_widget.pls_nc_label = QtGui.QLabel(self.reg_widget)
            self.reg_widget.pls_nc_label.setText('# of components:')
            self.reg_widget.pls_hlayout.addWidget(self.reg_widget.pls_nc_label)
            self.reg_widget.pls_nc_spinbox = QtGui.QSpinBox(self.reg_widget)
            self.reg_widget.pls_hlayout.addWidget(self.reg_widget.pls_nc_spinbox)
            self.reg_widget.pls_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                           QtGui.QSizePolicy.Minimum)
            self.reg_widget.pls_hlayout.addItem(self.reg_widget.pls_spacer)
            self.reg_widget.pls_nc_spinbox.valueChanged.connect(lambda: self.get_regression_parameters())

        elif alg == 'GP':
            self.reg_widget = QtGui.QWidget()
            self.reg_widget.gp_vlayout = QtGui.QVBoxLayout(self.reg_widget)
            self.reg_widget.gp_dim_red_hlayout = QtGui.QHBoxLayout()
            self.reg_widget.gp_dim_red_label = QtGui.QLabel(self.reg_widget)
            self.reg_widget.gp_dim_red_label.setText('Choose dimensionality reduction method:')
            self.reg_widget.gp_dim_red_hlayout.addWidget(self.reg_widget.gp_dim_red_label)
            self.reg_widget.gp_dim_red_combobox = QtGui.QComboBox(self.reg_widget)
            self.reg_widget.gp_dim_red_combobox.addItem(_fromUtf8("PCA"))
            self.reg_widget.gp_dim_red_combobox.addItem(_fromUtf8("ICA"))
            self.reg_widget.gp_dim_red_hlayout.addWidget(self.reg_widget.gp_dim_red_combobox)
            self.reg_widget.gp_dim_red_nc_label = QtGui.QLabel()
            self.reg_widget.gp_dim_red_nc_label.setText('# of components:')
            self.reg_widget.gp_dim_red_hlayout.addWidget(self.reg_widget.gp_dim_red_nc_label)
            self.reg_widget.gp_dim_red_nc_spinbox = QtGui.QSpinBox(self.reg_widget)
            self.reg_widget.gp_dim_red_hlayout.addWidget(self.reg_widget.gp_dim_red_nc_spinbox)

            self.reg_widget.gp_vlayout.addLayout(self.reg_widget.gp_dim_red_hlayout)
            self.reg_widget.gp_rand_starts_hlayout = QtGui.QHBoxLayout()
            self.reg_widget.gp_rand_starts_label = QtGui.QLabel(self.reg_widget)
            self.reg_widget.gp_rand_starts_label.setText('# of random starts:')
            self.reg_widget.gp_rand_starts_hlayout.addWidget(self.reg_widget.gp_rand_starts_label)
            self.reg_widget.gp_rand_starts_spin = QtGui.QSpinBox(self.reg_widget)
            self.reg_widget.gp_rand_starts_spin.setValue(1)
            self.reg_widget.gp_rand_starts_hlayout.addWidget(self.reg_widget.gp_rand_starts_spin)
            self.reg_widget.spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                            QtGui.QSizePolicy.Minimum)
            self.reg_widget.gp_rand_starts_hlayout.addItem(self.reg_widget.spacerItem4)
            self.reg_widget.gp_vlayout.addLayout(self.reg_widget.gp_rand_starts_hlayout)
            self.reg_widget.gp_theta_vlayout = QtGui.QVBoxLayout()
            self.reg_widget.gp_theta0_label = QtGui.QLabel(self.reg_widget)
            self.reg_widget.gp_theta0_label.setText('Starting Theta:')
            self.reg_widget.gp_theta_vlayout.addWidget(self.reg_widget.gp_theta0_label)
            self.reg_widget.gp_theta0_spin = QtGui.QDoubleSpinBox(self.reg_widget)
            self.reg_widget.gp_theta0_spin.setValue(1.0)
            self.reg_widget.gp_theta_vlayout.addWidget(self.reg_widget.gp_theta0_spin)
            self.reg_widget.gp_thetaL_label = QtGui.QLabel(self.reg_widget)
            self.reg_widget.gp_thetaL_label.setText('Lower bound on Theta:')
            self.reg_widget.gp_theta_vlayout.addWidget(self.reg_widget.gp_thetaL_label)
            self.reg_widget.gp_thetaL_spin = QtGui.QDoubleSpinBox(self.reg_widget)
            self.reg_widget.gp_thetaL_spin.setValue(0.1)
            self.reg_widget.gp_theta_vlayout.addWidget(self.reg_widget.gp_thetaL_spin)
            self.reg_widget.gp_thetaU_label = QtGui.QLabel(self.reg_widget)
            self.reg_widget.gp_thetaU_label.setText('Upper bound on Theta:')
            self.reg_widget.gp_theta_vlayout.addWidget(self.reg_widget.gp_thetaU_label)
            self.reg_widget.gp_thetaU_spin = QtGui.QDoubleSpinBox(self.reg_widget)
            self.reg_widget.gp_thetaU_spin.setMaximum(10000)
            self.reg_widget.gp_thetaU_spin.setValue(100.0)

            self.reg_widget.gp_theta_vlayout.addWidget(self.reg_widget.gp_thetaU_spin)
            self.reg_widget.spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                            QtGui.QSizePolicy.Minimum)
            self.reg_widget.gp_theta_vlayout.addItem(self.reg_widget.spacerItem5)
            self.reg_widget.gp_vlayout.addLayout(self.reg_widget.gp_theta_vlayout)

            self.reg_widget.gp_dim_red_combobox.currentIndexChanged.connect(lambda: self.get_regression_parameters())
            self.reg_widget.gp_dim_red_nc_spinbox.valueChanged.connect(lambda: self.get_regression_parameters())
            self.reg_widget.gp_rand_starts_spin.valueChanged.connect(lambda: self.get_regression_parameters())
            self.reg_widget.gp_theta0_spin.valueChanged.connect(lambda: self.get_regression_parameters())
            self.reg_widget.gp_thetaL_spin.valueChanged.connect(lambda: self.get_regression_parameters())
            self.reg_widget.gp_thetaU_spin.valueChanged.connect(lambda: self.get_regression_parameters())

        self.regression_vlayout.addWidget(self.reg_widget)

    def regression_ui(self):
        self.regression_train = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.regression_train.setFont(font)
        self.regression_train.setObjectName(_fromUtf8("regression_train"))
        self.regression_vlayout = QtGui.QVBoxLayout(self.regression_train)
        self.regression_vlayout.setObjectName(_fromUtf8("regression_vlayout"))
        # choose data
        self.regression_choosedata_hlayout = QtGui.QHBoxLayout()
        self.regression_choosedata_hlayout.setObjectName(_fromUtf8("regression_choosedata_hlayout"))
        self.regression_train_choosedata_label = QtGui.QLabel(self.regression_train)
        self.regression_train_choosedata_label.setObjectName(_fromUtf8("regression_train_choosedata_label"))
        self.regression_train_choosedata_label.setText(_translate("regression_train", "Choose data:", None))
        self.regression_choosedata_hlayout.addWidget(self.regression_train_choosedata_label)
        datachoices = self.pysat_fun.datakeys
        datachoices=[i for i in datachoices if i!='CV Results']  #prevent CV results from showing up as an option
        if datachoices == []:
            error_print('No Data has been loaded')
            datachoices = ['No data has been loaded!']
        self.regression_choosedata = make_combobox(datachoices)
        self.regression_choosedata.setIconSize(QtCore.QSize(50, 20))
        self.regression_choosedata.setObjectName(_fromUtf8("regression_choosedata"))
        self.regression_choosedata_hlayout.addWidget(self.regression_choosedata)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.regression_choosedata_hlayout.addItem(spacerItem)
        self.regression_vlayout.addLayout(self.regression_choosedata_hlayout)
        # choose variables
        self.regression_choosevars_hlayout = QtGui.QHBoxLayout()
        self.regression_choosevars_hlayout.setObjectName(_fromUtf8("regression_choosevars_hlayout"))
        self.regression_train_choosex_label = QtGui.QLabel(self.regression_train)
        self.regression_train_choosex_label.setObjectName(_fromUtf8("regression_train_choosex_label"))
        self.regression_choosevars_hlayout.addWidget(self.regression_train_choosex_label)

        xvarchoices = self.pysat_fun.data[self.regression_choosedata.currentText()].df.columns.levels[0].values

        self.regression_train_choosex = make_listwidget(xvarchoices)
        self.regression_train_choosex.setObjectName(_fromUtf8("regression_train_choosex"))
        self.regression_choosevars_hlayout.addWidget(self.regression_train_choosex)
        self.regression_train_choosey_label = QtGui.QLabel(self.regression_train)
        self.regression_train_choosey_label.setObjectName(_fromUtf8("regression_train_choosey_label"))
        self.regression_choosevars_hlayout.addWidget(self.regression_train_choosey_label)
        yvarchoices = self.pysat_fun.data[self.regression_choosedata.currentText()].df['comp'].columns.values

        self.regression_train_choosey = make_listwidget(yvarchoices)
        self.regression_choosevars_hlayout.addWidget(self.regression_train_choosey)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.regression_choosevars_hlayout.addItem(spacerItem1)
        self.regression_vlayout.addLayout(self.regression_choosevars_hlayout)

        # ransac options
        self.ransac_hlayout = QtGui.QHBoxLayout()
        self.regression_ransac_checkbox = QtGui.QCheckBox(self.regression_train)
        self.regression_ransac_checkbox.setObjectName(_fromUtf8("regression_ransac_checkbox"))
        self.regression_ransac_checkbox.setText('RANSAC')
        self.ransac_hlayout.addWidget(self.regression_ransac_checkbox)
        self.regression_vlayout.addLayout(self.ransac_hlayout)

        # choose regression algorithm
        self.regression_choosealg_hlayout = QtGui.QHBoxLayout()
        self.regression_choosealg_hlayout.setObjectName(_fromUtf8("regression_choosealg_hlayout"))
        self.regression_choosealg_label = QtGui.QLabel(self.regression_train)
        self.regression_choosealg_label.setObjectName(_fromUtf8("regression_choosealg_label"))
        self.regression_choosealg_hlayout.addWidget(self.regression_choosealg_label)
        self.regression_alg_choices = ['Choose an algorithm', 'PLS', 'GP', 'More to come...']
        self.regression_choosealg = make_combobox(self.regression_alg_choices)
        self.regression_choosealg.setIconSize(QtCore.QSize(50, 20))
        self.regression_choosealg.setObjectName(_fromUtf8("regression_choosealg"))
        self.regression_choosealg_hlayout.addWidget(self.regression_choosealg)
        regression_choosealg_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                        QtGui.QSizePolicy.Minimum)
        self.regression_choosealg_hlayout.addItem(regression_choosealg_spacer)
        self.regression_vlayout.addLayout(self.regression_choosealg_hlayout)

        self.verticalLayout_8.addWidget(self.regression_train)
        self.regression_train.raise_()
        self.regression_train.setTitle(_translate("regression_train", "Regression - Train", None))

        self.regression_choosedata.currentIndexChanged.connect(lambda: self.get_regression_parameters())
        self.regression_choosealg.currentIndexChanged.connect(lambda: self.get_regression_parameters())
        self.regression_train_choosex.currentItemChanged.connect(lambda: self.get_regression_parameters())
        self.regression_train_choosey.currentItemChanged.connect(lambda: self.get_regression_parameters())

        self.regression_choosedata.activated[int].connect(lambda: self.regression_change_vars(self.regression_train_choosey))
        
    def regression_change_vars(self, obj):
        obj.clear()
        choices = self.pysat_fun.data[self.regression_choosedata.currentText()].df[['comp']].columns.values
        for i in choices:
            obj.addItem(i[1])

def make_combobox(choices):
    combo = QtGui.QComboBox()

    for i, choice in enumerate(choices):
        combo.addItem(_fromUtf8(""))
        combo.setItemText(i, _translate('', choice, None))

    return combo


def make_listwidget(choices):
    listwidget = QtGui.QListWidget()
    listwidget.setItemDelegate
    for item in choices:
        item = QtGui.QListWidgetItem(item)
        listwidget.addItem(item)
    return listwidget
