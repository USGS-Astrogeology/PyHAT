import sys
from PyQt4.QtCore import  *
from PyQt4.QtGui import *

class SpinboxWidget(QWidget): ## this needs to be for mainwindow not widgets
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.addSpinboxes(10)

    def addSpinboxes(self, n):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        spb = []
        for i in range(n):
            spinbox = QSpinBox() #
            spinbox.setMaximum(1000) #
            spb.append(spinbox)#
            self.layout.addWidget(spinbox)

        for i in range(n-1):
            spb[i].valueChanged.connect(spb[i + 1].setMinimum)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('plastique')
    widget = SpinboxWidget()
    widget.setWindowTitle('Spinbox Tester')
    widget.show()

sys.exit(app.exec_())