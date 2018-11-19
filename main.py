import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap
import design
from Auxledsdata import *
import Mediator


# from PyQt5.QtGui import QIcon


class EffectTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, name):
        super().__init__([name])


class StepTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, name):
        super().__init__([name])


class ConfigTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, name):
        super().__init__([name])


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.data = AuxEffects()
        self.saved = True
        self.filename = ""

    def initUI(self):
        # useful lists of items
        self.leds_combo_list = [self.CBLed1, self.CBLed2, self.CBLed3, self.CBLed4, self.CBLed5, self.CBLed6,
                                self.CBLed7, self.CBLed8]
        self.leds = dict(list(zip(Mediator.leds_list, self.leds_combo_list)))
        self.step_leds_labels = [self.LBLLed1_2, self.LBLLed2_2, self.LBLLed3_2, self.LBLLed4_2, self.LBLLed5_2,
                                 self.LBLLed6_2, self.LBLLed7_2, self.LBLLed8_2]
        self.step_leds_brightnesses = [self.HSliderBrightness1, self.HSliderBrightness2, self.HSliderBrightness3,
                                       self.HSliderBrightness4, self.HSliderBrightness5, self.HSliderBrightness6,
                                       self.HSliderBrightness7, self.HSliderBrightness8]
        self.step_leds = dict(list(zip(Mediator.leds_list, [[x, y] for (x, y) in list(zip(self.step_leds_labels,
                                       self.step_leds_brightnesses))])))

        # add Logo
        self.ImgLogo = QPixmap('Logo.jpg')
        self.LblLogo = QtWidgets.QLabel(self)
        self.LblLogo.setPixmap(self.ImgLogo)
        self.gridLayout.addWidget(self.LblLogo, 2, 0, 12, 1)

        # add menu triggers
        #self.actionExit.triggered.connect((QtWidgets.qApp.quit))
        self.actionExit.triggered.connect(self.close)
        self.actionSave.triggered.connect(self.SavePressed)
        self.actionSave_As.triggered.connect(self.SaveAsPressed)

        # add button clicks
        self.BtnCreate.clicked.connect(self.AddEffect)
        self.BtnAddSequence.clicked.connect(self.AddSequence)
        self.BtnAddStep.clicked.connect(self.AddStep)
        self.BtnRepeat.clicked.connect(self.AddRepeatStep)
        self.BtnDelete.clicked.connect(self.DeleteItem)

        self.TxtName.textChanged[str].connect(self.NameChanged)
        self.CBLedsAll.clicked.connect(self.CheckAllLeds)
        for led in self.step_leds_brightnesses:
            led.valueChanged.connect(self.BrightnessChanged)
        self.LstEffects.currentItemChanged.connect(self.EffectClicked)
        self.TrStructure.itemPressed.connect(self.TreeItemChanged)

    def AddEffect(self):
        self.saved = False
        self.ChangeAuxTitle(self.filename, self.saved)
        name = self.TxtName.text()
        self.data.AddEffect(name)
        self.BtnCreate.setEnabled(False)
        self.LstEffects.addItem(name)
        effect = EffectTreeItem(name)
        self.TrStructure.addTopLevelItem(effect)

    def NameChanged(self, name):
        effects = self.data.GetEffectsList()
        enabled = True if name and name not in effects else False
        self.BtnCreate.setEnabled(enabled)

    def EffectClicked(self, item):
        name = item.text()
        root = self.TrStructure.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            item_text = item.text(0)
            if item_text == name:
                self.TrStructure.setCurrentItem(item)
                self.TreeItemChanged(item)

    def StepControlsDisable(self):
        self.SpinWait.setEnabled(False)  # all step controls are disabled
        self.SpinSmooth.setEnabled(False)
        self.ComboRepeat.setEnabled(False)
        self.ComboRepeat.clear()
        self.ComboCount.setEnabled(False)
        self.BtnAddStep.setEnabled(False)
        self.BtnRepeat.setEnabled(False)
        self.TxtStepName.setEnabled(False)
        self.BtnRepeat.setEnabled(False)
        for label in self.step_leds_labels:
            label.setEnabled(False)
        for led in self.step_leds_brightnesses:
            led.setEnabled(False)

    def StepControlsEnable(self):
        self.SpinWait.setEnabled(True)  # all step controls are enabled, but only available leds controls enabled
        self.SpinSmooth.setEnabled(True)
        self.ComboRepeat.setEnabled(True)
        self.ComboCount.setEnabled(True)
        self.BtnAddStep.setEnabled(True)
        self.TxtStepName.setEnabled(True)
        self.EnableLedsList()
        self.GetStepsNames()


    def ClearStepControls(self):
        self.SpinWait.setValue(0)
        self.SpinSmooth.setValue(0)
        self.TxtStepName.clear()
        for led in self.step_leds_brightnesses:
            led.setValue(0)

    def TreeItemChanged(self, current):
        if type(current) is EffectTreeItem:
            self.BtnAddSequence.setEnabled(True)  # if item is toplevel we can add sequencer
            name = current.text(0)
            disabled_leds = self.data.GetUsedLedsList(name)
            for led in Mediator.leds_list:      # used leds are checked and disabled
                if led not in disabled_leds:
                    self.leds[led].setEnabled(True)
                    self.leds[led].setChecked(False)
                else:                             # unused leds are enablled and unchecked
                    self.leds[led].setEnabled(False)
                    self.leds[led].setChecked(True)
            self.CBLedsAll.setEnabled(True)
            self.CBLedsAll.setChecked(False)
            self.StepControlsDisable()
        else:
            self.BtnAddSequence.setEnabled(False)  # for not top-level items sequencer and leds are not available
            for led in self.leds_combo_list:
                led.setEnabled(False)
            self.CBLedsAll.setEnabled(False)
            self.CBLedsAll.setChecked(False)
            if type(current) is ConfigTreeItem:
                self.StepControlsEnable()
            else:
                self.StepControlsDisable()
        self.ClearStepControls()
        self.BtnDelete.setEnabled(True)

    def EnableLedsList(self):
        current = self.TrStructure.currentItem()
        current_name = current.text(0)
        leds = Mediator.get_leds_from_config(current_name)
        for led in Mediator.leds_list:
            if led in leds:
                self.step_leds[led][0].setEnabled(True)
                self.step_leds[led][1].setEnabled(True)
                current_label = self.step_leds[led][0].text()
                current_brightness = self.step_leds[led][1].value()
                self.step_leds[led][0].setText(current_label.split()[0] + ' ' + str(current_brightness))
            else:
                self.step_leds[led][0].setEnabled(False)
                self.step_leds[led][1].setEnabled(False)
                self.step_leds[led][0].setText(self.stepleds[led][0].text().split()[0])

    def GetStepsNames(self):
        self.ComboRepeat.clear()
        current = self.TrStructure.currentItem()
        effect = current.parent().text(0)
        number = self.GetItemId(current)
        step_names = self.data.GetStepsList(effect, number)
        for name in step_names:
            self.ComboRepeat.addItem(name)
        if step_names:
            self.BtnRepeat.setEnabled(True)


    def GetItemId(self, item):
        parent = self.TrStructure.invisibleRootItem() if type(item) == EffectTreeItem else item.parent()
        for i in range(parent.childCount()):
            if parent.child(i) == item:
                return i

    def AddSequence(self):
        current_effect = self.TrStructure.currentItem()
        current_name = current_effect.text(0)
        leds_to_add = [led for led in Mediator.leds_list if self.leds[led].isChecked() and self.leds[led].isEnabled()]
        if leds_to_add:
            self.data.CreateSequencer(current_name, leds_to_add)
            for led in leds_to_add:
                self.leds[led].setEnabled(False)
            config_item = ConfigTreeItem(Mediator.get_config_name_from_leds(leds_to_add))
            current_effect.addChild(config_item)
            self.saved = False
            self.ChangeAuxTitle(self.filename, self.saved)

    def BrightnessChanged(self, value):
        source = self.sender()
        for led in self.step_leds:
            if self.step_leds[led][1] == source:
                self.step_leds[led][0].setText(self.step_leds[led][0].text().split()[0] + " " + str(value))

    def AddStep(self):
        current = self.TrStructure.currentItem()
        effect = current.parent().text(0)
        number = self.GetItemId(current)
        name = self.TxtStepName.text()
        steps_names = self.data.GetStepsList(effect, number)
        if name in steps_names:
            self.ErrorMessage("Step with this name is already used")
        else:
            brightnesses = list()
            for led in self.step_leds_brightnesses:
                if led.isEnabled():
                    brightnesses.append(led.value())
            wait = self.SpinWait.value()
            smooth = self.SpinSmooth.value()
            self.data.CreateStep(effect, number, name, brightnesses, wait, smooth)
            step_text = Mediator.get_step_name(name, brightnesses, wait, smooth)
            step_item = StepTreeItem(step_text)
            current.addChild(step_item)
            self.saved = False
            self.ChangeAuxTitle(self.filename, self.saved)
        self.GetStepsNames()

    def AddRepeatStep(self):
        current = self.TrStructure.currentItem()
        effect = current.parent().text(0)
        number = self.GetItemId(current)
        startstep = self.ComboRepeat.currentText()
        count = self.ComboCount.currentText()
        self.data.CreateRepeatStep(effect, number, startstep, count)
        step_text = Mediator.get_repeat_name(startstep, count)
        step_item = StepTreeItem(step_text)
        current.addChild(step_item)
        self.saved = False
        self.ChangeAuxTitle(self.filename, self.saved)

    def DeleteItem(self):
        current = self.TrStructure.currentItem()
        current_name = current.text(0)
        self.saved = False
        self.ChangeAuxTitle(self.filename, self.saved)
        if isinstance(current, EffectTreeItem):
            self.data.DeleteItem(current_name, [])
            root = self.TrStructure.invisibleRootItem()
            root.removeChild(current)
        if isinstance(current, ConfigTreeItem):
            parent = current.parent()
            effect = parent.text(0)
            number = self.GetItemId(current)
            self.data.DeleteItem(Mediator.config_name, [effect, number])
            parent.removeChild(current)
            if parent.childCount() == 0:
                self.data.DeleteItem(number, [effect])
        if isinstance(current, StepTreeItem):
            parent = current.parent()
            grandpa = parent.parent()
            seq_number = self.GetItemId(parent)
            effect = grandpa.text(0)
            step_number = self.GetItemId(current)
            used_steps = self.data.GetRepeatList(effect, seq_number)
            step_name = Mediator.get_currrent_step_name(current_name)
            if step_name in used_steps:
                self.ErrorMessage("This step is used in repeat step, first delete repeat step")
            else:
                self.data.DeleteItem(step_number, [effect, seq_number, Mediator.seq_name])
                parent.removeChild(current)


    def CheckAllLeds(self):
        state = self.CBLedsAll.isChecked()
        for led in self.leds_combo_list:
            if led.isEnabled():
                led.setChecked(state)

    def SavePressed(self):
        if not self.filename:
            self.filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "")[0]
        if self.filename:
            self.data.GetJsonToFile(self.filename)
            self.saved = True
            self.ChangeAuxTitle(self.filename, self.saved)

    def SaveAsPressed(self):
        self.filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "")[0]
        if self.filename:
            self.data.GetJsonToFile(self.filename)
            self.saved = True
            self.ChangeAuxTitle(self.filename, self.saved)


    def ErrorMessage(self, text):
        error = QMessageBox()
        error.setIcon(QMessageBox.Critical)
        error.setText(text)
        error.setWindowTitle("Error")
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()

    def ChangeAuxTitle(self, filename, saved):
        if filename:
            text = "AuxLeds - %s" % filename.split(r'/')[-1]
        else:
            text = 'AuxLeds'
        if not saved:
            text += "*"
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TabAuxLEDs), QtCore.QCoreApplication.translate("MainWindow", text))

    def closeEvent(self, event):
        if not self.saved:
            quit_msg = "You have unsaved profile. Do you want to save?"
            reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.SavePressed()
        event.accept()




def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()