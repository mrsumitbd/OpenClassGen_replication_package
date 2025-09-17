class Ui_GPSDialog(object):
    def setupUi(self, GPSDialog):
        GPSDialog.setObjectName("GPSDialog")
        GPSDialog.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(GPSDialog)
        self.gridLayout.setObjectName("gridLayout")
        
        self.label_latitude = QtWidgets.QLabel(GPSDialog)
        self.label_latitude.setObjectName("label_latitude")
        self.gridLayout.addWidget(self.label_latitude, 0, 0, 1, 1)
        
        self.lineEdit_latitude = QtWidgets.QLineEdit(GPSDialog)
        self.lineEdit_latitude.setObjectName("lineEdit_latitude")
        self.gridLayout.addWidget(self.lineEdit_latitude, 0, 1, 1, 1)
        
        self.label_longitude = QtWidgets.QLabel(GPSDialog)
        self.label_longitude.setObjectName("label_longitude")
        self.gridLayout.addWidget(self.label_longitude, 1, 0, 1, 1)
        
        self.lineEdit_longitude = QtWidgets.QLineEdit(GPSDialog)
        self.lineEdit_longitude.setObjectName("lineEdit_longitude")
        self.gridLayout.addWidget(self.lineEdit_longitude, 1, 1, 1, 1)
        
        self.label_altitude = QtWidgets.QLabel(GPSDialog)
        self.label_altitude.setObjectName("label_altitude")
        self.gridLayout.addWidget(self.label_altitude, 2, 0, 1, 1)
        
        self.lineEdit_altitude = QtWidgets.QLineEdit(GPSDialog)
        self.lineEdit_altitude.setObjectName("lineEdit_altitude")
        self.gridLayout.addWidget(self.lineEdit_altitude, 2, 1, 1, 1)
        
        self.buttonBox = QtWidgets.QDialogButtonBox(GPSDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        
        self.retranslateUi(GPSDialog)
        self.buttonBox.accepted.connect(GPSDialog.accept)
        self.buttonBox.rejected.connect(GPSDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GPSDialog)

    def retranslateUi(self, GPSDialog):
        _translate = QtCore.QCoreApplication.translate
        GPSDialog.setWindowTitle(_translate("GPSDialog", "GPS Coordinates"))
        self.label_latitude.setText(_translate("GPSDialog", "Latitude:"))
        self.label_longitude.setText(_translate("GPSDialog", "Longitude:"))
        self.label_altitude.setText(_translate("GPSDialog", "Altitude:"))