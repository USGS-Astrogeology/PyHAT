def main(self):
    # Load in function
    self.pysat_fun.set_arg_list(self.pysat_fun.do_norm)
    # main needs to call the UI
    self.normalization_ui()
    # TODO Add your connections here


def normalization_ui(self):
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
    self.regression_choosedata_label = QtGui.QLabel(self.normalization)
    self.regression_choosedata_label.setObjectName(_fromUtf8("regression_choosedata_label"))
    self.choosedata_layout.addWidget(self.regression_choosedata_label)
    self.regression_choosedata = QtGui.QComboBox(self.normalization)
    self.regression_choosedata.setIconSize(QtCore.QSize(50, 20))
    self.regression_choosedata.setObjectName(_fromUtf8("regression_choosedata"))
    self.choosedata_layout.addWidget(self.regression_choosedata)
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
    self.del_ranges_button = QtGui.QPushButton(self.normalization)
    self.del_ranges_button.setObjectName(_fromUtf8("add_ranges_button_2"))
    self.min_max_horizontalLayout.addWidget(self.del_ranges_button)
    self.verticalLayout.addLayout(self.min_max_horizontalLayout)
    self.verticalLayout_8.addWidget(self.normalization)

    self.normalization.setTitle(_translate("MainWindow", "Normalization", None))
    self.regression_choosedata_label.setText(_translate("MainWindow", "Choose data: ", None))
    self.regression_choosedata.setItemText(0, _translate("MainWindow", "Choose Data", None))
    self.regression_choosedata.setItemText(1, _translate("MainWindow", "Known Data", None))
    self.add_ranges_button.setText(_translate("MainWindow", "Add Ranges", None))
    self.del_ranges_button.setText(_translate("MainWindow", "delete Ranges", None))
    # TODO: give functionality to the buttons on the UI
    # self.add_ranges_button.clicked.connect(lambda: self.add_range_clicked(self.num))
    # self.del_ranges_button.clicked.connect(lambda: self.del_range_clicked(self.num))


class min_max:
    def __init__(self, pysat_fun, normalization, verticalLayout, num):
        self.pysat_fun = pysat_fun
        self.normalization = normalization
        self.all_ranges_layout = verticalLayout

    def min_max(self):
        self.ranges_layout = QtGui.QHBoxLayout()
        self.ranges_layout.setMargin(11)
        self.ranges_layout.setSpacing(6)
        self.ranges_layout.setObjectName(_fromUtf8("ranges_layout"))
        self.min_label = QtGui.QLabel(self.normalization)
        self.min_label.setObjectName(_fromUtf8("min_label"))
        self.ranges_layout.addWidget(self.min_label)
        self.min_lineEdit = QtGui.QLineEdit(self.normalization)
        self.min_lineEdit.setObjectName(_fromUtf8("min_lineEdit"))
        self.ranges_layout.addWidget(self.min_lineEdit)
        self.max_label = QtGui.QLabel(self.normalization)
        self.max_label.setObjectName(_fromUtf8("max_label"))
        self.ranges_layout.addWidget(self.max_label)
        self.max_lineEdit = QtGui.QLineEdit(self.normalization)
        self.max_lineEdit.setObjectName(_fromUtf8("max_lineEdit"))
        self.ranges_layout.addWidget(self.max_lineEdit)
        self.all_ranges_layout.addLayout(self.ranges_layout)
        self.min_label.setText(_translate("MainWindow", "Min", None))
        self.max_label.setText(_translate("MainWindow", "Max", None))

        # TODO each of these min_max's have connections that tell us what was updated
        self.min_lineEdit.editingFinished.connect(lambda: self.set_list(self.min_lineEdit, self.max_lineEdit))
        self.max_lineEdit.editingFinished.connect(lambda: self.set_list(self.min_lineEdit, self.max_lineEdit))


class normalization_:
    def __init__(self, pysat_fun, verticalLayout_8):
        self.pysat_fun = pysat_fun
        self.verticalLayout_8 = verticalLayout_8
        self.data = [None] * 24
        self.norm_list = [None] * 48
        self.num = 0
        self.main()

    def main(self):
        # append function to pysat
        # self.pysat_fun.fun_list.append(self.pysat_fun.set_file_outpath)
        self.normalization_ui()
        try:
            pass
            # parameters here
        except Exception as e:
            error_print(e)

    def normalization_ui(self):
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
        self.regression_choosedata_label = QtGui.QLabel(self.normalization)
        self.regression_choosedata_label.setObjectName(_fromUtf8("regression_choosedata_label"))
        self.choosedata_layout.addWidget(self.regression_choosedata_label)
        self.regression_choosedata = QtGui.QComboBox(self.normalization)
        self.regression_choosedata.setIconSize(QtCore.QSize(50, 20))
        self.regression_choosedata.setObjectName(_fromUtf8("regression_choosedata"))
        self.choosedata_layout.addWidget(self.regression_choosedata)
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
        self.del_ranges_button = QtGui.QPushButton(self.normalization)
        self.del_ranges_button.setObjectName(_fromUtf8("add_ranges_button_2"))
        self.min_max_horizontalLayout.addWidget(self.del_ranges_button)
        self.verticalLayout.addLayout(self.min_max_horizontalLayout)
        self.verticalLayout_8.addWidget(self.normalization)

        self.normalization.setTitle(_translate("MainWindow", "Normalization", None))
        self.regression_choosedata_label.setText(_translate("MainWindow", "Choose data: ", None))
        self.regression_choosedata.setItemText(0, _translate("MainWindow", "Choose Data", None))
        self.regression_choosedata.setItemText(1, _translate("MainWindow", "Known Data", None))
        self.add_ranges_button.setText(_translate("MainWindow", "Add Ranges", None))
        self.del_ranges_button.setText(_translate("MainWindow", "delete Ranges", None))


    def add_range_clicked(self, num):
        self.data[num] = min_max(self.pysat_fun, self.normalization, self.all_ranges_layout)
        if self.data[num]:
            self.get_norm_values()

        self.num = self.num + 1

    def del_range_clicked(self, num):
        self.del_ranges_button.clicked.connect(lambda: self.del_range_clicked(self.num))
        if self.num > 0:
            # self.data[num].
            self.num = self.num - 1

    def get_norm_values(self):
        print(['known data', [(self.data[0].get_min(), self.data[0].get_max)
            , (self.data[1].get_min(), self.data[1].get_max)
            , (self.data[2].get_min(), self.data[2].get_max)
            , (self.data[3].get_min(), self.data[3].get_max)
            , (self.data[4].get_min(), self.data[4].get_max)
            , (self.data[5].get_min(), self.data[5].get_max)
            , (self.data[6].get_min(), self.data[6].get_max)
            , (self.data[7].get_min(), self.data[7].get_max)
            , (self.data[8].get_min(), self.data[8].get_max)
            , (self.data[9].get_min(), self.data[9].get_max)]])


class min_max:
    def __init__(self, pysat_fun, normalization, verticalLayout):
        self.pysat_fun = pysat_fun
        self.normalization = normalization
        self.all_ranges_layout = verticalLayout
        self.small_tuple = (None, None)
        self.min_max()

    def min_max(self):
        self.ranges_layout = QtGui.QHBoxLayout()
        self.ranges_layout.setMargin(11)
        self.ranges_layout.setSpacing(6)
        self.ranges_layout.setObjectName(_fromUtf8("ranges_layout"))
        self.min_label = QtGui.QLabel(self.normalization)
        self.min_label.setObjectName(_fromUtf8("min_label"))
        self.ranges_layout.addWidget(self.min_label)
        self.min_lineEdit = QtGui.QLineEdit(self.normalization)
        self.min_lineEdit.setObjectName(_fromUtf8("min_lineEdit"))
        self.ranges_layout.addWidget(self.min_lineEdit)
        self.max_label = QtGui.QLabel(self.normalization)
        self.max_label.setObjectName(_fromUtf8("max_label"))
        self.ranges_layout.addWidget(self.max_label)
        self.max_lineEdit = QtGui.QLineEdit(self.normalization)
        self.max_lineEdit.setObjectName(_fromUtf8("max_lineEdit"))
        self.ranges_layout.addWidget(self.max_lineEdit)
        self.all_ranges_layout.addLayout(self.ranges_layout)
        self.min_label.setText(_translate("MainWindow", "Min", None))
        self.max_label.setText(_translate("MainWindow", "Max", None))

        self.min_lineEdit.editingFinished.connect(lambda: self.set_list(self.min_lineEdit, self.max_lineEdit))
        self.max_lineEdit.editingFinished.connect(lambda: self.set_list(self.min_lineEdit, self.max_lineEdit))

    def set_list(self, min, max):
        if min.text() == '' and max.text() == '':
            error_print("Please fill in all boxes")
        else:
            try:
                min = int(min.text())
                max = int(max.text())
                self.small_tuple = (min, max)
                print(self.small_tuple)
                return True
            except:
                pass

    def get_min(self):
        return self.min_lineEdit

    def get_max(self):
        return self.max_lineEdit

    def add_to_pysat(self):
        self.pysat_fun.set_arg_list()


# ============================================================================================================




        self.data = [None] * 42  # data holds the box objects
        self.list = [(None, None)] * 42  # normalization needs a list. It will look like this [(0,0), (0,0), (0,0)]
        self.pysat_fun = pysat_fun  # pysat holds all the functions used to run everything
        self.num = 0  # num holds necessary position
        self.verticalLayout_8 = verticalLayout  # normalization needs the necessary layouts to work.
        self.main()  # normalization_ needs a driver function main

    def add_range_clicked(self, num):
        self.data[num] = min_max(self.pysat_fun, self.normalization, self.all_ranges_layout, num)
        self.num = self.num + 1

    def del_range_clicked(self, num):
        if self.num > 0:
            # self.data[num].
            self.num = self.num - 1

    def add_norm_value(self):
        pass


class min_max:
    def __init__(self, pysat_fun, normalization, verticalLayout, num):
        self.pysat_fun = pysat_fun
        self.normalization = normalization
        self.all_ranges_layout = verticalLayout
        self.min_max()
        self.num = num

    def min_max(self):
        self.ranges_layout = QtGui.QHBoxLayout()
        self.ranges_layout.setMargin(11)
        self.ranges_layout.setSpacing(6)
        self.ranges_layout.setObjectName(_fromUtf8("ranges_layout"))
        self.min_label = QtGui.QLabel(self.normalization)
        self.min_label.setObjectName(_fromUtf8("min_label"))
        self.ranges_layout.addWidget(self.min_label)
        self.min_lineEdit = QtGui.QLineEdit(self.normalization)
        self.min_lineEdit.setObjectName(_fromUtf8("min_lineEdit"))
        self.ranges_layout.addWidget(self.min_lineEdit)
        self.max_label = QtGui.QLabel(self.normalization)
        self.max_label.setObjectName(_fromUtf8("max_label"))
        self.ranges_layout.addWidget(self.max_label)
        self.max_lineEdit = QtGui.QLineEdit(self.normalization)
        self.max_lineEdit.setObjectName(_fromUtf8("max_lineEdit"))
        self.ranges_layout.addWidget(self.max_lineEdit)
        self.all_ranges_layout.addLayout(self.ranges_layout)
        self.min_label.setText(_translate("MainWindow", "Min", None))
        self.max_label.setText(_translate("MainWindow", "Max", None))

        # TODO each of these min_max's have connections that tell us what was updated
        self.min_lineEdit.editingFinished.connect(lambda: self.set_list(self.min_lineEdit, self.max_lineEdit))
        self.max_lineEdit.editingFinished.connect(lambda: self.set_list(self.min_lineEdit, self.max_lineEdit))

        # TODO each of these updates should return a value back to normalization so we can add it to a list

    # These return the results, but where does position come in?
    # Should we just return everything?
    def get_min(self):
        return self.min_lineEdit

    def get_max(self):
        return self.max_lineEdit

    def set_list(self, min, max):
        # TODO: Fix logic for displaying the error window
        # if min.text() == '' and max.text() == '':
        #     error_print("Please fill in all boxes")
        # else:
        try:
            min = int(min.text())
            max = int(max.text())
            self.small_tuple = (min, max)
            normalization_.list[self.num] = self.small_tuple
            print(normalization_.list[self.num])
        except:
            pass
