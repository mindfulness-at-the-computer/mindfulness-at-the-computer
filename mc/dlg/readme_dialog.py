import logging

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import mc.mc_global


class ReadmeDialog(QtWidgets.QDialog):
    def __init__(self, i_parent):
        super(ReadmeDialog, self).__init__(i_parent)

        self.setWindowTitle("Please take care of yourself")
        self.setWindowIcon(QtGui.QIcon(mc.mc_global.APPLICATION_ICON_PATH_STR))
        self.setFixedWidth(500)
        self.setFixedHeight(600)

        vbox_l2 = QtWidgets.QVBoxLayout(self)

        read_me_text_qte = QtWidgets.QTextEdit()
        vbox_l2.addWidget(read_me_text_qte)
        read_me_text_qte.setReadOnly(True)

        contents_str = ""
        with open(mc.mc_global.README_FILE_PATH_STR, "r") as readme_file:
            contents_str = readme_file.read()
        read_me_text_qte.setText(contents_str)

    @staticmethod
    def show_dialog(i_parent):
        rest_reminder_dialog = ReadmeDialog(i_parent)
        rest_reminder_dialog.show()  # -modeless

