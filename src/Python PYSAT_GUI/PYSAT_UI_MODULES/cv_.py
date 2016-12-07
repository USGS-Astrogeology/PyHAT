from PYSAT_UI_MODULES.Error_ import error_print
from PyQt4 import QtCore, QtGui


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


class cv_:
    def __init__(self, pysat_fun, verticalLayout_8):
        self.pysat_fun = pysat_fun
        self.verticalLayout_8 = verticalLayout_8
        self.main()

    def main(self):
        self.pysat_fun.set_fun_list(self.pysat_fun.do_cv_train)
        self.pysat_fun.set_arg_list([])
        self.pysat_fun.set_kw_list({})
        self.cv_ui()
        self.cv_choosealg.currentIndexChanged.connect(lambda: self.make_reg_widget(self.cv_choosealg.currentText()))
         
              
    def get_cv_parameters(self):
        
        method=self.cv_choosealg.currentText()
        datakey=self.cv_choosedata.currentText()
        xvars=[str(x.text()) for x in self.cv_train_choosex.selectedItems()]
        yvars=[('comp',str(y.text())) for y in self.cv_train_choosey.selectedItems()]
        params={}
        kws={}        
        try:
            if method=='PLS':
                nc=self.reg_widget.pls_nc_lineedit.text().split(',')
                nc=[int(i) for i in nc]                
                params={'n_components':nc,
                        'scale':[False]}
                #modelkey=[method+' (nc='+str(i)+')' for i in self.reg_widget.pls_nc_lineedit.text().split(',')]
                
            if method=='GP':
                nc=[int(i) for i in self.reg_widget.gp_dim_red_nc_lineedit.text().split(',')]
                random_start=[int(i) for i in self.reg_widget.gp_rand_starts_lineedit.text().split(',')]
                theta0=[float(i) for i in self.reg_widget.gp_theta0_lineedit.text().split(',')]
                thetaL=[float(i) for i in self.reg_widget.gp_thetaL_lineedit.text().split(',')]
                thetaU=[float(i) for i in self.reg_widget.gp_thetaU_lineedit.text().split(',')]
                
                params={'reduce_dim':self.reg_widget.gp_dim_red_lineedit.text().split(','),
                        'n_components':nc,
                        'random_start':random_start,
                        'theta0':theta0,
                        'thetaL':thetaL,
                        'thetaU':thetaU}
                
        except:
            pass

        
        args=[datakey,xvars,yvars,method,params]
        self.pysat_fun.set_arg_list(args,replacelast=True)
        self.pysat_fun.set_kw_list(kws,replacelast=True)
        
        
    def make_reg_widget(self, alg):
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
            self.reg_widget.pls_nc_lineedit = QtGui.QLineEdit(self.reg_widget)
            self.reg_widget.pls_hlayout.addWidget(self.reg_widget.pls_nc_lineedit)
            self.reg_widget.pls_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            self.reg_widget.pls_hlayout.addItem(self.reg_widget.pls_spacer)
            self.reg_widget.pls_nc_lineedit.textChanged.connect(lambda: self.get_cv_parameters())
            
        elif alg == 'GP':
            self.reg_widget = QtGui.QWidget()
            self.reg_widget.gp_vlayout = QtGui.QVBoxLayout(self.reg_widget)
            self.reg_widget.gp_dim_red_hlayout = QtGui.QHBoxLayout()
            self.reg_widget.gp_dim_red_label = QtGui.QLabel(self.reg_widget)
            self.reg_widget.gp_dim_red_label.setText('Choose dimensionality reduction method:')
            self.reg_widget.gp_dim_red_hlayout.addWidget(self.reg_widget.gp_dim_red_label)
            self.reg_widget.gp_dim_red_lineedit = QtGui.QLineEdit(self.reg_widget)
            self.reg_widget.gp_dim_red_lineedit.setText('PCA')
            self.reg_widget.gp_dim_red_hlayout.addWidget(self.reg_widget.gp_dim_red_lineedit)
            self.reg_widget.gp_dim_red_nc_label = QtGui.QLabel()
            self.reg_widget.gp_dim_red_nc_label.setText('# of components:')
            self.reg_widget.gp_dim_red_hlayout.addWidget(self.reg_widget.gp_dim_red_nc_label)
            self.reg_widget.gp_dim_red_nc_lineedit = QtGui.QLineEdit(self.reg_widget)
            self.reg_widget.gp_dim_red_nc_lineedit.setText('10')
            self.reg_widget.gp_dim_red_hlayout.addWidget(self.reg_widget.gp_dim_red_nc_lineedit)
            
            self.reg_widget.gp_vlayout.addLayout(self.reg_widget.gp_dim_red_hlayout)
            self.reg_widget.gp_rand_starts_hlayout = QtGui.QHBoxLayout()
            self.reg_widget.gp_rand_starts_label = QtGui.QLabel(self.reg_widget)
            self.reg_widget.gp_rand_starts_label.setText('# of random starts:')
            self.reg_widget.gp_rand_starts_hlayout.addWidget(self.reg_widget.gp_rand_starts_label)
            self.reg_widget.gp_rand_starts_lineedit = QtGui.QLineEdit(self.reg_widget)
            self.reg_widget.gp_rand_starts_lineedit.setText('1')
            
            self.reg_widget.gp_rand_starts_hlayout.addWidget(self.reg_widget.gp_rand_starts_lineedit)
            self.reg_widget.spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            self.reg_widget.gp_rand_starts_hlayout.addItem(self.reg_widget.spacerItem4)
            self.reg_widget.gp_vlayout.addLayout(self.reg_widget.gp_rand_starts_hlayout)
            self.reg_widget.gp_theta_vlayout = QtGui.QVBoxLayout()
            self.reg_widget.gp_theta0_label = QtGui.QLabel(self.reg_widget)
            self.reg_widget.gp_theta0_label.setText('Starting Theta:')
            self.reg_widget.gp_theta_vlayout.addWidget(self.reg_widget.gp_theta0_label)
            self.reg_widget.gp_theta0_lineedit = QtGui.QLineEdit(self.reg_widget)
            self.reg_widget.gp_theta0_lineedit.setText('1.0')
            self.reg_widget.gp_theta_vlayout.addWidget(self.reg_widget.gp_theta0_lineedit)
            self.reg_widget.gp_thetaL_label = QtGui.QLabel(self.reg_widget)
            self.reg_widget.gp_thetaL_label.setText('Lower bound on Theta:')
            self.reg_widget.gp_theta_vlayout.addWidget(self.reg_widget.gp_thetaL_label)
            self.reg_widget.gp_thetaL_lineedit = QtGui.QLineEdit(self.reg_widget)
            self.reg_widget.gp_thetaL_lineedit.setText('0.1')
            self.reg_widget.gp_theta_vlayout.addWidget(self.reg_widget.gp_thetaL_lineedit)
            self.reg_widget.gp_thetaU_label = QtGui.QLabel(self.reg_widget)
            self.reg_widget.gp_thetaU_label.setText('Upper bound on Theta:')
            self.reg_widget.gp_theta_vlayout.addWidget(self.reg_widget.gp_thetaU_label)
            self.reg_widget.gp_thetaU_lineedit = QtGui.QLineEdit(self.reg_widget)
            self.reg_widget.gp_thetaU_lineedit.setText('100.0')

            self.reg_widget.gp_theta_vlayout.addWidget(self.reg_widget.gp_thetaU_lineedit)
            self.reg_widget.spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            self.reg_widget.gp_theta_vlayout.addItem(self.reg_widget.spacerItem5)
            self.reg_widget.gp_vlayout.addLayout(self.reg_widget.gp_theta_vlayout)
            
            self.reg_widget.gp_dim_red_lineedit.textChanged.connect(lambda: self.get_cv_parameters())
            self.reg_widget.gp_dim_red_nc_lineedit.textChanged.connect(lambda: self.get_cv_parameters())
            self.reg_widget.gp_rand_starts_lineedit.textChanged.connect(lambda: self.get_cv_parameters())
            self.reg_widget.gp_theta0_lineedit.textChanged.connect(lambda: self.get_cv_parameters())
            self.reg_widget.gp_thetaL_lineedit.textChanged.connect(lambda: self.get_cv_parameters())
            self.reg_widget.gp_thetaU_lineedit.textChanged.connect(lambda: self.get_cv_parameters())
            
        self.cv_vlayout.addWidget(self.reg_widget)

    def cv_ui(self):
        self.cv_train = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cv_train.setFont(font)
        self.cv_train.setObjectName(_fromUtf8("cv_train"))
        self.cv_vlayout = QtGui.QVBoxLayout(self.cv_train)
        self.cv_vlayout.setObjectName(_fromUtf8("cv_vlayout"))
        # choose data
        self.cv_choosedata_hlayout = QtGui.QHBoxLayout()
        self.cv_choosedata_hlayout.setObjectName(_fromUtf8("cv_choosedata_hlayout"))
        self.cv_train_choosedata_label = QtGui.QLabel(self.cv_train)
        self.cv_train_choosedata_label.setObjectName(_fromUtf8("cv_train_choosedata_label"))
        self.cv_train_choosedata_label.setText(_translate("cv_train", "Choose data:", None))
        self.cv_choosedata_hlayout.addWidget(self.cv_train_choosedata_label)
        datachoices = self.pysat_fun.datakeys
        if datachoices == []:
            error_print('No Data has been loaded')
            datachoices = ['No data has been loaded!']
        self.cv_choosedata = make_combobox(datachoices)
        self.cv_choosedata.setIconSize(QtCore.QSize(50, 20))
        self.cv_choosedata.setObjectName(_fromUtf8("cv_choosedata"))
        self.cv_choosedata_hlayout.addWidget(self.cv_choosedata)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.cv_choosedata_hlayout.addItem(spacerItem)
        self.cv_vlayout.addLayout(self.cv_choosedata_hlayout)
        # choose variables
        self.cv_choosevars_hlayout = QtGui.QHBoxLayout()
        self.cv_choosevars_hlayout.setObjectName(_fromUtf8("cv_choosevars_hlayout"))
        self.cv_train_choosex_label = QtGui.QLabel(self.cv_train)
        self.cv_train_choosex_label.setObjectName(_fromUtf8("cv_train_choosex_label"))
        self.cv_choosevars_hlayout.addWidget(self.cv_train_choosex_label)

        xvarchoices = self.pysat_fun.data[self.cv_choosedata.currentText()].df.columns.levels[0].values
        self.cv_train_choosex = make_listwidget(xvarchoices)
        self.cv_train_choosex.setObjectName(_fromUtf8("cv_train_choosex"))
        self.cv_choosevars_hlayout.addWidget(self.cv_train_choosex)
        self.cv_train_choosey_label = QtGui.QLabel(self.cv_train)
        self.cv_train_choosey_label.setObjectName(_fromUtf8("cv_train_choosey_label"))
        self.cv_choosevars_hlayout.addWidget(self.cv_train_choosey_label)
        try:
            yvarchoices = self.pysat_fun.data[self.cv_choosedata.currentText()].df['comp'].columns.values
        except:
            yvarchoices=['No valid options']
        self.cv_train_choosey = make_listwidget(yvarchoices)
        self.cv_choosevars_hlayout.addWidget(self.cv_train_choosey)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.cv_choosevars_hlayout.addItem(spacerItem1)
        self.cv_vlayout.addLayout(self.cv_choosevars_hlayout)

        # ransac options
        self.ransac_hlayout = QtGui.QHBoxLayout()
        self.cv_ransac_checkbox = QtGui.QCheckBox(self.cv_train)
        self.cv_ransac_checkbox.setObjectName(_fromUtf8("cv_ransac_checkbox"))
        self.cv_ransac_checkbox.setText('RANSAC')
        self.ransac_hlayout.addWidget(self.cv_ransac_checkbox)
        self.cv_vlayout.addLayout(self.ransac_hlayout)

        # choose cv algorithm
        self.cv_choosealg_hlayout = QtGui.QHBoxLayout()
        self.cv_choosealg_hlayout.setObjectName(_fromUtf8("cv_choosealg_hlayout"))
        self.cv_choosealg_label = QtGui.QLabel(self.cv_train)
        self.cv_choosealg_label.setObjectName(_fromUtf8("cv_choosealg_label"))
        self.cv_choosealg_hlayout.addWidget(self.cv_choosealg_label)
        self.cv_alg_choices = ['Choose an algorithm', 'PLS', 'GP', 'More to come...']
        self.cv_choosealg = make_combobox(self.cv_alg_choices)
        self.cv_choosealg.setIconSize(QtCore.QSize(50, 20))
        self.cv_choosealg.setObjectName(_fromUtf8("cv_choosealg"))
        self.cv_choosealg_hlayout.addWidget(self.cv_choosealg)
        cv_choosealg_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                        QtGui.QSizePolicy.Minimum)
        self.cv_choosealg_hlayout.addItem(cv_choosealg_spacer)
        self.cv_vlayout.addLayout(self.cv_choosealg_hlayout)

        self.verticalLayout_8.addWidget(self.cv_train)
        self.cv_train.raise_()
        self.cv_train.setTitle(_translate("cv_train", "Cross Validation / Training", None))
        
        self.cv_choosedata.currentIndexChanged.connect(lambda: self.get_cv_parameters())
        self.cv_choosealg.currentIndexChanged.connect(lambda: self.get_cv_parameters())
        self.cv_train_choosex.currentItemChanged.connect(lambda: self.get_cv_parameters())
        self.cv_train_choosey.currentItemChanged.connect(lambda: self.get_cv_parameters())
        self.cv_choosedata.activated[int].connect(lambda: self.cv_change_vars(self.cv_train_choosey))
        
    def cv_change_vars(self, obj):
        obj.clear()
        try:
            choices = self.pysat_fun.data[self.cv_choosedata.currentText()].df[['comp']].columns.values
        except:
            choices=['No valid options']
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
