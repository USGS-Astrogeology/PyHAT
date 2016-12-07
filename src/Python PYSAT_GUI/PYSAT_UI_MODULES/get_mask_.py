from PyQt4 import QtCore, QtGui
from pysat.utils.gui_utils import make_combobox

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


class get_mask_:
    def __init__(self, pysat_fun, verticalLayout_8):
        self.pysat_fun = pysat_fun
        self.verticalLayout_8 = verticalLayout_8
        self.main()

    def main(self):
        self.pysat_fun.set_fun_list(self.pysat_fun.do_mask)
        self.pysat_fun.set_arg_list([])
        self.pysat_fun.set_kw_list({})
        self.get_mask_ui()


    def get_mask_params(self):
        datakey=self.mask_choosedata.currentText()
        maskfile=self.get_mask_line_edit.text()
        args=[datakey,maskfile]
        kws={}
        self.pysat_fun.set_arg_list(args, replacelast=True)
        self.pysat_fun.set_kw_list(kws, replacelast=True)

    def get_mask_ui(self):
        self.get_mask = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.get_mask.setFont(font)
        self.get_mask.setObjectName(_fromUtf8("get_mask"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.get_mask)
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        self.choosedata_label = QtGui.QLabel(self.get_mask)
        self.choosedata_label.setObjectName(_fromUtf8("choosedata_label"))
        self.horizontalLayout.addWidget(self.choosedata_label)
        datachoices = self.pysat_fun.datakeys
        if datachoices == []:
            error_print('No data has been loaded!')
            datachoices = ['No data has been loaded!']
        self.mask_choosedata = make_combobox(datachoices)
        self.horizontalLayout.addWidget(self.mask_choosedata)

        self.get_mask_label = QtGui.QLabel(self.get_mask)
        self.get_mask_label.setObjectName(_fromUtf8("get_mask_label"))
        self.horizontalLayout.addWidget(self.get_mask_label)
        self.get_mask_line_edit = QtGui.QLineEdit(self.get_mask)
        self.get_mask_line_edit.setReadOnly(True)
        self.get_mask_line_edit.setObjectName(_fromUtf8("get_mask_line_edit"))
        self.horizontalLayout.addWidget(self.get_mask_line_edit)
        self.get_mask_button = QtGui.QToolButton(self.get_mask)
        self.get_mask_button.setObjectName(_fromUtf8("get_mask_button"))
        self.horizontalLayout.addWidget(self.get_mask_button)
        self.verticalLayout_8.addWidget(self.get_mask)

        self.get_mask.setTitle(_translate("MainWindow", "Mask Data", None))
        self.choosedata_label.setText(_translate("MainWindow", "Choose data: ", None))
        self.get_mask_label.setText(_translate("MainWindow", "Mask file: ", None))
        self.get_mask_line_edit.setText(_translate("MainWindow", "*.csv", None))
        self.get_mask_button.setText(_translate("MainWindow", "...", None))
        self.get_mask_line_edit.textChanged.connect(lambda: self.get_mask_params())
        self.mask_choosedata.currentIndexChanged.connect(lambda: self.get_mask_params())
        self.get_mask_button.clicked.connect(lambda: self.on_getDataButton_clicked(self.get_mask_line_edit)
        )

    def on_getDataButton_clicked(self, lineEdit):
        filename = QtGui.QFileDialog.getOpenFileName(None, "Open Mask Data File", '.', "(*.csv)")
        lineEdit.setText(filename)
        if lineEdit.text() == "":
            lineEdit.setText("*.csv")

