import logging

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from mc import model, mc_global


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

        """
        movement_qpb = QtWidgets.QPushButton("Movement exercise")
        rest_kindness_alternatives_qbb.addButton(movement_qpb, QtWidgets.QDialogButtonBox.YesRole)
        walk_qpb = QtWidgets.QPushButton("Taking a walk")
        rest_kindness_alternatives_qbb.addButton(walk_qpb, QtWidgets.QDialogButtonBox.YesRole)
        """

        self.rest_actions_qgb = QtWidgets.QGroupBox("Rest actions")
        vbox_l2.addWidget(self.rest_actions_qgb)
        self.ra_vbox = QtWidgets.QVBoxLayout()
        self.rest_actions_qgb.setLayout(self.ra_vbox)
        self.rest_actions_qbg = QtWidgets.QButtonGroup()

        self.populate_list_of_buttons()


        wait_qpb = QtWidgets.QPushButton("Wait (snooze) for 5 minutes")
        rest_kindness_alternatives_qbb.addButton(wait_qpb, QtWidgets.QDialogButtonBox.NoRole)

        close_qpb = QtWidgets.QPushButton("Close")
        rest_kindness_alternatives_qbb.addButton(close_qpb, QtWidgets.QDialogButtonBox.NoRole)
        close_qpb.clicked.connect(self.on_close_button_clicked)

        # Roles: http://doc.qt.io/qt-5/qdialogbuttonbox.html#ButtonRole-enum


        self.image_qll = QtWidgets.QLabel()
        hbox_l1.addWidget(self.image_qll)
        self.image_qll.setScaledContents(True)
        # self.image_qll.setPixmap(QtGui.QPixmap(mc_global.active_rest_image_full_path_str))
        # self.resize_image()



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
        rest_reminder_dialog = RestReminderDialog(i_parent)
        rest_reminder_dialog.show()  # -modeless

    def populate_list_of_buttons(self):

        for rest_action in model.RestActionsM.get_all():
            rest_action_cpb = CustomPushButton(
                rest_action.title_str,
                rest_action.id_int
            )
            rest_action_cpb.setCheckable(True)
            self.rest_actions_qbg.addButton(rest_action_cpb)
            self.ra_vbox.addWidget(rest_action_cpb)

            rest_action_cpb.button_clicked_signal.connect(self.on_rest_action_button_clicked)

    def on_rest_action_button_clicked(self, i_id: int):
        print("Id of button clicked: " + str(i_id))
        rest_action = model.RestActionsM.get(i_id)
        if rest_action.image_path_str:
            self.image_qll.setPixmap(
                QtGui.QPixmap(
                    rest_action.image_path_str
                )
            )
            self.resize_image()
        else:
            formatted_title_str = ""
            self.image_qll.setText(rest_action.title_str)
            new_font = QtGui.QFont()
            new_font.setPointSize(17)
            self.image_qll.setFont(new_font)

    def resize_image(self):
        if self.image_qll.pixmap() is None:
            return
        old_width_int = self.image_qll.pixmap().width()
        old_height_int = self.image_qll.pixmap().height()
        if old_width_int == 0:
            return
        goal_width_int = 400
        goal_height_int = 400
        width_relation_float = old_width_int / goal_width_int
        height_relation_float = old_height_int / goal_height_int

        # if width_relation_float > 1.0 or height_relation_float > 1.0:  # -scaling down
        if width_relation_float > height_relation_float:
            scaled_width_int = goal_width_int
            scaled_height_int = (scaled_width_int / old_width_int) * old_height_int
        else:
            scaled_height_int = goal_height_int
            scaled_width_int = (scaled_height_int / old_height_int) * old_width_int

        self.image_qll.setFixedWidth(scaled_width_int)
        self.image_qll.setFixedHeight(scaled_height_int)




class CustomPushButton(QtWidgets.QPushButton):
    button_clicked_signal = QtCore.pyqtSignal(int)
    def __init__(self, i_title: str, i_id: int):
        super().__init__(i_title)  # -TODO: Send parent as well here?
        self.id_int = i_id
        self.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        self.button_clicked_signal.emit(self.id_int)



