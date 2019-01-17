# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PickColor.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SelectColor(object):
    def setupUi(self, SelectColor):
        SelectColor.setObjectName("SelectColor")
        SelectColor.resize(1062, 451)
        self.verticalLayout = QtWidgets.QVBoxLayout(SelectColor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(SelectColor)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.LblColorSelected = QtWidgets.QLabel(SelectColor)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.LblColorSelected.setFont(font)
        self.LblColorSelected.setObjectName("LblColorSelected")
        self.verticalLayout.addWidget(self.LblColorSelected)
        self.LblColor = QtWidgets.QLabel(SelectColor)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.LblColor.setFont(font)
        self.LblColor.setObjectName("LblColor")
        self.verticalLayout.addWidget(self.LblColor)
        self.LblPalette = QtWidgets.QLabel(SelectColor)
        self.LblPalette.setObjectName("LblPalette")
        self.verticalLayout.addWidget(self.LblPalette)
        self.ColorSlider = QtWidgets.QSlider(SelectColor)
        self.ColorSlider.setMaximum(1530)
        self.ColorSlider.setPageStep(10)
        self.ColorSlider.setOrientation(QtCore.Qt.Horizontal)
        self.ColorSlider.setObjectName("ColorSlider")
        self.verticalLayout.addWidget(self.ColorSlider)
        self.LblSaturation = QtWidgets.QLabel(SelectColor)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.LblSaturation.setFont(font)
        self.LblSaturation.setObjectName("LblSaturation")
        self.verticalLayout.addWidget(self.LblSaturation)
        self.BrightnessSlider = QtWidgets.QSlider(SelectColor)
        self.BrightnessSlider.setMinimum(0)
        self.BrightnessSlider.setMaximum(255)
        self.BrightnessSlider.setOrientation(QtCore.Qt.Horizontal)
        self.BrightnessSlider.setInvertedAppearance(True)
        self.BrightnessSlider.setObjectName("BrightnessSlider")
        self.verticalLayout.addWidget(self.BrightnessSlider)
        self.LblBrightness = QtWidgets.QLabel(SelectColor)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.LblBrightness.setFont(font)
        self.LblBrightness.setObjectName("LblBrightness")
        self.verticalLayout.addWidget(self.LblBrightness)
        self.SuturationSlider = QtWidgets.QSlider(SelectColor)
        self.SuturationSlider.setMinimum(1)
        self.SuturationSlider.setMaximum(100)
        self.SuturationSlider.setProperty("value", 100)
        self.SuturationSlider.setOrientation(QtCore.Qt.Horizontal)
        self.SuturationSlider.setObjectName("SuturationSlider")
        self.verticalLayout.addWidget(self.SuturationSlider)
        self.buttonBox = QtWidgets.QDialogButtonBox(SelectColor)
        self.buttonBox.setSizeIncrement(QtCore.QSize(0, 0))
        self.buttonBox.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SelectColor)
        QtCore.QMetaObject.connectSlotsByName(SelectColor)

    def retranslateUi(self, SelectColor):
        _translate = QtCore.QCoreApplication.translate
        SelectColor.setWindowTitle(_translate("SelectColor", "Select Color"))
        self.LblColorSelected.setText(_translate("SelectColor", "Color:"))
        self.LblColor.setText(_translate("SelectColor", "255, 0, 0"))
        self.LblPalette.setText(_translate("SelectColor", "<html><head/><body><p><img src=\":/palette/palette.jpg\"/><img src=\"/palette.jpg\"/></p></body></html>"))
        self.LblSaturation.setText(_translate("SelectColor", "Saturation:"))
        self.LblBrightness.setText(_translate("SelectColor", "Brightness:"))

import palette_rc
