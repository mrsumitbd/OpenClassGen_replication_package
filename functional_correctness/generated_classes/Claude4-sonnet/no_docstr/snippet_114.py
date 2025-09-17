class Ui_DialogModulationParameters(object):
    def setupUi(self, DialogModulationParameters):
        DialogModulationParameters.setObjectName("DialogModulationParameters")
        DialogModulationParameters.resize(400, 300)
        DialogModulationParameters.setWindowTitle("Modulation Parameters")
        
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogModulationParameters)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.groupBoxModulation = QtWidgets.QGroupBox(DialogModulationParameters)
        self.groupBoxModulation.setObjectName("groupBoxModulation")
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxModulation)
        self.formLayout.setObjectName("formLayout")
        
        self.labelFrequency = QtWidgets.QLabel(self.groupBoxModulation)
        self.labelFrequency.setObjectName("labelFrequency")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelFrequency)
        
        self.spinBoxFrequency = QtWidgets.QDoubleSpinBox(self.groupBoxModulation)
        self.spinBoxFrequency.setObjectName("spinBoxFrequency")
        self.spinBoxFrequency.setMaximum(999999.99)
        self.spinBoxFrequency.setValue(1000.0)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBoxFrequency)
        
        self.labelAmplitude = QtWidgets.QLabel(self.groupBoxModulation)
        self.labelAmplitude.setObjectName("labelAmplitude")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelAmplitude)
        
        self.spinBoxAmplitude = QtWidgets.QDoubleSpinBox(self.groupBoxModulation)
        self.spinBoxAmplitude.setObjectName("spinBoxAmplitude")
        self.spinBoxAmplitude.setMaximum(100.0)
        self.spinBoxAmplitude.setValue(50.0)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBoxAmplitude)
        
        self.labelPhase = QtWidgets.QLabel(self.groupBoxModulation)
        self.labelPhase.setObjectName("labelPhase")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelPhase)
        
        self.spinBoxPhase = QtWidgets.QDoubleSpinBox(self.groupBoxModulation)
        self.spinBoxPhase.setObjectName("spinBoxPhase")
        self.spinBoxPhase.setMaximum(360.0)
        self.spinBoxPhase.setValue(0.0)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinBoxPhase)
        
        self.verticalLayout.addWidget(self.groupBoxModulation)
        
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogModulationParameters)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        
        self.retranslateUi(DialogModulationParameters)
        self.buttonBox.accepted.connect(DialogModulationParameters.accept)
        self.buttonBox.rejected.connect(DialogModulationParameters.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogModulationParameters)

    def retranslateUi(self, DialogModulationParameters):
        _translate = QtCore.QCoreApplication.translate
        DialogModulationParameters.setWindowTitle(_translate("DialogModulationParameters", "Modulation Parameters"))
        self.groupBoxModulation.setTitle(_translate("DialogModulationParameters", "Modulation Settings"))
        self.labelFrequency.setText(_translate("DialogModulationParameters", "Frequency (Hz):"))
        self.labelAmplitude.setText(_translate("DialogModulationParameters", "Amplitude (%):"))
        self.labelPhase.setText(_translate("DialogModulationParameters", "Phase (°):"))