import logging
import sys
import functools
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import mb_global
import mb_model


class RestReminderDialog(QtWidgets.QDialog):
    def __init__(self, i_parent):
        super(RestReminderDialog, self).__init__(i_parent)
        self.setWindowTitle("Please take care of yourself")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        hbox_l1 = QtWidgets.QHBoxLayout(self)
        # -please note: If we don't send "self" to the QVBoxLayout we won't see the main window
        #  in the background of the dialog. Also we don't need to use self.setLayout(vbox)
        vbox_l2 = QtWidgets.QVBoxLayout()
        hbox_l1.addLayout(vbox_l2)

        rest_kindness_alternatives_qbb = QtWidgets.QDialogButtonBox()
        vbox_l2.addWidget(rest_kindness_alternatives_qbb)

        rest_kindness_alternatives_qbb.setOrientation(QtCore.Qt.Vertical)

        movement_qpb = QtWidgets.QPushButton("Movement exercise")
        rest_kindness_alternatives_qbb.addButton(movement_qpb, QtWidgets.QDialogButtonBox.YesRole)
        walk_qpb = QtWidgets.QPushButton("Taking a walk")
        rest_kindness_alternatives_qbb.addButton(walk_qpb, QtWidgets.QDialogButtonBox.YesRole)

        self.rest_actions_qgb = QtWidgets.QGroupBox("Rest actions")
        vbox_l2.addWidget(self.rest_actions_qgb)
        self.ra_vbox = QtWidgets.QVBoxLayout()
        self.rest_actions_qgb.setLayout(self.ra_vbox)
        self.rest_actions_qbg = QtWidgets.QButtonGroup()
        button_one = QtWidgets.QPushButton("one")
        button_two = QtWidgets.QPushButton("two")
        button_one.setCheckable(True)
        button_two.setCheckable(True)
        self.rest_actions_qbg.addButton(button_one)
        self.rest_actions_qbg.addButton(button_two)
        self.ra_vbox.addWidget(button_one)
        self.ra_vbox.addWidget(button_two)

        self.populate_list_of_buttons()


        wait_qpb = QtWidgets.QPushButton("Wait (snooze) for 5 minutes")
        rest_kindness_alternatives_qbb.addButton(wait_qpb, QtWidgets.QDialogButtonBox.NoRole)

        close_qpb = QtWidgets.QPushButton("Close")
        rest_kindness_alternatives_qbb.addButton(close_qpb, QtWidgets.QDialogButtonBox.NoRole)
        close_qpb.clicked.connect(self.on_close_button_clicked)

        # Roles: http://doc.qt.io/qt-5/qdialogbuttonbox.html#ButtonRole-enum


        self.image_qll = QtWidgets.QLabel()
        self.image_qll.setScaledContents(True)
        self.image_qll.setPixmap(
            QtGui.QPixmap(mb_global.active_rest_image_full_path_str)
        )
        hbox_l1.addWidget(self.image_qll)


        """
        One or more push buttons can be selected at once? This would be toggle buttons,
        or alternatively a list could be used with multiple selection enabled
        """

        """
        tension in body, releasing tension, mindful movements
        mindfulness of walking
        mindfulness of steps when walking to the place where you are making your tea
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

    def populate_list_of_buttons(self):


        for rest_action in mb_model.RestActionsM.get_all():
            rest_action_qpb = QtWidgets.QPushButton(rest_action.title_str)
            rest_action_qpb.setCheckable(True)
            self.rest_actions_qbg.addButton(rest_action_qpb)
            self.ra_vbox.addWidget(rest_action_qpb)

        # store id as .data




