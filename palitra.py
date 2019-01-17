import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QDialogButtonBox
from PyQt5 import uic
from colorpicker import Ui_SelectColor

import resources_rc


class ColorDialog(QtWidgets.QDialog, Ui_SelectColor):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.palitra = QtGui.QPixmap(":/palitra/palitra.jpeg")
        self.LblColor.show()
        self.label_4.setAutoFillBackground(True)
        self.ColorSlider.valueChanged.connect(self.valuechange)
        self.BrightnessSlider.valueChanged.connect(self.valuechange)
        self.SuturationSlider.valueChanged.connect(self.valuechange)
        self.image = self.palitra.toImage()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.rgb = [255, 0, 0]

    def Color(self):
        return self.LblColor.text(), self.rgb

    def valuechange(self):
        hValue = self.ColorSlider.value()
        bValue = self.BrightnessSlider.value()
        sValue = self.SuturationSlider.value()
        Color = [0, 0, 0]
        if hValue < 255:
            Color[0] = 255
            Color[1] = hValue
        if 254  < hValue < 510:
            Color[0] = 255 - (hValue % 255)
            Color[1] = 255
        if 509 < hValue < 765:
            Color[1] = 255
            Color[2] = hValue % 255
        if 764 < hValue < 1020:
            Color[1] = 255 - (hValue % 255)
            Color[2] = 255
        if 1019 < hValue < 1275:
            Color[0] = hValue % 255
            Color[2] = 255
        if 1274 < hValue < 1530:
            Color[0] = 255
            Color[2] = 255 - hValue % 255
        if 1530 == hValue:
            Color[0] = 255

        # в текст
        Color = [255 if x + bValue > 256 else x + bValue for x in Color]
        Color = [(x*sValue)/100 for x in Color]

        # в отрисовку
        c = self.image.pixel(1529 if hValue == 1530 else hValue, 0)
        cpix = QtGui.QColor(c).getRgbF()
        cpix = [int((x * 255 * sValue)/100) for x in cpix]
        cpix = [255 if x + bValue >= 256 else x + bValue for x in cpix]
        # для динамической отрисовки
        self.LblColor.setText('%d, %d, %d' % (Color[0],Color[1],Color[2]))
        #self.label_3.setText('Saturation : %d' % bValue)
        # self.label_5.setText('Brightness %d%%' % sValue)
        #Цвет по модифицированой палитрой, выводимые коды не соотвествуют цвету (sic!)
        self.label_4.setStyleSheet("QLabel { background-color : rgb(%d, %d, %d)}" % (cpix[0], cpix[1], cpix[2]))
        self.rgb = [cpix[0], cpix[1], cpix[2]]


    #с передачей значения из основной фаормы сделать можно, но !
    # востановить из 3 х значений ргб положения ползунков очень сложно
    #легче добавляя к передаче еще данные ползунков,
    # но лезть в реализацию чужих данныз нехочется

    @staticmethod
    def getColor():
        dialog = ColorDialog()
        result = dialog.exec_()
        color = dialog.Color()
        return (color, result == QDialog.Accepted)