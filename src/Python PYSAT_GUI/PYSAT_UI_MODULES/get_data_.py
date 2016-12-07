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


class get_data_u_:
    def __init__(self, pysat_fun, verticalLayout_8):
        self.pysat_fun = pysat_fun
        self.verticalLayout_8 = verticalLayout_8
        self.main()

    def main(self):
        self.pysat_fun.set_fun_list(self.pysat_fun.get_data)  # add this function to the pysat list to be run
        self.get_data_ui()  # initiate the UI
        try:
            self.get_data_u_button.clicked.connect(
                lambda: self.on_getDataButton_clicked(self.get_data_u_line_edit,
                                                      "unknown"))  # when a button is clicked call the on_getDataButton_clicked function
        except:
            pass

    def get_data_ui(self):
        self.get_data_u = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.get_data_u.setFont(font)
        self.get_data_u.setObjectName(_fromUtf8("get_data_u"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.get_data_u)
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.get_data_u_label = QtGui.QLabel(self.get_data_u)
        self.get_data_u_label.setObjectName(_fromUtf8("get_data_u_label"))
        self.horizontalLayout.addWidget(self.get_data_u_label)
        self.get_data_u_line_edit = QtGui.QLineEdit(self.get_data_u)
        self.get_data_u_line_edit.setReadOnly(True)
        self.get_data_u_line_edit.setObjectName(_fromUtf8("get_data_u_line_edit"))
        self.horizontalLayout.addWidget(self.get_data_u_line_edit)
        self.get_data_u_button = QtGui.QToolButton(self.get_data_u)
        self.get_data_u_button.setObjectName(_fromUtf8("get_data_u_button"))
        self.horizontalLayout.addWidget(self.get_data_u_button)
        self.verticalLayout_8.addWidget(self.get_data_u)

        self.get_data_u.setTitle(_translate("MainWindow", "Load Unknown Data", None))
        self.get_data_u_label.setText(_translate("MainWindow", "File Name", None))
        self.get_data_u_line_edit.setText(_translate("MainWindow", "*.csv", None))
        self.get_data_u_button.setText(_translate("MainWindow", "...", None))

    def on_getDataButton_clicked(self, lineEdit, key):
        filename = QtGui.QFileDialog.getOpenFileName(None, "Open " + key + " Data File", '.', "(*.csv)")
        lineEdit.setText(filename)
        if lineEdit.text() == "":
            lineEdit.setText("*.csv")
        
        self.pysat_fun.set_arg_list([filename, key])
        self.pysat_fun.set_kw_list({})
        return True


class get_data_k_:
    def __init__(self, pysat_fun, verticalLayout_8):
        self.pysat_fun = pysat_fun
        self.verticalLayout_8 = verticalLayout_8
        self.main()

    def main(self):
        self.pysat_fun.set_fun_list(self.pysat_fun.get_data)  # add this function to the pysat list to be run
        self.get_data_ui()  # initiate the UI
        try:
            self.get_data_k_button.clicked.connect(
                lambda: self.on_getDataButton_clicked(self.get_data_k_line_edit,
                                                      "known"))  # when a button is clicked call the on_getDataButton_clicked function
        except:
            pass

    def get_data_ui(self):
        self.get_data_k = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.get_data_k.setFont(font)
        self.get_data_k.setObjectName(_fromUtf8("get_data_k"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.get_data_k)
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.get_data_k_label = QtGui.QLabel(self.get_data_k)
        self.get_data_k_label.setObjectName(_fromUtf8("get_data_k_label"))
        self.horizontalLayout.addWidget(self.get_data_k_label)
        self.get_data_k_line_edit = QtGui.QLineEdit(self.get_data_k)
        self.get_data_k_line_edit.setReadOnly(True)
        self.get_data_k_line_edit.setObjectName(_fromUtf8("get_data_k_line_edit"))
        self.horizontalLayout.addWidget(self.get_data_k_line_edit)
        self.get_data_k_button = QtGui.QToolButton(self.get_data_k)
        self.get_data_k_button.setObjectName(_fromUtf8("get_data_k_button"))
        self.horizontalLayout.addWidget(self.get_data_k_button)
        self.verticalLayout_8.addWidget(self.get_data_k)

        self.get_data_k.setTitle(_translate("MainWindow", "Load Known Data", None))
        self.get_data_k_label.setText(_translate("MainWindow", "File Name", None))
        self.get_data_k_line_edit.setText(_translate("MainWindow", "*.csv", None))
        self.get_data_k_button.setText(_translate("MainWindow", "...", None))

    def on_getDataButton_clicked(self, lineEdit, key):
        filename = QtGui.QFileDialog.getOpenFileName(None, "Open " + key + " Data File", '.', "(*.csv)")
        lineEdit.setText(filename)
        if lineEdit.text() == "":
            lineEdit.setText("*.csv")
        
        self.pysat_fun.set_arg_list([filename, key])
        self.pysat_fun.set_kw_list({})
        return True
