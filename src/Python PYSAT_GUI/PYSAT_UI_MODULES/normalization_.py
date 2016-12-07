from PyQt4 import QtCore, QtGui

from PYSAT_UI_MODULES.Error_ import error_print

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


# Normalization creates a UI
# and many smaller pieces of the UI called min_max
#
# normalization
#     |_ min_max
#     |_ min_max
#     |_ min_max
#
# each of these min_max's have connections that tell us what was updated
# each of these updates should return a value back to normalization so we can add it to a list
#
#      |---------------------|           |----------------------|
#      |    Normalization    |           |       min_max        |
#      |---------------------|           |----------------------|
#      | returned val in lst | <-------- | return value and pos |
#      | load UI/Boxes       | --------> |                      |
#      |---------------------|           |----------------------|
#
# every time we change boxes, we should know which box is getting updated, and what the updated value is
# so for example
#
#     min [      ]  max [      ]
#     min [      ]  max [ 1000 ]*
#     min [      ]  max [      ]
# the above box* was update4d
# it's position is data[1], max_lineEdit, and it's value is 1000

class normalization_:
    def __init__(self, pysat_fun, verticalLayout_8):
        self.verticalLayout_8 = verticalLayout_8
        self.pysat_fun = pysat_fun
        self.min_lineEdits = []
        self.max_lineEdits = []
        self.num = 0
        self.main()

    def main(self):
        # driver function, calls UI and set's up connections
        # add function list calls here
        self.pysat_fun.set_fun_list(self.pysat_fun.do_norm)
        self.normalization_ui()
        self.add_ranges_button.clicked.connect(lambda: self.add_ranges())
        self.finish_button.clicked.connect(lambda: self.finished())

    def normalization_ui(self):
        datachoices = self.pysat_fun.datakeys
        if datachoices == []:
            error_print('No Data has been loaded')
            datachoices = ['No data has been loaded!']
        self.normalization = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.normalization.setFont(font)
        self.normalization.setObjectName(_fromUtf8("normalization"))
        self.verticalLayout = QtGui.QVBoxLayout(self.normalization)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.choosedata_layout = QtGui.QHBoxLayout()
        self.choosedata_layout.setMargin(11)
        self.choosedata_layout.setSpacing(6)
        self.choosedata_layout.setObjectName(_fromUtf8("choosedata_layout"))
        self.normalization_choosedata_label = QtGui.QLabel(self.normalization)
        self.normalization_choosedata_label.setObjectName(_fromUtf8("normalization_choosedata_label"))
        self.choosedata_layout.addWidget(self.normalization_choosedata_label)
        self.normalization_choosedata = make_combobox(datachoices)
        self.normalization_choosedata.setIconSize(QtCore.QSize(50, 20))
        self.normalization_choosedata.setObjectName(_fromUtf8("normalization_choosedata"))
        self.choosedata_layout.addWidget(self.normalization_choosedata)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.choosedata_layout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.choosedata_layout)
        self.all_ranges_layout = QtGui.QVBoxLayout()
        self.all_ranges_layout.setMargin(11)
        self.all_ranges_layout.setSpacing(6)
        self.all_ranges_layout.setObjectName(_fromUtf8("all_ranges_layout"))
        self.verticalLayout.addLayout(self.all_ranges_layout)
        self.min_max_horizontalLayout = QtGui.QHBoxLayout()
        self.min_max_horizontalLayout.setMargin(11)
        self.min_max_horizontalLayout.setSpacing(6)
        self.min_max_horizontalLayout.setObjectName(_fromUtf8("min_max_horizontalLayout"))
        self.add_ranges_button = QtGui.QPushButton(self.normalization)
        self.add_ranges_button.setObjectName(_fromUtf8("add_ranges_button"))
        self.min_max_horizontalLayout.addWidget(self.add_ranges_button)
        self.finish_button = QtGui.QPushButton(self.normalization)
        self.finish_button.setObjectName(_fromUtf8("add_ranges_button_2"))
        self.min_max_horizontalLayout.addWidget(self.finish_button)
        self.verticalLayout.addLayout(self.min_max_horizontalLayout)
        self.verticalLayout_8.addWidget(self.normalization)

        self.normalization.setTitle(_translate("MainWindow", "Normalization", None))
        self.normalization_choosedata_label.setText(_translate("MainWindow", "Choose data: ", None))
        self.normalization_choosedata.setItemText(1, _translate("MainWindow", "Known Data", None))
        self.add_ranges_button.setText(_translate("MainWindow", "Add Ranges", None))
        self.finish_button.setText(_translate("MainWindow", "Finished", None))

    def add_ranges(self):
        self.ranges_layout = QtGui.QHBoxLayout()
        self.min_label = QtGui.QLabel(self.normalization)
        self.max_label = QtGui.QLabel(self.normalization)
        self.min_lineEdit = QtGui.QLineEdit(self.normalization)
        self.max_lineEdit = QtGui.QLineEdit(self.normalization)
        self.all_ranges_layout.addLayout(self.ranges_layout)
        self.ranges_layout.addWidget(self.min_label)
        self.ranges_layout.addWidget(self.min_lineEdit)
        self.ranges_layout.addWidget(self.max_label)
        self.ranges_layout.addWidget(self.max_lineEdit)
        self.min_label.setText(_translate("MainWindow", "Min", None))
        self.max_label.setText(_translate("MainWindow", "Max", None))

        self.min_lineEdits.append(self.min_lineEdit)
        self.max_lineEdits.append(self.max_lineEdit)

    def finished(self):
        arg_list = []
        len_of_lineEdits = len(self.min_lineEdits) + len(self.max_lineEdits)
        for i in range(len_of_lineEdits):
            try:
                if not self.min_lineEdits[i].text() == '' and not self.max_lineEdits[i].text() == '':
                    small_tuple = (int(self.min_lineEdits[i].text()), int(self.max_lineEdits[i].text()))
                    arg_list.append(small_tuple)
                    # arg_list.append(['known data', [(0, 350), (350, 470), (470, 1000)]])
            except:
                pass
        datakey = self.normalization_choosedata.currentText()
        self.pysat_fun.set_arg_list([datakey, arg_list])
        self.pysat_fun.set_kw_list({})
        print(self.pysat_fun.arg_list)


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
