class Ui_GPSDialog(object):
    def setupUi(self, GPSDialog):
        GPSDialog.setObjectName("GPSDialog")
        GPSDialog.resize(400, 150)
        self.gridLayout = QtWidgets.QGridLayout(GPSDialog)
        self.gridLayout.setObjectName("gridLayout")

        self.labelLatitude = QtWidgets.QLabel(GPSDialog)
        self.labelLatitude.setObjectName("labelLatitude")
        self.gridLayout.addWidget(self.labelLatitude, 0, 0, 1, 1)
        self.lineEditLatitude = QtWidgets.QLineEdit(GPSDialog)
        self.lineEditLatitude.setObjectName("lineEditLatitude")
        self.gridLayout.addWidget(self.lineEditLatitude, 0, 1, 1, 1)

        self.labelLongitude = QtWidgets.QLabel(GPSDialog)
        self.labelLongitude.setObjectName("labelLongitude")
        self.gridLayout.addWidget(self.labelLongitude, 1, 0, 1, 1)
        self.lineEditLongitude = QtWidgets.QLineEdit(GPSDialog)
        self.lineEditLongitude.setObjectName("lineEditLongitude")
        self.gridLayout.addWidget(self.lineEditLongitude, 1, 1, 1, 1)

        self.labelAltitude = QtWidgets.QLabel(GPSDialog)
        self.labelAltitude.setObjectName("labelAltitude")
        self.gridLayout.addWidget(self.labelAltitude, 2, 0, 1, 1)
        self.lineEditAltitude = QtWidgets.QLineEdit(GPSDialog)
        self.lineEditAltitude.setObjectName("lineEditAltitude")
        self.gridLayout.addWidget(self.lineEditAltitude, 2, 1, 1, 1)

        self.buttonBox = QtWidgets.QDialogButtonBox(GPSDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.retranslateUi(GPSDialog)
        self.buttonBox.accepted.connect(GPSDialog.accept)
        self.buttonBox.rejected.connect(GPSDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GPSDialog)

    def retranslateUi(self, GPSDialog):
        _translate = QtCore.QCoreApplication.translate
        GPSDialog.setWindowTitle(_translate("GPSDialog", "GPS Coordinates"))
        self.labelLatitude.setText(_translate("GPSDialog", "Latitude:"))
        self.labelLongitude.setText(_translate("GPSDialog", "Longitude:"))
        self.labelAltitude.setText(_translate("GPSDialog", "Altitude:"))