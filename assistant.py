from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
import os
from typing import Optional
from help import Ui_Help

auxhelptext = (
    'On tab AuxLEDs you may configure behaviour for auxiliary LEDS (AuxLEDs) (see https://warsabers.ru/downloads/ '
    'for guide. Setup consists of two stages:\n'
    '1. Making groups of AUX leds; \n'
    '2. Making sequences for that groups.\n'
    'After creating Sequencers you may select them for effects on Profiles tab.\n'
    '\n'
    'Fill «LED group name» and check nesessary AUXLEDS  in  «LEDs  in the group» part.  LEDS used in other  groups are'
    ' always  checked  and unavailable. Add new group with «Add Group» button. Once LED  group is selected you may '
    'delete it or add a Sequencer. You are not allowed to create groups with the same names or without LEDs and delete'
    ' groups used in Sequencers.\n'
    '\n'
    'To create Sequencer select LED Group and fill «Sequencer name». You may create new sequencer with «Add  Sequencer»'
    ' button or copy steps of existing with «Copy Sequencer» button (only if there is at least one sequencer to copy, '
    'you need to select sequencer for copying in dropdown). \n'
    '\n'
    'Once Sequencer is created select it for adding steps or delete it (with all its steps). After Sequencer selecting '
    'controls of Step group are available(Name (filled with Step_nvalue), Wait, Smooth and LEDs  available for this '
    'Sequencer (depends on its Group).  For each LED you may select Brightness or channel of main blade to copy. If '
    'channel is selected, Brightness  is ignored. When all values are filled correctly add step with «Add Step» button.\n'
    '\n'
    'Repeat section becomes available if any step with name is created for this sequencer. Select step to start and '
    'count. If Forever is checked, Count value is ignored. \n'
    '\n'
    'If you select step or repeat in Sequencer List, values of this step are loaded and you may edit them with «Edit '
    'Step/Repeat» button or add a new step after selected using «Add Step/Repeat» button. Also ypu may delete step(not'
    ' used in repeat steps). \n'
    '\n'
    'You may add unlimited number of Sequencers and Steps for them and you may create different Sequencers for the same'
    ' Group to use in different effects. If you want  to use config file on lightsaber save it as «Auxleds.ini».  \n')

common_helptext = """On Common tab you may change values  of common settings 
(see guide at https://warsabers.ru/downloads/) for each setting 
meaning.  You may reset values to defaults using «Reset 
to default»  button. To use resulted config on lightsaber
save it as Common.ini"""

profile_helptext = """
On Profiles tab you may create and edit profiles. To add new profile fill «Profile name» and click «Add Profile» button. Select profile in «Profile list» to edit it settings. See quide at https://warsabers.ru/downloads/ to each setting  meaning. 

After selecting profile tab widget with effects or lightsaber  work mode settings  becomes available. Select appropriate tab to edit each effect/mode settings. You may also add  AUXLEDs effect to each effect/mode using AUXLEDs controls group.

You may select existing AUXLEDs sequencer from AUXLEDs tab in dropdown or type AUXLEDs effect name in field for custom name and create it later. If custom name is filled dropdown is ignored. 

Change Blade1 to Blade2 in Current Blade dropdown to edit Blade2 settings. Only actual settings for current Blade remain available when you change Blade.

You may create unlimited number of profiles or edit existing (open file using «Open» menu item). Save file as «Profiles.ini» before placing it at lightsaber microSD. 
"""

about_text = """Setting Editor 0.9
Warsabers.ru"""

class CommonHelp(QtWidgets.QDialog, Ui_Help):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

def about_help():
    """
    shows help window with about text
    :return:
    """
    editor_help(about_text)


def common_help():
    """
    show help window with text for common
    :return:
    """
    help_window = CommonHelp()
    help_window.exec()


def auxleds_help():
    """
    show help window with text for auxleds
    :return:
    """
    # editor_help(auxhelptext)
    help_window = CommonHelp()
    help_window.setWindowTitle("AuxLEDS Settings Help")
    help_window.TxtHelp.setText(auxhelptext)
    help_window.exec()


def profile_help():
    """
    show help window with text for common
    :return:
    """
    # editor_help(profile_helptext)

    help_window = CommonHelp()
    help_window.setWindowTitle("Profiles Settings Help")
    help_window.TxtHelp.setText(profile_helptext)
    help_window.exec()


def editor_help(text):
    """
    functions for showing help window
    :param text:
    :return:
    """
    help = QMessageBox()
    help.setIcon(QMessageBox.Information)
    help.setText(text)
    help.setWindowTitle("Auxleds Editor Help")
    help.setStandardButtons(QMessageBox.Ok)
    help.exec_()


def find_file(filename: str, path: str = ".") -> Optional[str]:
    """
    case insensitive search for file in current directory
    :param filename: filename
    :param path: directory for search
    :return: real filename
    """
    for file in os.listdir(path):
        if filename.lower() == file.lower():
            return file
    return None