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


class pca_:
    def __init__(self, pysat_fun, verticalLayout_8):
        self.pysat_fun = pysat_fun
        self.verticalLayout_8 = verticalLayout_8
        self.main()


    def main(self):
        # TODO add function param call here
        # TODO add try and except here
        self.pca_ui()

    def pca_ui(self):
        self.pca = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pca.setFont(font)
        self.pca.setObjectName(_fromUtf8("pca"))
        self.verticalLayout = QtGui.QVBoxLayout(self.pca)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pca_vlayout = QtGui.QVBoxLayout()
        self.pca_vlayout.setMargin(11)
        self.pca_vlayout.setSpacing(6)
        self.pca_vlayout.setObjectName(_fromUtf8("pca_vlayout"))
        self.pca_choose_data = QtGui.QComboBox(self.pca)
        self.pca_choose_data.setObjectName(_fromUtf8("pca_choose_data"))
        self.pca_vlayout.addWidget(self.pca_choose_data)
        self.pca_hlayout = QtGui.QHBoxLayout()
        self.pca_hlayout.setMargin(11)
        self.pca_hlayout.setSpacing(6)
        self.pca_hlayout.setObjectName(_fromUtf8("pca_hlayout"))
        self.pca_nc_label = QtGui.QLabel(self.pca)
        self.pca_nc_label.setObjectName(_fromUtf8("pca_nc_label"))
        self.pca_hlayout.addWidget(self.pca_nc_label)
        self.pca_nc = QtGui.QSpinBox(self.pca)
        self.pca_nc.setObjectName(_fromUtf8("pca_nc"))
        self.pca_hlayout.addWidget(self.pca_nc)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.pca_hlayout.addItem(spacerItem)
        self.pca_button = QtGui.QPushButton(self.pca)
        self.pca_button.setObjectName(_fromUtf8("pca_button"))
        self.pca_hlayout.addWidget(self.pca_button)
        self.pca_vlayout.addLayout(self.pca_hlayout)
        self.verticalLayout.addLayout(self.pca_vlayout)
        self.verticalLayout_8.addWidget(self.pca)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.ok.addItem(spacerItem1)

        self.pca.setTitle(_translate("MainWindow", "PCA", None))
        self.pca_choose_data.setItemText(0, _translate("MainWindow", "Choose Data", None))
        self.pca_choose_data.setItemText(1, _translate("MainWindow", "Known Data", None))
        self.pca_button.setText(_translate("MainWindow", "Do PCA", None))