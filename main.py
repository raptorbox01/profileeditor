import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap
import design
from Auxledsdata import *

from PyQt5.QtGui import QIcon


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.initUI()
        self.data = AuxEffects()

    def initUI(self):
        #useful lists of items
        self.ledsdict = {"Led1": self.CBLed1, "Led2": self.CBLed2, "Led3": self.CBLed3, "Led4": self.CBLed4,
                         "Led5": self.CBLed5, "Led6": self.CBLed6, "Led7": self.CBLed7, "Led8": self.CBLed8}
        self.ledslist = self.ledsdict.values()
        self.stepleds = {"Led1": [self.LBLLed1_2, self.HSliderBrightness1], "Led2": [self.LBLLed2_2, self.HSliderBrightness2],
                               "Led3": [self.LBLLed3_2, self.HSliderBrightness3], "Led4": [self.LBLLed4_2, self.HSliderBrightness4],
                               "Led5": [self.LBLLed5_2, self.HSliderBrightness5], "Led6": [self.LBLLed6_2, self.HSliderBrightness6],
                               "Led7": [self.LBLLed7_2, self.HSliderBrightness7], "Led8": [self.LBLLed8_2, self.HSliderBrightness8]}
        self.steplabels = [item[0] for item in self.stepleds.values()]
        self.stepbrightness = [item[1] for item in self.stepleds.values()]

        #add Logo
        self.ImgLogo = QPixmap('Logo.jpg')
        self.LblLogo = QtWidgets.QLabel(self)
        self.LblLogo.setPixmap(self.ImgLogo)
        self.gridLayout.addWidget(self.LblLogo, 2, 0, 12, 1)

        #add menu triggers
        self.actionExit.triggered.connect((QtWidgets.qApp.quit))
        self.actionSave.triggered.connect(self.SavePressed)

        #add button clicks
        self.BtnCreate.clicked.connect(self.ClickCreated)
        self.BtnAddSequence.clicked.connect(self.AddSequence)
        self.BtnAddStep.clicked.connect(self.AddStep)
        self.BtnRepeat.clicked.connect(self.AddRepeatStep)
        self.BtnDelete.clicked.connect(self.DeleteItem)

        self.TxtName.textChanged[str].connect(self.NameChanged)
        self.CBLedsAll.clicked.connect(self.CheckAllLeds)
        for led in self.stepbrightness:
            led.valueChanged.connect(self.BrightnessChanged)

        self.LstEffects.currentItemChanged.connect(self.EffectClicked)
        #self.TrStructure.currentItemChanged.connect(self.TreeItemChanged)
        #self.TrStructure.itemActivated.connect(self.TreeItemChanged)
        #self.TrStructure.itemClicked.connect(self.TreeItemChanged)
        self.TrStructure.itemPressed.connect(self.TreeItemChanged)


    def ClickCreated(self):
        name = self.TxtName.text()
        self.data.AddEffect(name)
        self.BtnCreate.setEnabled(False)
        self.LstEffects.addItem(name)
        effect = QtWidgets.QTreeWidgetItem([name])
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


    def GetItemType(self, item: QtWidgets.QTreeWidgetItem):
        root = self.TrStructure.invisibleRootItem()
        children = [root.child(i) for i in range(root.childCount())]
        if item in children:
            return "Effect"
        parent = item.parent()
        if parent in children:
            return "Sequencer"
        grandpa = parent.parent()
        if grandpa in children:
            return "Config"
        return "Step"


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
        for label in self.steplabels:
            label.setEnabled(False)
        for led in self.stepbrightness:
            led.setEnabled(False)

    def TreeItemChanged(self, current):

        item_type = self.GetItemType(current)
        if item_type == 'Effect':
            self.BtnAddSequence.setEnabled(True)  # if item is toplevel we can add sequencer
            name = current.text(0)

            disabled_leds = self.data.GetUsedLedsList(name)
            for led in self.ledsdict.keys():      # used leds are checked and disabled
                if led not in disabled_leds:
                    self.ledsdict[led].setEnabled(True)
                    self.ledsdict[led].setChecked(False)
                else:                             # unused leds are enablled and unchecked
                    self.ledsdict[led].setEnabled(False)
                    self.ledsdict[led].setChecked(True)
            self.CBLedsAll.setEnabled(True)
            self.CBLedsAll.setChecked(False)
            self.StepControlsDisable()


        else:
            self.BtnAddSequence.setEnabled(False)  #for not top-level items sequencer and leds are not available
            for led in self.ledslist:
                led.setEnabled(False)
            self.CBLedsAll.setEnabled(False)
            self.CBLedsAll.setChecked(False)

            if item_type != 'Step':
                self.SpinWait.setEnabled(True)  # all step controls are enabled, but only available leds controls enabled
                self.SpinSmooth.setEnabled(True)
                self.ComboRepeat.setEnabled(True)
                self.ComboCount.setEnabled(True)
                self.BtnAddStep.setEnabled(True)
                #self.BtnRepeat.setEnabled(True)
                self.TxtStepName.setEnabled(True)
                self.EnableLedsList()
                self.GetStepsNames()
            else:
                self.StepControlsDisable()

        self.SpinWait.setValue(0)
        self.SpinSmooth.setValue(0)
        self.TxtStepName.clear()
        for led in self.stepbrightness:
            led.setValue(0)
        self.BtnDelete.setEnabled(True)




    def EnableLedsList(self):
        current = self.TrStructure.currentItem()
        currentName = current.text(0)
        if 'Sequencer' in currentName:
            current = current.child(0)
            currentName = current.text(0)
        leds = currentName.split(", ")
        for led in self.stepleds.keys():
            if led in leds:
                self.stepleds[led][0].setEnabled(True)
                self.stepleds[led][1].setEnabled(True)
                currentLabel = self.stepleds[led][0].text()
                currentBrightness = self.stepleds[led][1].value()
                self.stepleds[led][0].setText(currentLabel.split()[0] +' ' + str(currentBrightness))

            else:
                self.stepleds[led][0].setEnabled(False)
                self.stepleds[led][1].setEnabled(False)
                self.stepleds[led][0].setText(self.stepleds[led][0].text().split()[0])

    def GetStepsNames(self):
        self.ComboRepeat.clear()
        current = current = self.TrStructure.currentItem()
        current_name = current.text(0)
        if 'Sequencer' not in current_name:
            current = current.parent()
            current_name = current.text(0)
        effect = current.parent().text(0)
        number = int(current.text(0).replace('Sequencer', ""))-1
        step_names = self.data.GetStepsList(effect, number)
        for name in step_names:
            self.ComboRepeat.addItem(name)
        if step_names:
            self.BtnRepeat.setEnabled(True)


    def AddSequence(self):
        currentEffect = self.TrStructure.currentItem()
        currentEffectName = currentEffect.text(0)
        leds_to_add = [led for  led in self.ledsdict if self.ledsdict[led].isChecked() and self.ledsdict[led].isEnabled()]
        if leds_to_add:
            self.data.CreateSequencer(currentEffectName, leds_to_add)
            for led in leds_to_add:
                self.ledsdict[led].setEnabled(False)
            seq_item = QtWidgets.QTreeWidgetItem(['Sequencer' + str(currentEffect.childCount()+1)])
            currentEffect.addChild(seq_item)
            config_item = QtWidgets.QTreeWidgetItem([', '.join(leds_to_add)])
            seq_item.addChild(config_item)


    def BrightnessChanged(self, value):
        source = self.sender()
        for led in self.stepleds:
            if self.stepleds[led][1] == source:
                self.stepleds[led][0].setText(self.stepleds[led][0].text().split()[0] + " " + str(value))

    def AddStep(self):
        current = self.TrStructure.currentItem()
        current_name = current.text(0)
        if 'Sequencer' not in current_name:
            current = current.parent()
            current_name = current.text(0)
        effect = current.parent().text(0)
        number = int(current.text(0).replace('Sequencer', ""))-1
        name = self.TxtStepName.text()
        steps_names = self.data.GetStepsList(effect, number)
        if name in steps_names:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("This step name is already used")
            error.setWindowTitle("Error")
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()
        else:
            brightnesses = list()
            for led in self.stepbrightness:
                if led.isEnabled():
                    brightnesses.append(led.value())
            wait = self.SpinWait.value()
            smooth = self.SpinSmooth.value()
            self.data.CreateStep(effect, number, name, brightnesses, wait, smooth)

            step_text = []
            if name:
                step_text.append('Name: %s ' % name)
            brightnesses = list(map(str, brightnesses))
            brightnesses =  ', '.join(brightnesses)
            step_text.append("Brightness: [%s]" % brightnesses)
            if wait > 0:
                step_text.append('Wait: %i' % wait)
            if smooth > 0:
                step_text.append('Smooth: %i' % smooth)
            step_text = ', '.join(step_text)

            step_item = QtWidgets.QTreeWidgetItem([step_text])
            current.child(0).addChild(step_item)
        self.GetStepsNames()

    def AddRepeatStep(self):
        current = self.TrStructure.currentItem()
        current_name = current.text(0)
        if 'Sequencer' not in current_name:
            current = current.parent()
            current_name = current.text(0)
        effect = current.parent().text(0)
        number = int(current.text(0).replace('Sequencer', "")) - 1
        startstep = self.ComboRepeat.currentText()
        count = self.ComboCount.currentText()
        self.data.CreateRepeatStep(effect, number, startstep, count)
        step_text = "Repeat: StartFrom: %s, Count: %s" % (startstep, count)
        step_item = QtWidgets.QTreeWidgetItem([step_text])
        current.child(0).addChild(step_item)


    def DeleteItem(self):
        current = self.TrStructure.currentItem()
        current_name = current.text(0)
        current_type = self.GetItemType(current)
        if current_type == 'Effect':
            self.data.DeleteItem(current_name, [])
            root = self.TrStructure.invisibleRootItem()
            root.removeChild(current)
        else:
            if current_type == 'Sequencer':
                number = int(current_name.replace("Sequencer", "")) - 1
                self.data.DeleteItem(number, [current.parent().text(0)])
                current.parent().removeChild(current)
            if current_type == 'Config':
                parent = current.parent()
                grandpa = parent.parent()
                effect = grandpa.text(0)
                number = int(parent.text(0).replace("Sequencer", "")) - 1
                self.data.DeleteItem("Config", [effect, number])
                if parent.childCount() == 1:
                    grandpa.removeChild(parent)
                    self.data.DeleteItem(number, [effect])
                else:
                    parent.removeChild(current)
            if current_type == 'Step':
                parent = current.parent()
                grandpa = parent.parent()
                ancestor = grandpa.parent()
                number = int(grandpa.text(0).replace("Sequencer", "")) - 1
                effect = ancestor.text(0)







    def CheckAllLeds(self):
        state = self.CBLedsAll.isChecked()
        for led in self.ledslist:
            if led.isEnabled():
                led.setChecked(state)



    def SavePressed(self):
        self.data.GetJsonToFile("test.ini")





def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()