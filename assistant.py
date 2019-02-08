from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets, QtCore
import os
from typing import Optional
from help import Ui_Help
from profileshelp import  Ui_Help as Profile_Help
from auxhelp import Ui_Help as Aux_Help


about_text = """Settings Editor 1.1 for lightsabers.
By Warsabers.ru"""

class CommonHelp(QtWidgets.QDialog, Ui_Help):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

class ProfileHelp(QtWidgets.QDialog, Profile_Help):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

class AuxHelp(QtWidgets.QDialog, Aux_Help):

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
    help_window = AuxHelp()
    help_window.exec()


def profile_help():
    """
    show help window with text for common
    :return:
    """
    # editor_help(profile_helptext)

    help_window = ProfileHelp()
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
    help.setWindowTitle()
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