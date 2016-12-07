import sys
from PyQt4 import QtGui, QtCore
from pysat_ui import *
count = 1

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI(self)

    def initUI(self, MainWindow):
        pysat_ui.mainframe(self, MainWindow)
        button = QtGui.QPushButton('close',)



def main():
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()