from PyQt4 import QtCore, QtGui
from pysat.utils.gui_utils import make_combobox
from PYSAT_UI_MODULES.Error_ import error_print
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


class removenull_:
    def __init__(self, pysat_fun, verticalLayout_8):
        self.pysat_fun = pysat_fun
        self.verticalLayout_8 = verticalLayout_8
        self.main()

    def main(self):
        self.pysat_fun.set_fun_list(self.pysat_fun.removenull)  # add this function to the pysat list to be run
        self.pysat_fun.set_arg_list([])
        self.pysat_fun.set_kw_list({})
        self.removenull_ui()  # initiate the UI

    def get_removenull_parameters(self):

        datakey = self.removenull_choosedata.currentText()
        colname=self.colname_choices.currentText()
        colname = (self.vars_level0[self.vars_level1.index(colname)], colname)

        args = [datakey,colname]
        kws = {}
        self.pysat_fun.set_arg_list(args, replacelast=True)
        self.pysat_fun.set_kw_list(kws, replacelast=True)

    def removenull_ui(self):
        self.removenull = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.removenull.setFont(font)
        self.removenull.setObjectName(_fromUtf8("removenull"))
        self.verticalLayout = QtGui.QVBoxLayout(self.removenull)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.removenull_vlayout = QtGui.QVBoxLayout()
        self.removenull_vlayout.setMargin(11)
        self.removenull_vlayout.setSpacing(6)
        self.removenull_vlayout.setObjectName(_fromUtf8("removenull_vlayout"))
        self.removenull_choosedata_hlayout = QtGui.QHBoxLayout()
        self.removenull_choosedata_hlayout.setMargin(11)
        self.removenull_choosedata_hlayout.setSpacing(6)
        self.removenull_choosedata_hlayout.setObjectName(_fromUtf8("removenull_choosedata_hlayout"))
        self.removenull_choosedata_label = QtGui.QLabel(self.removenull)
        self.removenull_choosedata_label.setObjectName(_fromUtf8("removenull_choosedata_label"))
        self.removenull_choosedata_hlayout.addWidget(self.removenull_choosedata_label)

        datachoices = self.pysat_fun.datakeys
        if datachoices == []:
            error_print('No data has been loaded!')
            datachoices = ['No data has been loaded!']
        self.removenull_choosedata = make_combobox(datachoices)
        self.removenull_choosedata_hlayout.addWidget(self.removenull_choosedata)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.removenull_choosedata_hlayout.addItem(spacerItem)


        self.removenull_vlayout.addLayout(self.removenull_choosedata_hlayout)
        self.removenull_widget = QtGui.QWidget(self.removenull)
        self.removenull_widget.setMinimumSize(QtCore.QSize(0, 0))
        self.removenull_widget.setObjectName(_fromUtf8("removenull_widget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.removenull_widget)
        self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.start_of_sentence = QtGui.QLabel(self.removenull_widget)
        self.start_of_sentence.setObjectName(_fromUtf8("start_of_sentence"))
        self.horizontalLayout_2.addWidget(self.start_of_sentence)

        try:
            self.vars_level0 = self.pysat_fun.data[
                self.removenull_choosedata.currentText()].df.columns.get_level_values(0)
            self.vars_level1 = self.pysat_fun.data[
                self.removenull_choosedata.currentText()].df.columns.get_level_values(1)
            self.vars_level1 = list(self.vars_level1[self.vars_level0 != 'wvl'])
            self.vars_level0 = list(self.vars_level0[self.vars_level0 != 'wvl'])

            colnamechoices = self.vars_level1

        except:
            colnamechoices = self.pysat_fun.data[self.removenull_choosedata.currentText()].columns.values
        colnamechoices = [i for i in colnamechoices if not 'Unnamed' in i]  # remove unnamed columns from choices

        self.colname_choices = make_combobox(colnamechoices)
        self.horizontalLayout_2.addWidget(self.colname_choices)
        self.end_of_sentence = QtGui.QLabel(self.removenull_widget)
        self.end_of_sentence.setObjectName(_fromUtf8("end_of_sentence"))
        self.horizontalLayout_2.addWidget(self.end_of_sentence)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.removenull_vlayout.addWidget(self.removenull_widget)
        self.verticalLayout.addLayout(self.removenull_vlayout)

        self.verticalLayout_8.addWidget(self.removenull)

        self.removenull.setTitle(_translate("MainWindow", "Remove Null", None))
        self.removenull_choosedata_label.setText(_translate("MainWindow", "Choose data: ", None))
        self.start_of_sentence.setText(_translate("MainWindow", "Remove rows where ", None))

        self.end_of_sentence.setText(_translate("MainWindow", "is null.", None))
        self.get_removenull_parameters()
        self.colname_choices.currentIndexChanged.connect(lambda: self.get_removenull_parameters())
        self.removenull_choosedata.currentIndexChanged.connect(lambda: self.get_removenull_parameters())
