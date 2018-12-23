import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
import design
from Auxledsdata import *
from Commondata import *
from profiledata import *
import Mediator

from loguru import logger

logger.start("logfile.log", rotation="1 week", format="{time} {level} {message}", level="DEBUG", enqueue=True)

auxleds = 'AuxLEDs'
common = 'Common'
profiletab = 'Profiles'
tabnames = [auxleds, common, profiletab]


def initiate_exception_logging():
    # generating our hook
    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook

    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        logger.exception(f"{exctype}, {value}, {traceback}")
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        #sys.exit(1)

    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook


# from PyQt5.QtGui import QIcon


class StepTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, name):
        super().__init__([name])


class SequencerTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, name):
        super().__init__([name])


class ProfileEditor(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.auxdata = AuxEffects()
        self.commondata = CommonData()
        self.profiledata = Profiles()
        self.data = [self.auxdata, self.commondata, self.profiledata]
        self.saved = [True, True, True]
        self.filename = ["", "", ""]
        self.initAuxUI()
        self.CommonUI()
        self.ProfileUI()
        self.savefunctions = [self.auxdata.save_to_file, self.commondata.save_to_file, self.profiledata.save_to_file]
        self.openfunctions = [Mediator.translate_json_to_tree_structure, Mediator.get_common_data, Mediator.load_profiles]
        self.statusfields = [self.TxtAuxStatus, self.TxtCommonStatus, self.TxtProfileStatus]

    def initAuxUI(self):
        # useful lists of items
        self.leds_combo_list = [self.CBLed1, self.CBLed2, self.CBLed3, self.CBLed4, self.CBLed5, self.CBLed6,
                                self.CBLed7, self.CBLed8]
        self.leds = dict(list(zip(Mediator.leds_list, self.leds_combo_list)))
        self.leds_cb_str = dict(list(zip(self.leds_combo_list, Mediator.leds_list)))
        self.step_leds_brightnesses = [self.SpinBrightness1, self.SpinBrightness2, self.SpinBrightness3,
                                       self.SpinBrightness4, self.SpinBrightness5, self.SpinBrightness6,
                                       self.SpinBrightness7, self.SpinBrightness8]
        self.step_channels = [self.CBChannel1, self.CBChannel2, self.CBChannel3, self.CBChannel4, self.CBChannel5,
                              self.CBChannel6, self.CBChannel7, self.CBChannel8]
        self.step_brightness_dict = dict(list(zip(Mediator.leds_list, self.step_leds_brightnesses)))
        self.step_channels_dict = dict(list(zip(Mediator.leds_list, self.step_channels)))

        # add Logo
        # self.ImgLogo = QPixmap('Logo.jpg')
        # self.LblLogo = QtWidgets.QLabel(self)
        # self.LblLogo.setPixmap(self.ImgLogo)
        # self.gridLayout.addWidget(self.LblLogo, 2, 0, 12, 1)

        # add menu triggers
        self.actionExit.triggered.connect(self.close)
        self.actionSave.triggered.connect(self.SavePressed)
        self.actionSave_As.triggered.connect(self.SaveAsPressed)
        self.actionOpen.triggered.connect(self.OpenPressed)

        # add button clicks
        self.BtnAddGroup.clicked.connect(self.AddGroup)
        self.BtnAddSequencer.clicked.connect(self.AddSequencer)
        self.BtnDeleteGroup.clicked.connect(self.DeleteGroup)
        self.BtnAddStep.clicked.connect(self.AddStep)
        self.BtnDeleteSeq.clicked.connect(self.DeleteItem)
        # self.BtnRepeat.clicked.connect(self.AddRepeatStep)

        self.TxtGroup.textChanged[str].connect(self.GroupNameChanged)

        #for led in self.step_leds_brightnesses:
        #    led.valueChanged.connect(self.BrightnessChanged)
        self.LstGroup.itemPressed.connect(self.GroupClicked)
        self.TrStructure.itemPressed.connect(self.TreeItemChanged)

        for CB in self.leds_combo_list:
            CB.stateChanged.connect(self.LedClicked)

    def CommonUI(self):
        # list of common items
        self.blade1_controls = [self.SpinBand, self.SpinPixPerBand, self.SpinStartFlash]
        self.blade2_controls = [self.SpinBandNumber, self.SpinPixPerBand2, self.SpinStartFlash_2]
        self.volume_controls = [self.SpinCommon, self.SpinCoarseLow, self.SpinCoarseMid, self.SpinCoarseHigh]
        self.deadtime_controls = [self.SpinAfterPowerOn, self.SpinAfterBlaster, self.SpinAfterClash]
        self.other_ccntrols = [self.SpinPowerOffTimeout]
        self.swing_controls = [self.SpinSwingHighW, self.SpinSwingPercent, self.SpinSwingCircle, self.SpinSwingCircleW]
        self.spin_controls = [self.CBSpinEnabled, self.SpinSpinCounter, self.SpinSpinW, self.SpinSpinCircle,
                              self.SpinSpinWLow]
        self.clash_controls = [self.SpinClashHighA, self.SpinClashLength, self.SpinClashHitLevel, self.SpinClashLowW]
        self.stab_controls = [self.CBStabEnabled, self.SpinStabHighA, self.SpinStabLowW, self.SpinStabHitLevel,
                              self.SpinStabLength, self.SpinStabPercent]
        self.screw_controls = [self.CBScrewEnabled, self.SpinScrewHighW, self.SpinScrewLowW]
        self.common_controls = [self.blade1_controls, self.blade2_controls, self.volume_controls,
                                self.deadtime_controls, self.other_ccntrols]
        self.motion_controls = [self.swing_controls, self.spin_controls, self.clash_controls, self.stab_controls,
                                self.screw_controls]

        # common_controls_connect_maps
        self.common_dict = {}
        for i in range(len(self.common_controls)):
            keys_list = [[Mediator.main_sections[i], key] for key in Mediator.main_list[i]]
            self.common_dict.update(dict(list(zip(self.common_controls[i], keys_list))))
        self.motion_dict = {}
        for i in range(len(self.motion_controls)):
            keys_list = [[Mediator.motion_key, Mediator.motion_keys[i], key] for key in Mediator.motion_list[i]]
            self.motion_dict.update((dict(list(zip(self.motion_controls[i], keys_list)))))

        # common controls init
        for control_list in self.common_controls + self.motion_controls:
            for control in control_list:
                if control in (self.CBBlade2Enabled, self.CBSpinEnabled, self.CBStabEnabled, self.CBScrewEnabled):
                    control.stateChanged.connect(self.CBClicked)
                else:
                    control.valueChanged.connect(self.SpinChanged)

        self.SetDefaultCommon()
        self.BtnSave.clicked.connect(self.SavePressed)
        self.BtnDefault.clicked.connect(self.SetDefaultCommon)
        self.CBBlade2Enabled.stateChanged.connect(self.Blade2Clicked)

    def ProfileUI(self):
        # list of controls
        self.poweron = [self.SpinBladeSpeedOn]
        self.poweroff = [self.SpinPowerOffSpeed, self.CBMoveForward]
        self.working = [self.TxtWorkingColor, self.CBFlaming, self.CBFlickering]
        self.flaming = [self.SpinFlamingSizeMin, self.SpinFlamingSizeMax, self.SpinFlamingSpeedMin,
                        self.SpinFlamingSpeedMax,
                        self.SpinFlamingDelayMin, self.SpinFlamingDelayMax]
        self.flickering = [self.SpinFlickeringTimeMin, self.SpinFlickeringTimeMax, self.SpinFlickeringBrMin,
                           self.SpinFlickeringBrMax]
        self.blaster = [self.TxtBlasterColor, self.SpinBlasterDuration, self.SpinBlasterSizePix]
        self.clash = [self.TxtClashColor, self.SpinClashDuration, self.SpinClashSizePix]
        self.stab = [self.TxtStabColor, self.SpinStabDuration, self.SpinStabSizePix]
        self.lockup = [self.TxtLockupFlickerColor, self.SpinLockupTimeMin, self.SpinLockupTimeMax,
                       self.SpinLockupBrightnessMin, self.SpinLockupBrightnessMax, self.SpinLockupPeriodMin,
                       self.SpinLockupPeriodMax, self.TxtLockupFlashesColor, self.SpinLockupDuration,
                       self.SpinLockupSizepix]
        # map of tabs and their controls
        self.control_tab_dict = {1: self.poweron, 2: self.working, 3: self.poweroff, 4: self.flaming, 5: self.flickering,
                             6: self.blaster, 7: self.clash, 8: self.stab, 9: self.lockup}
        # map of color change data to their text field
        self.color_dict = {self.BtnBlasterColor: self.TxtBlasterColor, self.BtnClashColor: self.TxtClashColor,
                           self.BtnStabColor: self.TxtStabColor, self.BtnWorkingColor: self.TxtWorkingColor,
                           self.BtnLockupFlashesColor: self.TxtLockupFlashesColor,
                           self.BtnLockupFlickerColor: self.TxtLockupFlickerColor}
        # list of color text fields
        self.color_list = [self.TxtClashColor, self.TxtWorkingColor, self.TxtStabColor, self.TxtBlasterColor,
                           self.TxtLockupFlickerColor, self.TxtLockupFlashesColor]
        # map of min to max values in min max pairs
        self.min_max_dict = {self.SpinLockupTimeMin: self.SpinLockupTimeMax,
                             self.SpinLockupPeriodMin: self.SpinLockupPeriodMax,
                             self.SpinLockupBrightnessMin: self.SpinLockupBrightnessMax,
                             self.SpinFlickeringTimeMin: self.SpinFlickeringTimeMax,
                             self.SpinFlickeringBrMin: self.SpinFlickeringBrMax,
                             self.SpinFlamingSpeedMin: self.SpinFlamingSpeedMax,
                             self.SpinFlamingSizeMin: self.SpinFlamingSizeMax,
                             self.SpinFlamingDelayMin: self.SpinFlamingDelayMax}
        # lists of checkboxes
        self.CB_list = [self.CBFlickering, self.CBFlaming, self.CBMoveForward]
        self.extra_blade_CB_dict = {self.CBIndicate: Mediator.indicate_path, self.CBFlickeringAlwaysOn:
                                    Mediator.flickering_on_path, self.CBFlamingAlwaysOn: Mediator.flaming_on_path}
        # reverce of min max dict - map max value to min
        self.max_min_dict = dict([(self.min_max_dict[key], key) for key in self.min_max_dict.keys()])

        #create map of controls to key path in data dictionary (path lists from Mediator file)
        self.profile_dict = {}
        for i in self.control_tab_dict.keys():
            keys_list = []
            for key in Mediator.profile_list[i - 1]:
                keys_list.append([Mediator.tab_list[i - 1]] + key)
            self.profile_dict.update(dict(list(zip(self.control_tab_dict[i], keys_list))))
        #set data change handlers
        for control in self.profile_dict.keys():
            if control in self.CB_list:
                control.stateChanged.connect(self.ProfileCBClicked)
            else:
                if control in self.color_list:
                    control.textChanged.connect(self.ProfileTextChanged)
                else:
                    control.valueChanged.connect(self.ProfileSpinChanged)

        for color_button in self.color_dict.keys():
            color_button.clicked.connect(self.ColorChanged)

        for CB in self.extra_blade_CB_dict.keys():
            CB.clicked.connect(self.ExtraBladeCBlicked)

        self.BtnProfile.clicked.connect(self.AddProfile)
        self.BtnDeleteProfile.clicked.connect(self.DeleteProfile)
        self.BtnAddColor.clicked.connect(self.AddColor)
        self.BtnDeleteColor.clicked.connect(self.DeleteColor)
        self.BtnCReateAux.clicked.connect(self.ProfileAddAux)
        self.BtnAuxDelete.clicked.connect(self.DeleteAux)

        self.TabEffects.currentChanged.connect(self.EffectTabChanged)
        self.TxtAddProfile.textChanged[str].connect(self.ProfileNameChanged)
        self.LstProfile.itemPressed.connect(self.ProfileClicked)
        self.LstFlamingColor.itemPressed.connect(self.ColorClicked)
        self.LstAuxProfile.itemPressed.connect(self.AuxClicked)
        self.CBBlade.currentIndexChanged.connect(self.BladeChanged)
        self.SpinDelayBeforeOn.valueChanged.connect(self.DelayChanged)


    def AddGroup(self):
        """
        Adds group to UI and data if name is correct
        disables used leds
        """
        name: str = self.TxtGroup.text()
        leds_clicked: List[QtWidgets.QComboBox] = [CB for CB in self.leds_combo_list if CB.isChecked() and CB.isEnabled()]
        leds_list: List[str] = [self.leds_cb_str[CB] for CB in leds_clicked]
        group_to_add, error = self.auxdata.add_group(name, leds_list)
        if group_to_add is None:
            self.ErrorMessage(error)
        else:
            self.LstGroup.addItem(str(group_to_add))
            self.saved[0] = False
            self.ChangeTabTitle(auxleds, self.tabWidget.currentIndex())
            self.BtnAddGroup.isEnabled()
            for CB in leds_clicked:
                CB.setEnabled(False)
            self.BtnAddGroup.setEnabled(False)

    def GroupNameChanged(self, name):
        """
        enables add group button if name is not empty and some leds are checked
        :param name:
        :return:
        """
        enabled = True if name and any([CB.isChecked() and CB.isEnabled() for CB in self.leds_combo_list]) else False
        self.BtnAddGroup.setEnabled(enabled)

    def LedClicked(self):
        """
        changes status of add group button if some leds are selected/are not selected
        :return:
        """
        name = self.TxtGroup.text()
        enabled = True if name and any([CB.isChecked() and CB.isEnabled() for CB in self.leds_combo_list]) else False
        self.BtnAddGroup.setEnabled(enabled)


    def GroupClicked(self):
        """
        enables Sequence controls and Delete Button
        :return:
        """
        self.BtnDeleteGroup.setEnabled(True)
        self.SequenceControlsEnable()

    def DeleteGroup(self):
        """
        deletes group if it is not used in any Sequencer
        :return:
        """
        group = self.LstGroup.currentItem().text()
        leds_to_free = self.auxdata.delete_group_and_enable_leds(group)
        if not leds_to_free:
            self.ErrorMessage("This group is used un sequencers, remove or edit them first")
        else:
            # enabled freed leds
            for led in leds_to_free:
                self.leds[led].setEnabled(True)
                self.leds[led].setChecked(False)
            # reload group list
            self.LstGroup.clear()
            for group in self.auxdata.LedGroups:
                self.LstGroup.addItem(str(group))
            # disable delete button and sequencer controls
            self.BtnDeleteGroup.setEnabled(False)
            self.SequenceControlsDisable()
            #data is unsaved now
            self.saved[0] = False
            self.ChangeTabTitle(auxleds, 0)

    def SequenceControlsEnable(self):
        """
        enables all sequencer controls
        :return:
        """
        self.TxtSeqName.setEnabled(True)
        self.BtnAddSequencer.setEnabled(True)
        self.CBSeqList.setEnabled(True)
        if self.CBSeqList.count() > 0:
            self.BtnCopySeq.setEnabled(True)

    def SequenceControlsDisable(self):
        """
        disables all sequencer controls
        :return:
        """
        self.TxtSeqName.setEnabled(False)
        self.BtnAddSequencer.setEnabled(False)
        self.CBSeqList.setEnabled(False)
        self.BtnCopySeq.setEnabled(False)

    def AddSequencer(self):
        """
        Adds new Sequencer to gui and data
        :return:
        """
        seq_name = self.TxtSeqName.text()
        group_name = self.LstGroup.currentItem().text()
        seq, error = self.auxdata.create_sequence(group_name, seq_name)
        if not seq:
            self.ErrorMessage(error)
        else:
            seq_item = SequencerTreeItem(str(seq))
            self.TrStructure.addTopLevelItem(seq_item)
            self.saved[0] = False
            self.ChangeTabTitle(auxleds, self.tabWidget.currentIndex())
            self.CBAuxList.addItem(seq_name)  # add sequencer to aux section on profile tab
            self.CBSeqList.addItem(seq_name)  # add sequencer to copy sequencer section
            self.BtnCopySeq.setEnabled(True)

    def StepControlsDisable(self):
        """
        disable all step controls
        :return:
        """
        self.TxtStepName.setEnabled(False)
        self.SpinWait.setEnabled(False)
        self.SpinSmooth.setEnabled(False)
        self.BtnAddStep.setEnabled(False)
        self.BtnDeleteStep.setEnabled(False)
        for brightness in self.step_leds_brightnesses:
            brightness.setEnabled(False)
        for channel in self.step_channels:
            channel.setEnabled(False)
        self.CBStartrom.setEnabled(False)
        self.SpinCount.setEnabled(False)
        self.CBForever.setEnabled(False)
        self.BtnAddRepeat.setEnabled(False)
        self.BtnDeleteRepeat.setEnabled(False)

    def StepControlsEnable(self):
        """
        enable step controls, enable only used in tis sequencer led group led brightness and channels
        :return:
        """
        self.TxtStepName.setEnabled(True)
        self.SpinWait.setEnabled(True)  # all step controls are enabled, but only available leds controls enabled
        self.SpinSmooth.setEnabled(True)
        self.BtnAddStep.setEnabled(True)
        # get leds for tis sequencer led group and enable its brightnesses and channels
        leds_list = self.auxdata.get_led_list(self.TrStructure.currentItem().text(0))
        for brightness in self.step_brightness_dict.keys():
            if brightness in leds_list:
                self.step_brightness_dict[brightness].setEnabled(True)
            else:
                self.step_brightness_dict[brightness].setEnabled(False)
        for channel in self.step_channels_dict.keys():
            if channel in leds_list:
                self.step_channels_dict[channel].setEnabled(True)
            else:
                self.step_channels_dict[channel].setEnabled(False)
        # if any steps to repeat, enable step repeat section
        if self.CBStartrom.count() > 0:
            self.CBStartrom.setEnabled(True)
            self.SpinCount.setEnabled(True)
            self.BtnAddRepeat.setEnabled(True)
        #self.GetStepsNames()

    def ClearStepControls(self):
        """
        load new data for step controls
        :return:
        """
        self.SpinWait.setValue(0)
        self.SpinSmooth.setValue(0)
        self.TxtStepName.clear()
        for led in self.step_leds_brightnesses:
            led.setValue(0)
        for channel in self.step_channels:
            channel.setCurrentIndex(0)

    def TreeItemChanged(self, current):
        self.BtnAddStep.setEnabled(False)  # for not top-level items sequencer and leds are not available
        if isinstance(current, SequencerTreeItem):
            self.StepControlsEnable()
            self.ClearStepControls()
            self.BtnDeleteSeq.setEnabled(True)
            self.BtnDeleteStep.setEnabled(False)
        if isinstance(current, StepTreeItem):
            self.BtnDeleteStep.setEnabled(True)
            self.BtnDeleteSeq.setEnabled(False)


    # def GetStepsNames(self):
    #     self.ComboRepeat.clear()
    #     current = self.TrStructure.currentItem()
    #     effect = current.parent().text(0)
    #     number = self.GetItemId(current)
    #     step_names = self.auxdata.GetStepsList(effect, number)
    #     for name in step_names:
    #         self.ComboRepeat.addItem(name)
    #     if step_names:
    #         self.BtnRepeat.setEnabled(True)
    #
    # def GetItemId(self, item):
    #     parent = self.TrStructure.invisibleRootItem() if type(item) == SequencerTreeItem else item.parent()
    #     for i in range(parent.childCount()):
    #         if parent.child(i) == item:
    #             return i

    def AddStep(self):
        current = self.TrStructure.currentItem()
        if isinstance(current, SequencerTreeItem):
            seq_name = current.text(0)
            name = self.TxtStepName.text()
            brightnesses = list()
            for led in Mediator.leds_list:
                if self.step_channels_dict[led].isEnabled() and self.step_channels_dict[led].currentIndex() != 0:
                    brightnesses.append(self.step_channels_dict[led].currentText())
                elif self.step_brightness_dict[led].isEnabled():
                    brightnesses.append(self.step_brightness_dict[led].value())
            wait = self.SpinWait.value()
            smooth = self.SpinSmooth.value()
            step, error = self.auxdata.create_step(seq_name, name, brightnesses, smooth, wait)
            if error:
                self.ErrorMessage(error)
            else:
                step_item = StepTreeItem(str(step))
                current.addChild(step_item)
                self.saved[0] = False
                self.ChangeTabTitle(auxleds, self.tabWidget.currentIndex())
        #self.GetStepsNames()

    def AddRepeatStep(self):
        current = self.TrStructure.currentItem()
        effect = current.parent().text(0)
        number = self.GetItemId(current)
        startstep = self.ComboRepeat.currentText()
        count = self.ComboCount.currentText()
        self.auxdata.CreateRepeatStep(effect, number, startstep, count)
        step_text = Mediator.get_repeat_name(startstep, count)
        step_item = StepTreeItem(step_text)
        current.addChild(step_item)
        self.saved[0] = False
        self.ChangeTabTitle(auxleds, self.tabWidget.currentIndex())

    def DeleteItem(self):
        current = self.TrStructure.currentItem()
        current_name = current.text(0)
        if current.childCount() > 0:
            reply = QMessageBox.question(self, 'Message', "This sequencer has steps, do you really want to delete it?",
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.No:
                return
        self.saved[0] = False
        self.ChangeTabTitle(auxleds, self.tabWidget.currentIndex())
        if isinstance(current, SequencerTreeItem):
            parent = self.TrStructure.invisibleRootItem()
            parent.removeChild(current)
            self.auxdata.delete_sequence(current_name)
            #delete seq from copy sequncer block and aux block in profile tab
            self.CBSeqList.clear()
            self.CBAuxList.clear()
            for sequencer in self.auxdata.Sequencers:
                self.CBSeqList.addItem(sequencer.Name)
                self.CBAuxList.addItem(sequencer.Name)
            if self.CBSeqList.count() == 0:
                self.BtnCopySeq.setEnabled(False)
            #to do : delete child steps
        if isinstance(current, StepTreeItem):
            parent = current.parent()
            grandpa = parent.parent()
            seq_number = self.GetItemId(parent)
            effect = grandpa.text(0)
            step_number = self.GetItemId(current)
            used_steps = self.auxdata.GetRepeatList(effect, seq_number)
            step_name = Mediator.get_currrent_step_name(current_name)
            if step_name in used_steps:
                self.ErrorMessage("This step is used in repeat step, first delete repeat step")
                self.saved[0] = True
                self.ChangeTabTitle(self.auxfilename, self.saved, auxleds, self.tabWidget.currentIndex())
            else:
                self.auxdata.DeleteItem(step_number, [effect, seq_number, Mediator.seq_key])
                parent.removeChild(current)

    #def CheckAllLeds(self):
    #    state = self.CBLedsAll.isChecked()
    #    for led in self.leds_combo_list:
    #        if led.isEnabled():
    #            led.setChecked(state)

    def SavePressed(self):
        self.Save(False)

    def Save(self, save_as: bool):
        index = self.tabWidget.currentIndex()
        if save_as or not self.filename[index]:
            new_filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "")[0]
            if new_filename:
                self.filename[index] = new_filename
            else:
                return
        self.savefunctions[index](self.filename[index])
        self.saved[index] = True
        self.ChangeTabTitle(tabnames[index], self.tabWidget.currentIndex())
        if index == 1:
            self.BtnSave.setEnabled(False)

    def SaveAsPressed(self):
        self.Save(True)

    def OpenPressed(self):
        openfilename = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "")[0]
        if openfilename:
            openfile = open(openfilename)
            text = openfile.read()
            index = self.tabWidget.currentIndex()
            gui_data, error, warning = self.openfunctions[index](text)
            if error:
                self.ErrorMessage("Could not load file % s: % s" % (openfilename, error))
            else:
                if not self.saved[index]:
                    save_msg = "You have unsaved profile. Do you want to save?"
                    reply = QMessageBox.question(self, 'Message', save_msg, QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.SavePressed()
                if warning:
                    self.statusfields[index].setText("Try to open %s...\n %s" % (openfilename, warning))
                else:
                    self.statusfields[index].setText("%s successfully loaded" % openfilename)
                if index == 0:
                    self.auxdata = AuxEffects()
                    self.LoadDataToTree(gui_data)
                if index == 1:
                    self.LoadCommonData(gui_data)
                    self.BtnSave.setEnabled(False)
                if index == 2:
                    self.profiledata.data = gui_data
                    self.LoadProfileList()
                self.filename[index] = openfilename
                self.saved[index] = True
                self.ChangeTabTitle(tabnames[index], self.tabWidget.currentIndex())

    def LoadDataToTree(self, data):
        self.TrStructure.clear()
        self.LstEffects.clear()
        self.CBAuxList.clear()
        for effect in data.keys():
            item = EffectTreeItem(effect)
            self.TrStructure.addTopLevelItem(item)
            self.LstEffects.addItem(effect)
            self.auxdata.AddEffect(effect)
            self.CBAuxList.addItem(effect)
            i = 0
            for config in data[effect].keys():
                config_item = SequencerTreeItem(config)
                item.addChild(config_item)
                self.auxdata.CreateSequencer(effect, Mediator.get_leds_from_config(config))
                for step in data[effect][config]:
                    step_item = StepTreeItem(step)
                    config_item.addChild(step_item)
                    if Mediator.repeat_key in step:
                        start, count = Mediator.get_param_from_repeat(step)
                        self.auxdata.CreateRepeatStep(effect, i, start, count)
                    else:
                        name, brightness, wait, smooth = Mediator.get_param_from_name(step)
                        self.auxdata.CreateStep(effect, i, name, brightness, wait, smooth)
                i += 1

    def ErrorMessage(self, text):
        error = QMessageBox()
        error.setIcon(QMessageBox.Critical)
        error.setText(text)
        error.setWindowTitle("Error")
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()

    def ChangeTabTitle(self, filetype, index):
        if self.filename[index]:
            text = "%s - %s" % (filetype, self.filename[index].split(r'/')[-1])
        else:
            text = filetype
        if not self.saved[index]:
            text += "*"
        self.tabWidget.setTabText(index,
                                  QtCore.QCoreApplication.translate("MainWindow", text))

    def closeEvent(self, event):
        for i in range(3):
            if not self.saved[i]:
                quit_msg = "You have unsaved %s file. Do you want to save?" % tabnames[i]
                reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.SavePressed()
        event.accept()

    def CBClicked(self):
        CB = self.sender()
        if CB in self.common_dict.keys():
            key_list = self.common_dict[CB]
        else:
            key_list = self.motion_dict[CB]
        if CB.isChecked():
            self.commondata.update_value(key_list, 1)
        else:
            self.commondata.update_value(key_list, 0)
        if self.saved[1]:
            self.saved[1] = False
            self.ChangeTabTitle(common, self.tabWidget.currentIndex())
        self.BtnSave.setEnabled(True)
        self.BtnDefault.setEnabled(True)

    def SpinChanged(self):
        Spin = self.sender()
        blade = self.CBBlade.currentIndex()
        if Spin in self.common_dict.keys():
            key_list = Mediator.change_keylist(self.common_dict[Spin])
        else:
            key_list = self.motion_dict[Spin]
        self.commondata.update_value(key_list, Spin.value())
        if self.saved[1] == True:
            self.saved[1] = False
            self.ChangeTabTitle(common, 1)
        self.BtnSave.setEnabled(True)
        self.BtnDefault.setEnabled(True)

    def SetDefaultCommon(self):
        for key in self.common_dict.keys():
            value = self.commondata.get_default_value(Mediator.change_keylist(self.common_dict[key]))
            if key == self.CBBlade2Enabled:
                key.setChecked(value)
            else:
                key.setValue(value)
        for key in self.motion_dict.keys():
            value = self.commondata.get_default_value(Mediator.change_keylist(self.motion_dict[key]))
            if key in [self.CBStabEnabled, self.CBScrewEnabled, self.CBSpinEnabled]:
                key.setChecked(value)
            else:
                key.setValue(value)

    def LoadCommonData(self, data):
        try:
            for key in self.common_dict.keys():
                path = Mediator.change_keylist(self.common_dict[key])
                value = data
                for path_key in path:
                    value = value[path_key]
                if key == self.CBBlade2Enabled:
                    key.setChecked(value)
                else:
                    key.setValue(value)
            for key in self.motion_dict.keys():
                path = Mediator.change_keylist(self.motion_dict[key])
                value = data
                for path_key in path:
                    value = value[path_key]
                if key in [self.CBStabEnabled, self.CBScrewEnabled, self.CBSpinEnabled]:
                    key.setChecked(value)
                else:
                    key.setValue(value)
            self.CBBlade2Enabled.setChecked(data[Mediator.blade2_key[0]]['Enabled'])
        except Exception:
            e = sys.exc_info()[1]
            self.ErrorMessage(e.args[0])

    def Blade2Clicked(self):
        """
        writes 0 or 1 to corresponding data field
        :return:
        """
        if self.CBBlade2Enabled.isChecked():
            self.commondata.update_value(Mediator.blade2_enabled_keys, 1)
            self.SpinPixPerBand2.setEnabled(True)
            self.SpinBandNumber.setEnabled(True)
        else:
            self.commondata.update_value(Mediator.blade2_enabled_keys, 0)
            self.SpinPixPerBand2.setEnabled(False)
            self.SpinBandNumber.setEnabled(False)
        self.saved[1] = False
        self.ChangeTabTitle(common, 1)


    def GetAuxEffectsList(self):
        """
        gets aux effects list from aux data (first tab)
        :return:
        """
        effects = self.data.get_effects_list()
        for effect in effects:
            self.CBAuxList.addItem(effect)

    def EffectTabChanged(self):
        """
        changes group and button label for auxleds group when tab changes
        :return:
        """
        current = self.TabEffects.currentIndex()
        text = self.TabEffects.tabText(current)
        self.GBAuxLeds.setTitle("Select AuxLeds Effects for %s Effect" % text)
        self.BtnCReateAux.setText("Add effect to %s" % text)
        # load data or current tab if profile is selected
        if self.BtnCReateAux.isEnabled():
            profile = self.LstProfile.currentItem().text()
            auxeffects = self.profiledata.get_aux_effects(text, profile)
            self.LstAuxProfile.clear()
            for aux in auxeffects:
                self.LstAuxProfile.addItem(aux)

    def MinChanged(self, min_control):
        """
        when min data changes corresponding max border changes too
        :param min_control: control that changes
        :return:
        """
        max_control = self.min_max_dict[min_control]
        max_control.setMinimum(min_control.value())

    def MaxChanged(self, max_control):
        """
        when max data changes corresponding min border changes too
        :param max_control: control that changes
        :return:
        """
        min_control = self.max_min_dict[max_control]
        min_control.setMaximum(max_control.value())

    def ProfileNameChanged(self, name):
        """
        if text in profile field changed and this name is not used yet and it is valid make add profile button enabled
        :param name:
        :return:
        """
        effects = self.profiledata.get_profiles_list()
        valid = [ch.isalpha() or ch.isdigit() or ch == '_' for ch in name]
        enabled = True if name and name not in effects and all(valid) else False
        self.BtnProfile.setEnabled(enabled)

    def AddProfile(self):
        """
        adds new profile with current name to Profile List and profile data
        :return:
        """
        name = self.TxtAddProfile.text()
        self.profiledata.add_profile(name)
        self.BtnProfile.setEnabled(False)
        self.LstProfile.addItem(name)
        # data is unsaved now
        self.saved[2] = False
        self.ChangeTabTitle(profiletab, self.tabWidget.currentIndex())

    def ProfileCBClicked(self):
        """
        any check box in profile controls clicked. we get key path for it and save to data to current profile
        (checked = 1, otherwise 0)
        :return:
        """
        CB = self.sender()
        key_list = self.profile_dict[CB]
        profile = self.LstProfile.currentItem().text()
        if CB.isChecked():
            self.profiledata.update_value(key_list, profile, 1)
        else:
            self.profiledata.update_value(key_list, profile, 0)
        # data now is unsaved
        if self.saved[2]:
            self.saved[2] = False
            self.ChangeTabTitle(profiletab, self.tabWidget.currentIndex())

    def LoadProfileControls(self, profile):
        """
        enables all neeeded controls for selected profile
        load data for selected profile to profile controls (Main Blade section)
        :param profile:
        :return:
        """
        # enable all control for all tabs
        for key in self.control_tab_dict.keys():
            for control in self.control_tab_dict[key]:
                control.setEnabled(True)
        for key in self.color_dict.keys():
            key.setEnabled(True)
        self.BtnAddColor.setEnabled(True)
        self.CBBlade.setEnabled(True)
        #aux block enable
        self.TxtCreateAux.setEnabled(True)
        self.BtnCReateAux.setEnabled(True)
        self.CBAuxList.setEnabled(True)

        # loads data for main blade
        for control in self.profile_dict.keys():
            value = self.profiledata.get_value(self.profile_dict[control], profile)
            # Combo Box
            if control in self.CB_list:
                control.setChecked(value)
            else:
                # color text
                if control in self.color_list:
                    text = Mediator.color_data_to_str(value)
                    control.setText(text)
                else:
                    # spin box
                    control.setValue(value)

        # controls under Blade selection loaded
        value = self.profiledata.get_value(Mediator.indicate_path, profile)
        self.CBIndicate.setChecked(value)
        value = self.profiledata.get_value(Mediator.delay_path, profile)
        self.SpinDelayBeforeOn.setValue(value)

        # flaming colors lis loaded
        self.LstFlamingColor.clear()
        flaming_colors = self.profiledata.get_colors(Mediator.flaming_color_path, self.LstProfile.currentItem().text())
        for color in flaming_colors:
            item = Mediator.color_data_to_str(color)
            self.LstFlamingColor.addItem(item)

        #auxleds section
        index = self.TabEffects.currentIndex()
        effect = self.TabEffects.tabText(index)
        auxeffects = self.profiledata.get_aux_effects(effect, profile)
        self.LstAuxProfile.clear()
        for aux in auxeffects:
            self.LstAuxProfile.addItem(aux)

        # you may delete profile now
        self.BtnDeleteProfile.setEnabled(True)

    def ProfileClicked(self, item):
        """
        profile item in Profile List clicked. All neseccary data loaded, controls enabled
        :param item:
        :return:
        """
        profile = item.text()
        self.CBBlade.setCurrentIndex(0)
        self.LoadProfileControls(profile)

    def DeleteProfile(self):
        """
        delete profile from data and UI with question, disables delete button, loads default data to all controls
        :return:
        """
        name = self.LstProfile.currentItem().text()
        # warning message
        reply = QMessageBox.question(self, 'Message', "Do you realy want to delete this profile?",
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.profiledata.delete_profile(name)
            self.LstProfile.clear()
            for profile in self.profiledata.get_profiles_list():
                self.LstProfile.addItem(profile)
            self.BtnDeleteProfile.setEnabled(False)

            #disable all profile controls
            for key in self.control_tab_dict.keys():
                for control in self.control_tab_dict[key]:
                    control.setEnabled(False)
            for key in self.color_dict.keys():
                key.setEnabled(False)
            self.BtnAddColor.setEnabled(False)
            self.CBBlade.setEnabled(False)
            self.SpinDelayBeforeOn.setEnabled(False)
            self.CBIndicate.setEnabled(False)
            # and auxleds group
            self.BtnAuxDelete.setEnabled(False)
            self.BtnCReateAux.setEnabled(False)
            self.CBAuxList.setEnabled(False)
            self.TxtCreateAux.setEnabled(False)

            #load default data
            for key in self.profile_dict.keys():
                value = self.profiledata.get_default(self.profile_dict[key])
                if key in self.CB_list:
                    key.setChecked(value)
                else:
                    if key in self.color_list:
                        text = Mediator.color_data_to_str(value)
                        key.setText(text)
                    else:
                        key.setValue(value)
            self.LstFlamingColor.clear()
            value = self.profiledata.get_default(Mediator.indicate_path)
            self.CBIndicate.setChecked(value)
            value = self.profiledata.get_default(Mediator.delay_path)
            self.SpinDelayBeforeOn.setValue(value)
            self.TxtAddProfile.clear()
            #file is unsaved now
            self.saved[2] = False
            self.ChangeTabTitle(profiletab, self.tabWidget.currentIndex())

    def ProfileSpinChanged(self):
        """
        saves new value of any profile spin control to corresponding data using path of keys, changes min/max controls
        borders if nesessary
        :return:
        """
        spin = self.sender()
        if spin.isEnabled():
            blade = self.CBBlade.currentIndex()
            key_list = self.profile_dict[spin]
            # for second blade Blade2 key added to key path
            if blade == 1:
                key_list = Mediator.blade2_key + key_list
            text = self.LstProfile.currentItem().text()
            self.profiledata.update_value(key_list, text, spin.value())
            # data may be unsaved now
            if self.saved[2]:
                self.saved[2] = False
                self.ChangeTabTitle(profiletab, self.tabWidget.currentIndex())
            # update min and max controls
            if spin in self.min_max_dict.keys():
                self.MinChanged(spin)
            if spin in self.max_min_dict.keys():
                self.MaxChanged(spin)

    def ProfileTextChanged(self):
        """
        saves data if text changed
        :return:
        """
        text = self.sender()
        # not save id control is disabled (may occur when we load default settings if no profile is selected
        if text.isEnabled():
            label = text.text()
            label = Mediator.str_to_color_data(label)
            if label:
                key_list = self.profile_dict[text]
                # add blade2 key to path for second blade
                blade = self.CBBlade.currentIndex()
                if blade == 1:
                    key_list = Mediator.blade2_key + key_list
                profile = self.LstProfile.currentItem().text()
                self.profiledata.update_value(key_list, profile, label)
                #profile is not saved now
                if self.saved[2]:
                    self.saved[2] = False
                    self.ChangeTabTitle(profiletab, self.tabWidget.currentIndex())

    def ColorChanged(self):
        """
        adds new color selected with color dialog to control
        :return:
        """
        color_button = self.sender()
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            rgb = [color.red(), color.green(), color.blue()]
            color_text = Mediator.color_data_to_str(rgb)
            color_input = self.color_dict[color_button]
            color_input.setText(color_text)

    def AddColor(self):
        """
        adds color to flaming color list and saves color data to profile
        :return:
        """
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            rgb = [color.red(), color.green(), color.blue()]
            color_text = Mediator.color_data_to_str(rgb)
            self.LstFlamingColor.addItem(color_text)
            # save to profile adding Blade2 key if Blade2 selected
            profile = self.LstProfile.currentItem().text()
            path = Mediator.flaming_color_path
            index = self.CBBlade.currentIndex()
            if index == 1:
                path = Mediator.blade2_key + path
            self.profiledata.save_color(path, rgb, profile)
        #profile is unsaved now
        self.saved[2] = False
        self.ChangeTabTitle(profiletab, self.tabWidget.currentIndex())

    def ColorClicked(self):
        """
        if any color selected we may delete it
        :return:
        """
        self.BtnDeleteColor.setEnabled(True)

    def DeleteColor(self):
        current_color = self.LstFlamingColor.currentItem().text()
        current_color = Mediator.str_to_color_data(current_color)
        path = Mediator.flaming_color_path
        index = self.CBBlade.currentIndex()
        if index == 1:
            path = Mediator.blade2_key + path
        self.profiledata.delete_color(path, current_color, self.LstProfile.currentItem().text())
        self.LstFlamingColor.clear()
        flaming_colors = self.profiledata.get_colors(path, self.LstProfile.currentItem().text())
        for color in flaming_colors:
            item = Mediator.color_data_to_str(color)
            self.LstFlamingColor.addItem(item)
        self.saved[2] = False
        self.ChangeTabTitle(profiletab, self.tabWidget.currentIndex())

    def BladeChanged(self, index):
        """
        enable necessary controls for selected blade and disable unnecessary and loads data
        :param index: index of blade
        :return:
        """
        profile = self.LstProfile.currentItem().text()
        if index == 0:
            # main blade
            # all tabs enabled
            self.TabPowerOn.setEnabled(True)
            self.TabPowerOff.setEnabled(True)
            self.TabClash.setEnabled(True)
            self.TabStab.setEnabled(True)
            self.TabLockup.setEnabled(True)
            self.TabBlaster.setEnabled(True)
            # enables and loads all tab controls for main blade
            self.LoadProfileControls(profile)
            # disable extra blade2 comboboxes
            self.CBFlickeringAlwaysOn.setEnabled(False)
            self.CBFlamingAlwaysOn.setEnabled(False)
            # disables controls for blade2
            self.CBIndicate.setEnabled(False)
            self.SpinDelayBeforeOn.setEnabled(False)
        else:
            # blade2
            # disables unused tabs
            self.TabPowerOn.setEnabled(False)
            self.TabPowerOff.setEnabled(False)
            self.TabClash.setEnabled(False)
            self.TabStab.setEnabled(False)
            self.TabLockup.setEnabled(False)
            self.TabBlaster.setEnabled(False)
            # enables special Blade2 Comboboxes
            self.CBFlamingAlwaysOn.setEnabled(True)
            self.CBFlickeringAlwaysOn.setEnabled(True)
            # enables blade2 settings
            self.CBIndicate.setEnabled(True)
            self.SpinDelayBeforeOn.setEnabled(True)
            # disables AuxEffects section
            self.BtnCReateAux.setEnabled(False)
            self.TxtCreateAux.setEnabled(False)
            self.CBAuxList.setEnabled(False)
            self.BtnAuxDelete.setEnabled(False)
            self.LstAuxProfile.clear()
            # disable unused comboboxes
            self.CBFlaming.setEnabled(False)
            self.CBFlickering.setEnabled(False)
            # load data for blade2
            self.LoadBlade2Controls()

    def LoadBlade2Controls(self):
        """
        loads data for blade2 for selected profile
        :return:
        """
        # all paths must start with Mediator.blade2_keys.
        # Done automatically for self.extra_blade_CB and self.spinDelayBeforeOn
        profile = self.LstProfile.currentItem().text()
        # flickering and flaming tabs
        controls = self.flickering + self.flaming
        for spin in controls:
            path = self.profile_dict[spin]
            path = Mediator.blade2_key + path
            value = self.profiledata.get_value(path, profile)
            spin.setValue(value)
        # color for working mode
        path = self.profile_dict[self.TxtWorkingColor]
        color = self.profiledata.get_value(Mediator.blade2_key + path, profile)
        text = Mediator.color_data_to_str(color)
        self.TxtWorkingColor.setText(text)
        # extrs Blade2 comboboxes
        for CB in self.extra_blade_CB_dict.keys():
            value = self.profiledata.get_value(self.extra_blade_CB_dict[CB], profile)
            CB.setChecked(value)
        # dalay before blade2
        delay = self.profiledata.get_value(Mediator.delay_path, profile)
        self.SpinDelayBeforeOn.setValue(delay)
        # flaming colors fpr blade2
        self.LstFlamingColor.clear()
        flaming_colors = self.profiledata.get_colors(Mediator.blade2_key + Mediator.flaming_color_path, self.LstProfile.currentItem().text())
        for color in flaming_colors:
            item = Mediator.color_data_to_str(color)
            self.LstFlamingColor.addItem(item)

    def ExtraBladeCBlicked(self):
        """
        handlers for extra comboboxes for blade2, saves to profile data
        :return:
        """
        CB = self.sender()
        path = self.extra_blade_CB_dict[CB]
        profile = self.LstProfile.currentItem().text()
        if CB.isChecked():
            value = 1
        else:
            value = 0
        #data is unsaved now
        self.profiledata.update_value(path, profile, value)
        self.saved[2] = False

    def DelayChanged(self):
        """
        dalay before handler, saves to profile data
        :return:
        """
        if self.SpinDelayBeforeOn.isEnabled():
            path = Mediator.delay_path
            value = self.SpinDelayBeforeOn.value()
            profile = self.LstProfile.currentItem().text()
            self.profiledata.update_value(path, profile, value)

    def ProfileAddAux(self):
        """
        adds aux effect from test field if it is correcty filled or from auxlist
        :return:
        """
        current = self.TabEffects.currentIndex()
        effect = self.TabEffects.tabText(current)
        profile = self.LstProfile.currentItem().text()
        auxeffect = self.TxtCreateAux.text()
        valid = [ch.isalpha() or ch.isdigit() or ch == '_' for ch in auxeffect]
        existing = self.profiledata.get_aux_effects(effect, profile)
        if auxeffect != "" and all(valid) and auxeffect not in existing:
            self.LstAuxProfile.addItem(auxeffect)
            self.TxtCreateAux.clear()
            self.profiledata.save_aux(auxeffect, effect, profile)
        else:
            auxeffect = self.CBAuxList.currentText()
            if auxeffect and auxeffect not in existing:
                self.LstAuxProfile.addItem(auxeffect)
                self.profiledata.save_aux(auxeffect, effect, profile)

    def AuxClicked(self):
        """
        button Delete AuxEffect activated
        :return:
        """
        self.BtnAuxDelete.setEnabled(True)

    def DeleteAux(self):
        """
        delete selected aux from UI and profile data for tos effect. AuxSetion is cleared if it was last effect
        :return:
        """
        current = self.LstAuxProfile.currentItem().text()
        current_tab = self.TabEffects.currentIndex()
        effect = self.TabEffects.tabText(current_tab)
        profile = self.LstProfile.currentItem().text()
        self.profiledata.delete_aux(current, effect, profile)
        auxeffects = self.profiledata.get_aux_effects(effect, profile)
        self.LstAuxProfile.clear()
        for aux in auxeffects:
            self.LstAuxProfile.addItem(aux)
        self.BtnAuxDelete.setEnabled(False)

    def LoadProfileList(self):
        """
        loads from data all profiles to list
        :return:
        """
        self.LstProfile.clear()
        for profile in self.profiledata.get_profiles_list():
            self.LstProfile.addItem(profile)
        self.BtnDeleteProfile.setEnabled(False)

        # disable all profile controls
        for key in self.control_tab_dict.keys():
            for control in self.control_tab_dict[key]:
                control.setEnabled(False)
        for key in self.color_dict.keys():
            key.setEnabled(False)
        self.BtnAddColor.setEnabled(False)
        self.CBBlade.setEnabled(False)
        self.SpinDelayBeforeOn.setEnabled(False)
        self.CBIndicate.setEnabled(False)
        # and auxleds group
        self.BtnAuxDelete.setEnabled(False)
        self.BtnCReateAux.setEnabled(False)
        self.CBAuxList.setEnabled(False)
        self.TxtCreateAux.setEnabled(False)

        # load default data
        for key in self.profile_dict.keys():
            value = self.profiledata.get_default(self.profile_dict[key])
            if key in self.CB_list:
                key.setChecked(value)
            else:
                if key in self.color_list:
                    text = Mediator.color_data_to_str(value)
                    key.setText(text)
                else:
                    key.setValue(value)
        self.LstFlamingColor.clear()
        value = self.profiledata.get_default(Mediator.indicate_path)
        self.CBIndicate.setChecked(value)
        value = self.profiledata.get_default(Mediator.delay_path)
        self.SpinDelayBeforeOn.setValue(value)
        self.TxtAddProfile.clear()


@logger.catch
def main():
    initiate_exception_logging()
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ProfileEditor()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
