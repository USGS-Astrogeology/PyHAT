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


class ransac_:
    def __init__(self, pysat_fun, verticalLayout_8):
        self.pysat_fun = pysat_fun
        self.verticalLayout_8 = verticalLayout_8
        self.main()

    def main(self):
        # TODO add function param call here
        self.ransac_ui()
        # TODO add try and except here

    def ransac_ui(self):
        self.ransac = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ransac.setFont(font)
        self.ransac.setObjectName(_fromUtf8("ransac"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.ransac)
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.ransac_vlayout_2 = QtGui.QVBoxLayout()
        self.ransac_vlayout_2.setMargin(11)
        self.ransac_vlayout_2.setSpacing(6)
        self.ransac_vlayout_2.setObjectName(_fromUtf8("ransac_vlayout_2"))
        self.ransac_loss_func_hlayout_2 = QtGui.QHBoxLayout()
        self.ransac_loss_func_hlayout_2.setMargin(11)
        self.ransac_loss_func_hlayout_2.setSpacing(6)
        self.ransac_loss_func_hlayout_2.setObjectName(_fromUtf8("ransac_loss_func_hlayout_2"))
        self.ransac_loss_func_2 = QtGui.QComboBox(self.ransac)
        self.ransac_loss_func_2.setObjectName(_fromUtf8("ransac_loss_func_2"))
        self.ransac_loss_func_hlayout_2.addWidget(self.ransac_loss_func_2)
        self.ransac_threshold_label_2 = QtGui.QLabel(self.ransac)
        self.ransac_threshold_label_2.setObjectName(_fromUtf8("ransac_threshold_label_2"))
        self.ransac_loss_func_hlayout_2.addWidget(self.ransac_threshold_label_2)
        self.ransac_threshold_2 = QtGui.QDoubleSpinBox(self.ransac)
        self.ransac_threshold_2.setObjectName(_fromUtf8("ransac_threshold_2"))
        self.ransac_loss_func_hlayout_2.addWidget(self.ransac_threshold_2)
        self.ransac_min_label_2 = QtGui.QLabel(self.ransac)
        self.ransac_min_label_2.setObjectName(_fromUtf8("ransac_min_label_2"))
        self.ransac_loss_func_hlayout_2.addWidget(self.ransac_min_label_2)
        self.ransac_min_2 = QtGui.QDoubleSpinBox(self.ransac)
        self.ransac_min_2.setObjectName(_fromUtf8("ransac_min_2"))
        self.ransac_loss_func_hlayout_2.addWidget(self.ransac_min_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.ransac_loss_func_hlayout_2.addItem(spacerItem)
        self.ransac_vlayout_2.addLayout(self.ransac_loss_func_hlayout_2)
        self.horizontalLayout.addLayout(self.ransac_vlayout_2)
        self.verticalLayout_8.addWidget(self.ransac)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

        self.ransac.setTitle(_translate("MainWindow", "Ransac", None))
        self.ransac_loss_func_2.setItemText(0, _translate("MainWindow", "Loss Function", None))
        self.ransac_loss_func_2.setItemText(1, _translate("MainWindow", "Absolute Error", None))
        self.ransac_loss_func_2.setItemText(2, _translate("MainWindow", "Squared Error", None))
        self.ransac_threshold_label_2.setText(_translate("MainWindow", "Threshold", None))
        self.ransac_min_label_2.setText(_translate("MainWindow", "Minimum samples ", None))

