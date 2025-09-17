class Ui_DialogModulationParameters(object):
    def setupUi(self, DialogModulationParameters):
        DialogModulationParameters.setObjectName("DialogModulationParameters")
        DialogModulationParameters.resize(320, 150)
        self.gridLayout = QtWidgets.QGridLayout(DialogModulationParameters)
        self.gridLayout.setObjectName("gridLayout")

        self.labelType = QtWidgets.QLabel(DialogModulationParameters)
        self.labelType.setObjectName("labelType")
        self.gridLayout.addWidget(self.labelType, 0, 0, 1, 1)

        self.comboBoxType = QtWidgets.QComboBox(DialogModulationParameters)
        self.comboBoxType.setObjectName("comboBoxType")
        self.comboBoxType.addItem("")
        self.comboBoxType.addItem("")
        self.comboBoxType.addItem("")
        self.gridLayout.addWidget(self.comboBoxType, 0, 1, 1, 1)

        self.labelFrequency = QtWidgets.QLabel(DialogModulationParameters)
        self.labelFrequency.setObjectName("labelFrequency")
        self.gridLayout.addWidget(self.labelFrequency, 1, 0, 1, 1)

        self.doubleSpinBoxFrequency = QtWidgets.QDoubleSpinBox(DialogModulationParameters)
        self.doubleSpinBoxFrequency.setObjectName("doubleSpinBoxFrequency")
        self.doubleSpinBoxFrequency.setRange(0.0, 1000000.0)
        self.doubleSpinBoxFrequency.setSuffix(" Hz")
        self.gridLayout.addWidget(self.doubleSpinBoxFrequency, 1, 1, 1, 1)

        self.labelDepth = QtWidgets.QLabel(DialogModulationParameters)
        self.labelDepth.setObjectName("labelDepth")
        self.gridLayout.addWidget(self.labelDepth, 2, 0, 1, 1)

        self.doubleSpinBoxDepth = QtWidgets.QDoubleSpinBox(DialogModulationParameters)
        self.doubleSpinBoxDepth.setObjectName("doubleSpinBoxDepth")
        self.doubleSpinBoxDepth.setRange(0.0, 100.0)
        self.doubleSpinBoxDepth.setSuffix(" %")
        self.gridLayout.addWidget(self.doubleSpinBoxDepth, 2, 1, 1, 1)

        self.buttonBox = QtWidgets.QDialogButtonBox(DialogModulationParameters)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.retranslateUi(DialogModulationParameters)
        self.buttonBox.accepted.connect(DialogModulationParameters.accept)
        self.buttonBox.rejected.connect(DialogModulationParameters.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogModulationParameters)

    def retranslateUi(self, DialogModulationParameters):
        _translate = QtCore.QCoreApplication.translate
        DialogModulationParameters.setWindowTitle(_translate("DialogModulationParameters", "Modulation Parameters"))
        self.labelType.setText(_translate("DialogModulationParameters", "Type:"))
        self.comboBoxType.setItemText(0, _translate("DialogModulationParameters", "AM"))
        self.comboBoxType.setItemText(1, _translate("DialogModulationParameters", "FM"))
        self.comboBoxType.setItemText(2, _translate("DialogModulationParameters", "PM"))
        self.labelFrequency.setText(_translate("DialogModulationParameters", "Frequency:"))
        self.labelDepth.setText(_translate("DialogModulationParameters", "Depth:"))