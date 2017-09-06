import logging
import sys
import functools
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class RestReminderDialog(QtWidgets.QDialog):
    def __init__(self, i_parent):
        super(RestReminderDialog, self).__init__(i_parent)
        self.setWindowTitle("Please take care of yourself")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        vbox = QtWidgets.QVBoxLayout(self)
        # -please note: If we don't send "self" to the QVBoxLayout we won't see the main window
        #  in the background of the dialog. Also we don't need to use self.setLayout(vbox)

        rest_kindness_alternatives_qbb = QtWidgets.QDialogButtonBox()
        vbox.addWidget(rest_kindness_alternatives_qbb)

        rest_kindness_alternatives_qbb.setOrientation(QtCore.Qt.Vertical)

        movement_qpb = QtWidgets.QPushButton("Movement exercise")
        rest_kindness_alternatives_qbb.addButton(movement_qpb, QtWidgets.QDialogButtonBox.YesRole)
        walk_qpb = QtWidgets.QPushButton("Taking a walk")
        rest_kindness_alternatives_qbb.addButton(walk_qpb, QtWidgets.QDialogButtonBox.YesRole)

        wait_qpb = QtWidgets.QPushButton("Wait (snooze) for 5 minutes")
        rest_kindness_alternatives_qbb.addButton(wait_qpb, QtWidgets.QDialogButtonBox.NoRole)

        close_qpb = QtWidgets.QPushButton("Close")
        rest_kindness_alternatives_qbb.addButton(close_qpb, QtWidgets.QDialogButtonBox.NoRole)
        close_qpb.clicked.connect(self.on_close_button_clicked)

        # Roles: http://doc.qt.io/qt-5/qdialogbuttonbox.html#ButtonRole-enum

        """
        tension in body, releasing tension, mindful movements
        mindfulness of walking
        making tea, drinking tea

        **if skipping break: arms over head**
        stretching arms
        """

        # TODO: Idea: For each action have a small image that the user can set

    def on_close_button_clicked(self):
        ##self.parent().show()
        self.accept()

    @staticmethod
    def show_dialog(i_parent):
        i_parent.show()
        # -PLEASE NOTE: We have to make sure the window is visible if using a modal dialog,
        #  otherwise when the dialog is closed the whole application will close as well
        #  (unknown why)
        rest_reminder_dialog = RestReminderDialog(i_parent)
        rest_reminder_dialog.exec()

