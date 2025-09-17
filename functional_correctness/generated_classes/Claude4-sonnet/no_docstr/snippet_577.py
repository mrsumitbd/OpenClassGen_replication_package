class Ui_GPSDialog(object):
    def setupUi(self, GPSDialog):
        GPSDialog.setObjectName("GPSDialog")
        GPSDialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(GPSDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.groupBox = QtWidgets.QGroupBox(GPSDialog)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        
        self.label_latitude = QtWidgets.QLabel(self.groupBox)
        self.label_latitude.setObjectName("label_latitude")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_latitude)
        
        self.lineEdit_latitude = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_latitude.setObjectName("lineEdit_latitude")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_latitude)
        
        self.label_longitude = QtWidgets.QLabel(self.groupBox)
        self.label_longitude.setObjectName("label_longitude")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_longitude)
        
        self.lineEdit_longitude = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_longitude.setObjectName("lineEdit_longitude")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_longitude)
        
        self.label_altitude = QtWidgets.QLabel(self.groupBox)
        self.label_altitude.setObjectName("label_altitude")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_altitude)
        
        self.lineEdit_altitude = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_altitude.setObjectName("lineEdit_altitude")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_altitude)
        
        self.verticalLayout.addWidget(self.groupBox)
        
        self.buttonBox = QtWidgets.QDialogButtonBox(GPSDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        
        self.retranslateUi(GPSDialog)
        self.buttonBox.accepted.connect(GPSDialog.accept)
        self.buttonBox.rejected.connect(GPSDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GPSDialog)

    def retranslateUi(self, GPSDialog):
        _translate = QtCore.QCoreApplication.translate
        GPSDialog.setWindowTitle(_translate("GPSDialog", "GPS Coordinates"))
        self.groupBox.setTitle(_translate("GPSDialog", "Location"))
        self.label_latitude.setText(_translate("GPSDialog", "Latitude:"))
        self.label_longitude.setText(_translate("GPSDialog", "Longitude:"))
        self.label_altitude.setText(_translate("GPSDialog", "Altitude:"))