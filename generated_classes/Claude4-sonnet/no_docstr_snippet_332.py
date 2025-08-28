class Ui_DialogModulation(object):
    def setupUi(self, DialogModulation):
        DialogModulation.setObjectName("DialogModulation")
        DialogModulation.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogModulation)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.groupBoxModulation = QtWidgets.QGroupBox(DialogModulation)
        self.groupBoxModulation.setObjectName("groupBoxModulation")
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxModulation)
        self.formLayout.setObjectName("formLayout")
        
        self.labelModulationType = QtWidgets.QLabel(self.groupBoxModulation)
        self.labelModulationType.setObjectName("labelModulationType")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelModulationType)
        
        self.comboBoxModulationType = QtWidgets.QComboBox(self.groupBoxModulation)
        self.comboBoxModulationType.setObjectName("comboBoxModulationType")
        self.comboBoxModulationType.addItem("")
        self.comboBoxModulationType.addItem("")
        self.comboBoxModulationType.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBoxModulationType)
        
        self.labelFrequency = QtWidgets.QLabel(self.groupBoxModulation)
        self.labelFrequency.setObjectName("labelFrequency")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelFrequency)
        
        self.spinBoxFrequency = QtWidgets.QSpinBox(self.groupBoxModulation)
        self.spinBoxFrequency.setMinimum(1)
        self.spinBoxFrequency.setMaximum(10000)
        self.spinBoxFrequency.setValue(100)
        self.spinBoxFrequency.setObjectName("spinBoxFrequency")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBoxFrequency)
        
        self.labelAmplitude = QtWidgets.QLabel(self.groupBoxModulation)
        self.labelAmplitude.setObjectName("labelAmplitude")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelAmplitude)
        
        self.doubleSpinBoxAmplitude = QtWidgets.QDoubleSpinBox(self.groupBoxModulation)
        self.doubleSpinBoxAmplitude.setMinimum(0.1)
        self.doubleSpinBoxAmplitude.setMaximum(10.0)
        self.doubleSpinBoxAmplitude.setValue(1.0)
        self.doubleSpinBoxAmplitude.setObjectName("doubleSpinBoxAmplitude")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxAmplitude)
        
        self.verticalLayout.addWidget(self.groupBoxModulation)
        
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogModulation)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        
        self.retranslateUi(DialogModulation)
        self.buttonBox.accepted.connect(DialogModulation.accept)
        self.buttonBox.rejected.connect(DialogModulation.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogModulation)

    def retranslateUi(self, DialogModulation):
        _translate = QtCore.QCoreApplication.translate
        DialogModulation.setWindowTitle(_translate("DialogModulation", "Modulation Settings"))
        self.groupBoxModulation.setTitle(_translate("DialogModulation", "Modulation Parameters"))
        self.labelModulationType.setText(_translate("DialogModulation", "Type:"))
        self.comboBoxModulationType.setItemText(0, _translate("DialogModulation", "AM"))
        self.comboBoxModulationType.setItemText(1, _translate("DialogModulation", "FM"))
        self.comboBoxModulationType.setItemText(2, _translate("DialogModulation", "PM"))
        self.labelFrequency.setText(_translate("DialogModulation", "Frequency (Hz):"))
        self.labelAmplitude.setText(_translate("DialogModulation", "Amplitude:"))