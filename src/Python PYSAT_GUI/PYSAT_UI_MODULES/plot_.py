from PYSAT_UI_MODULES.Error_ import error_print
from PyQt4 import QtCore, QtGui
import numpy as np
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


class plot_:
    def __init__(self, pysat_fun, verticalLayout_8):
        self.pysat_fun = pysat_fun
        self.verticalLayout_8 = verticalLayout_8
        self.main()

    def main(self):
        self.pysat_fun.set_fun_list(self.pysat_fun.do_plot)
        self.pysat_fun.set_arg_list([])
        self.pysat_fun.set_kw_list({})
        self.plot_ui()

    def get_plot_parameters(self):

        datakey = self.plot_choosedata.currentText()
        xvar = self.xvar_choices.currentText()
        yvar = self.yvar_choices.currentText()
        try:
            xvar = (self.vars_level0[self.vars_level1.index(xvar)], xvar)
            yvar = (self.vars_level0[self.vars_level1.index(yvar)], yvar)
        except:
            print('Problem setting x and/or y variable!')
            pass
        figname = self.figname_text.text()
        title = self.plot_title_text.text()
        xrange = self.xmin_spin.value(), self.xmax_spin.value()
        yrange = self.ymin_spin.value(), self.ymax_spin.value()
        xtitle = self.xtitle_text.text()
        ytitle = self.ytitle_text.text()
        lbl = self.legend_label_text.text()
        one_to_one = self.onetoone.isChecked()
        figfile = self.file_text.text()
        
        color = self.color_choices.currentText()
        alpha=self.alpha_spin.value()    

        if color=='Red':
            color=[1,0,0,alpha]
        if color=='Green':
            color=[0,1,0,alpha]
        if color=='Blue':
            color=[0,0,1,alpha]
        if color=='Cyan':
            color=[0,1,1,alpha]
        if color=='Yellow':
            color=[1,1,0,alpha]
        if color=='Magenta':
            color=[1,0,1,alpha]
        if color=='Black':
            color=[0,0,0,alpha]

        
        marker=self.marker_choices.currentText()        
        if marker=='Circles':
            marker='o'
        if marker=='Squares':
            marker='s'
        if marker=='Diamonds':
            marker='D'
        if marker=='Triangle Up':
            marker='^'
        if marker=='Triangle Down':
            marker='v'
        if marker=='Triangle Right':
            marker='>'
        if marker=='Triangle Left':
            marker='<'
        
        
        line=self.line_choices.currentText()
        if line=='No Line':
            linestyle='None'
        if line=='Line':
            linestyle='-'
        if line=='Dashed Line':
            linestyle='--'
        if line=='Dotted Line':
            linestyle=':'
            
            
        args = [datakey, xvar, yvar]
        kws = {'figname': figname,
               'title': title,
               'xrange': xrange,
               'yrange': yrange,
               'xtitle': xtitle,
               'ytitle': ytitle,
               'lbl': lbl,
               'one_to_one': one_to_one,
               'figfile': figfile,
               'color': color,
               'marker': marker,
               'linestyle':linestyle
               }
        self.pysat_fun.set_arg_list(args, replacelast=True)
        self.pysat_fun.set_kw_list(kws, replacelast=True)

    def plot_ui(self):
        self.plot = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.plot.setFont(font)
        self.plot.setObjectName(_fromUtf8("plot"))
        self.plot_vlayout = QtGui.QVBoxLayout(self.plot)
        self.plot_vlayout.setMargin(11)
        self.plot_vlayout.setSpacing(6)
        self.plot_vlayout.setObjectName(_fromUtf8("plot_vlayout"))

        self.plot_choosedata_hlayout = QtGui.QHBoxLayout()
        self.plot_choosedata_hlayout.setMargin(11)
        self.plot_choosedata_hlayout.setSpacing(6)
        self.plot_choosedata_hlayout.setObjectName(_fromUtf8("plot_choosedata_hlayout"))

        self.plot_choosedata_label = QtGui.QLabel(self.plot)
        self.plot_choosedata_label.setObjectName(_fromUtf8("plot_choosedata_label"))
        self.plot_choosedata_label.setText('Choose data: ')
        self.plot_choosedata_hlayout.addWidget(self.plot_choosedata_label)

        datachoices = self.pysat_fun.datakeys
        if datachoices == []:
            error_print('No Data has been loaded')
            datachoices = ['No data has been loaded!']
        self.plot_choosedata = make_combobox(datachoices)
        self.plot_choosedata.setIconSize(QtCore.QSize(50, 20))
        self.plot_choosedata.setObjectName(_fromUtf8("plot_choosedata"))
        self.plot_choosedata_hlayout.addWidget(self.plot_choosedata)

        self.figname_label = QtGui.QLabel(self.plot)
        self.figname_label.setObjectName(_fromUtf8("figname_label"))
        self.figname_label.setText('Figure name: ')
        self.plot_choosedata_hlayout.addWidget(self.figname_label)
        self.figname_text = QtGui.QLineEdit(self.plot)
        self.figname_text.setObjectName(_fromUtf8("figname_text"))
        self.plot_choosedata_hlayout.addWidget(self.figname_text)
        self.plot_title_label = QtGui.QLabel(self.plot)
        self.plot_title_label.setObjectName(_fromUtf8("plot_title_label"))
        self.plot_title_label.setText('Plot title: ')
        self.plot_choosedata_hlayout.addWidget(self.plot_title_label)
        self.plot_title_text = QtGui.QLineEdit(self.plot)
        self.plot_title_text.setObjectName(_fromUtf8("plot_title_text"))
        self.plot_choosedata_hlayout.addWidget(self.plot_title_text)
        self.plot_vlayout.addLayout(self.plot_choosedata_hlayout)
        self.plot_choosevars_hlayout = QtGui.QHBoxLayout()
        self.plot_choosevars_hlayout.setMargin(11)
        self.plot_choosevars_hlayout.setSpacing(6)
        self.plot_choosevars_hlayout.setObjectName(_fromUtf8("plot_choosevars_hlayout"))

        self.plot_choosex_vlayout = QtGui.QVBoxLayout()
        self.plot_choosex_vlayout.setMargin(11)
        self.plot_choosex_vlayout.setSpacing(6)
        self.plot_choosex_vlayout.setObjectName(_fromUtf8("plot_choosex_vlayout"))
        self.plot_choosex_label = QtGui.QLabel(self.plot)
        self.plot_choosex_label.setObjectName(_fromUtf8("plot_choosex_label"))
        self.plot_choosex_label.setText('Choose X variable: ')
        self.plot_choosex_vlayout.addWidget(self.plot_choosex_label)
        try:
            self.vars_level0 = self.pysat_fun.data[self.plot_choosedata.currentText()].df.columns.get_level_values(0)
            self.vars_level1 = self.pysat_fun.data[self.plot_choosedata.currentText()].df.columns.get_level_values(1)
            self.vars_level1 = list(self.vars_level1[self.vars_level0 != 'wvl'])
            self.vars_level0 = list(self.vars_level0[self.vars_level0 != 'wvl'])

            xvarchoices = self.vars_level1
            pass
        except:
            xvarchoices = self.pysat_fun.data[self.plot_choosedata.currentText()].columns.values
        try:
            xvarchoices = [i for i in xvarchoices if not 'Unnamed' in i] #remove unnamed columns from choices
        except:
            pass
        self.xvar_choices = make_combobox(xvarchoices)
        self.xvar_choices.SizeAdjustPolicy(0)
        self.plot_choosex_vlayout.addWidget(self.xvar_choices)
        self.xtitle_hlayout = QtGui.QHBoxLayout()
        self.xtitle_hlayout.setMargin(11)
        self.xtitle_hlayout.setSpacing(6)
        self.xtitle_hlayout.setObjectName(_fromUtf8("xtitle_hlayout"))
        self.xtitle_label = QtGui.QLabel(self.plot)
        self.xtitle_label.setObjectName(_fromUtf8("xtitle_label"))
        self.xtitle_label.setText('X title: ')
        self.xtitle_hlayout.addWidget(self.xtitle_label)
        self.xtitle_text = QtGui.QLineEdit(self.plot)
        self.xtitle_text.setObjectName(_fromUtf8("xtitle_text"))
        self.xtitle_hlayout.addWidget(self.xtitle_text)
        self.plot_choosex_vlayout.addLayout(self.xtitle_hlayout)
        self.xrange_hlayout = QtGui.QHBoxLayout()
        self.xrange_hlayout.setMargin(11)
        self.xrange_hlayout.setSpacing(6)
        self.xrange_hlayout.setObjectName(_fromUtf8("xrange_hlayout"))
        self.xmin_label = QtGui.QLabel(self.plot)
        self.xmin_label.setObjectName(_fromUtf8("xmin_label"))
        self.xmin_label.setText('X min: ')
        self.xrange_hlayout.addWidget(self.xmin_label)
        self.xmin_spin = QtGui.QDoubleSpinBox(self.plot)
        self.xmin_spin.setObjectName(_fromUtf8("xmin_spin"))
        self.xmin_spin.setRange(-10000000, 10000000)
        self.xrange_hlayout.addWidget(self.xmin_spin)
        self.xmax_label = QtGui.QLabel(self.plot)
        self.xmax_label.setObjectName(_fromUtf8("xmax_label"))
        self.xmax_label.setText('X max: ')
        self.xrange_hlayout.addWidget(self.xmax_label)
        self.xmax_spin = QtGui.QDoubleSpinBox(self.plot)
        self.xmax_spin.setObjectName(_fromUtf8("xmax_spin"))
        self.xmax_spin.setRange(-10000000, 10000000)
        self.xrange_hlayout.addWidget(self.xmax_spin)
        self.plot_choosex_vlayout.addLayout(self.xrange_hlayout)
        self.plot_choosevars_hlayout.addLayout(self.plot_choosex_vlayout)

        self.plot_choosey_vlayout = QtGui.QVBoxLayout()
        self.plot_choosey_vlayout.setMargin(11)
        self.plot_choosey_vlayout.setSpacing(6)
        self.plot_choosey_vlayout.setObjectName(_fromUtf8("plot_choosey_vlayout"))
        self.plot_choosey_label = QtGui.QLabel(self.plot)
        self.plot_choosey_label.setObjectName(_fromUtf8("plot_choosey_label"))
        self.plot_choosey_label.setText('Choose Y variable: ')
        self.plot_choosey_vlayout.addWidget(self.plot_choosey_label)
        yvarchoices = xvarchoices
        self.yvar_choices = make_combobox(yvarchoices)
        self.yvar_choices.SizeAdjustPolicy(0)
        self.plot_choosey_vlayout.addWidget(self.yvar_choices)
        self.ytitle_hlayout = QtGui.QHBoxLayout()
        self.ytitle_hlayout.setMargin(11)
        self.ytitle_hlayout.setSpacing(6)
        self.ytitle_hlayout.setObjectName(_fromUtf8("ytitle_hlayout"))
        self.ytitle_label = QtGui.QLabel(self.plot)
        self.ytitle_label.setObjectName(_fromUtf8("ytitle_label"))
        self.ytitle_label.setText('Y title: ')
        self.ytitle_hlayout.addWidget(self.ytitle_label)
        self.ytitle_text = QtGui.QLineEdit(self.plot)
        self.ytitle_text.setObjectName(_fromUtf8("ytitle_text"))
        self.ytitle_hlayout.addWidget(self.ytitle_text)
        self.plot_choosey_vlayout.addLayout(self.ytitle_hlayout)
        self.yrange_hlayout = QtGui.QHBoxLayout()
        self.yrange_hlayout.setMargin(11)
        self.yrange_hlayout.setSpacing(6)
        self.yrange_hlayout.setObjectName(_fromUtf8("yrange_hlayout"))
        self.ymin_label = QtGui.QLabel(self.plot)
        self.ymin_label.setObjectName(_fromUtf8("ymin_label"))
        self.ymin_label.setText('Y min: ')
        self.yrange_hlayout.addWidget(self.ymin_label)
        self.ymin_spin = QtGui.QDoubleSpinBox(self.plot)
        self.ymin_spin.setObjectName(_fromUtf8("ymin_spin"))
        self.ymin_spin.setRange(-10000000, 10000000)
        self.yrange_hlayout.addWidget(self.ymin_spin)
        self.ymax_label = QtGui.QLabel(self.plot)
        self.ymax_label.setObjectName(_fromUtf8("ymax_label"))
        self.ymax_label.setText('Y max: ')
        self.yrange_hlayout.addWidget(self.ymax_label)
        self.ymax_spin = QtGui.QDoubleSpinBox(self.plot)
        self.ymax_spin.setObjectName(_fromUtf8("ymax_spin"))
        self.ymin_spin.setRange(-10000000, 10000000)
        self.yrange_hlayout.addWidget(self.ymax_spin)
        self.plot_choosey_vlayout.addLayout(self.yrange_hlayout)
        self.plot_choosevars_hlayout.addLayout(self.plot_choosey_vlayout)
        self.plot_vlayout.addLayout(self.plot_choosevars_hlayout)

        self.legend_hlayout = QtGui.QHBoxLayout()
        self.legend_hlayout.setMargin(11)
        self.legend_hlayout.setSpacing(6)
        self.legend_hlayout.setObjectName(_fromUtf8("legend_hlayout"))
        self.legend_label = QtGui.QLabel(self.plot)
        self.legend_label.setObjectName(_fromUtf8("legend_label"))
        self.legend_label.setText('Legend label: ')
        self.legend_hlayout.addWidget(self.legend_label)
        self.legend_label_text = QtGui.QLineEdit(self.plot)
        self.legend_label_text.setObjectName(_fromUtf8("legend_label_text"))
        self.legend_hlayout.addWidget(self.legend_label_text)
        self.onetoone = QtGui.QCheckBox(self.plot)
        self.onetoone.setObjectName(_fromUtf8("onetoone"))
        self.onetoone.setText('One to One')
        self.legend_hlayout.addWidget(self.onetoone)
        self.plot_vlayout.addLayout(self.legend_hlayout)
        
        self.plot_appearance_options = QtGui.QHBoxLayout()
        self.plot_appearance_options.setMargin(11)
        self.plot_appearance_options.setSpacing(6)
        self.plot_appearance_options.setObjectName(_fromUtf8("plot_appearance_options"))
        self.color_choices = QtGui.QComboBox(self.plot)
        self.color_choices.setIconSize(QtCore.QSize(50, 20))
        self.color_choices.setObjectName(_fromUtf8("color_choices"))
        self.color_choices.addItem(_fromUtf8("Red"))
        self.color_choices.addItem(_fromUtf8("Green"))
        self.color_choices.addItem(_fromUtf8("Blue"))
        self.color_choices.addItem(_fromUtf8("Cyan"))
        self.color_choices.addItem(_fromUtf8("Yellow"))
        self.color_choices.addItem(_fromUtf8("Magenta"))
        self.color_choices.addItem(_fromUtf8("Black"))
        self.plot_appearance_options.addWidget(self.color_choices)
        self.line_choices = QtGui.QComboBox(self.plot)
        self.line_choices.setIconSize(QtCore.QSize(50, 20))
        self.line_choices.setObjectName(_fromUtf8("line_choices"))
        self.line_choices.addItem(_fromUtf8("No Line"))
        self.line_choices.addItem(_fromUtf8("Line"))
        self.line_choices.addItem(_fromUtf8("Dashed Line"))
        self.line_choices.addItem(_fromUtf8("Dotted Line"))
        self.plot_appearance_options.addWidget(self.line_choices)
        
        self.marker_choices = QtGui.QComboBox(self.plot)
        self.marker_choices.setIconSize(QtCore.QSize(50, 20))
        self.marker_choices.setObjectName(_fromUtf8("marker_choices"))
        self.marker_choices.addItem(_fromUtf8("Circles"))
        self.marker_choices.addItem(_fromUtf8("Squares"))
        self.marker_choices.addItem(_fromUtf8("Diamonds"))
        self.marker_choices.addItem(_fromUtf8("Triangle Up"))
        self.marker_choices.addItem(_fromUtf8("Triangle Down"))
        self.marker_choices.addItem(_fromUtf8("Triangle Left"))
        self.marker_choices.addItem(_fromUtf8("Triangle Right"))
        self.marker_choices.addItem(_fromUtf8("None"))
        self.plot_appearance_options.addWidget(self.marker_choices)
        
                
        self.alpha_label = QtGui.QLabel(self.plot)
        self.alpha_label.setObjectName(_fromUtf8("alpha_label"))
        self.alpha_label.setText('Alpha: ')
        self.plot_appearance_options.addWidget(self.alpha_label)

        self.alpha_spin = QtGui.QDoubleSpinBox(self.plot)
        self.alpha_spin.setObjectName(_fromUtf8("alpha_spin"))
        self.alpha_spin.setRange(0, 1)
        self.alpha_spin.setValue(0.5)
        self.alpha_spin.setSingleStep(0.1)
        self.plot_appearance_options.addWidget(self.alpha_spin)

        
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.plot_appearance_options.addItem(spacerItem)
        self.plot_vlayout.addLayout(self.plot_appearance_options)
        
        self.file_hlayout = QtGui.QHBoxLayout()

        self.file_label = QtGui.QLabel(self.plot)
        self.file_label.setObjectName(_fromUtf8("file_label"))
        self.file_label.setText('Plot filename: ')
        self.file_hlayout.addWidget(self.file_label)
        self.file_text = QtGui.QLineEdit(self.plot)
        self.file_text.setObjectName(_fromUtf8("file_text"))
        self.file_hlayout.addWidget(self.file_text)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.file_hlayout.addItem(spacerItem)
                
        self.plot_vlayout.addLayout(self.file_hlayout)
        
        self.verticalLayout_8.addWidget(self.plot)
        self.plot.raise_()
        self.plot.setTitle(_translate("plot", "Plot", None))

        self.plot_choosedata.activated[int].connect(lambda: self.plot_change_vars(self.xvar_choices))

        self.plot_choosedata.activated[int].connect(
            lambda: self.get_minmax(self.xmin_spin, self.xmax_spin, self.xvar_choices.currentText()))
        self.plot_choosedata.activated[int].connect(
            lambda: self.get_minmax(self.ymin_spin, self.ymax_spin, self.yvar_choices.currentText()))

        self.xvar_choices.activated[int].connect(
            lambda: self.get_minmax(self.xmin_spin, self.xmax_spin, self.xvar_choices.currentText()))
        self.plot_choosedata.activated[int].connect(lambda: self.plot_change_vars(self.yvar_choices))
        self.yvar_choices.activated[int].connect(
            lambda: self.get_minmax(self.ymin_spin, self.ymax_spin, self.yvar_choices.currentText()))
        self.color_choices.activated.connect(lambda: self.get_plot_parameters())
        
        for name, obj in inspect.getmembers(self):
            if isinstance(obj, QtGui.QComboBox):
                obj.currentIndexChanged.connect(lambda: self.get_plot_parameters())
            if isinstance(obj, QtGui.QLineEdit):
                obj.textChanged.connect(lambda: self.get_plot_parameters())
            if isinstance(obj, QtGui.QDoubleSpinBox):
                obj.valueChanged.connect(lambda: self.get_plot_parameters())
            if isinstance(obj, QtGui.QCheckBox):
                obj.toggled.connect(lambda: self.get_plot_parameters())
                #
                #        self.plot_choosedata.currentIndexChanged.connect(lambda: self.get_plot_parameters())
                #        self.xvar_choices.currentIndexChanged.connect(lambda: self.get_plot_parameters())
                #        self.yvar_choices.currentIndexChanged.connect(lambda: self.get_plot_parameters())
                #        self.xmin_spin.valueChanged.connect(lambda: self.get_plot_parameters())
                #        self.ymin_spin.valueChanged.connect(lambda: self.get_plot_parameters())
                #        self.xmax_spin.valueChanged.connect(lambda: self.get_plot_parameters())
                #        self.ymax_spin.valueChanged.connect(lambda: self.get_plot_parameters())
                #        self.xtitle_text.textChanged.connect(lambda: self.get_plot_parameters())
                #        self.ytitle_text.textChanged.connect(lambda: self.get_plot_parameters())
                #        self.legend_label_text.textChanged.connect(lambda: self.get_plot_parameters())
                #        self.figname_text.textChanged.connect(lambda: self.get_plot_parameters())
                #        self.plot_title_text.textChanged.connect(lambda: self.get_plot_parameters())
                #        self.onetoone.toggled.connect(lambda: self.get_plot_parameters())
                #        self.color_choices.currentIndexChanged.connect(lambda: self.get_plot_parameters())
                #        self.file_text.textChanged.connect(lambda: self.get_plot_parameters())

    def plot_change_vars(self, obj):
        obj.clear()
        try:
            self.vars_level0 = self.pysat_fun.data[self.plot_choosedata.currentText()].df.columns.get_level_values(0)
            self.vars_level1 = self.pysat_fun.data[self.plot_choosedata.currentText()].df.columns.get_level_values(1)
            self.vars_level1 = list(self.vars_level1[self.vars_level0 != 'wvl'])
            self.vars_level0 = list(self.vars_level0[self.vars_level0 != 'wvl'])

            choices = self.vars_level1

            for i in choices:
                obj.addItem(i)
        except:
            try:
                choices=self.pysat_fun.data[self.plot_choosedata.currentText()].columns.values
                for i in choices:
                    obj.addItem(i)
            except:
                choices=['No valid choices']

    def get_minmax(self, objmin, objmax, var):
        try:
            varind = self.vars_level1.index(var)
            vartuple = (self.vars_level0[varind], self.vars_level1[varind])
            vardata = self.pysat_fun.data[self.plot_choosedata.currentText()].df[vartuple]

        except:
            try:
                vardata=self.pysat_fun.data[self.plot_choosedata.currentText()][var]
            except:
                vardata=[0,0]
        varmin = np.min(vardata)
        varmax = np.max(vardata)
        objmin.setValue(varmin)
        objmax.setValue(varmax)


def make_combobox(choices):
    combo = QtGui.QComboBox()

    for i, choice in enumerate(choices):
        combo.addItem(_fromUtf8(""))
        combo.setItemText(i, str(choice))

    return combo


def make_listwidget(choices):
    listwidget = QtGui.QListWidget()
    listwidget.setItemDelegate
    for item in choices:
        item = QtGui.QListWidgetItem(item)
        listwidget.addItem(item)
    return listwidget
