import logging

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from mc import model, mc_global
import mc.win.quotes

IMAGE_GOAL_WIDTH_INT = 240
IMAGE_GOAL_HEIGHT_INT = IMAGE_GOAL_WIDTH_INT
CLOSED_RESULT_INT = -1


class RestReminderDialog(QtWidgets.QDialog):
    def __init__(self, i_parent):
        super(RestReminderDialog, self).__init__(i_parent)
        self.setWindowTitle("Please take care of yourself")
        self.setWindowIcon(QtGui.QIcon("icon.png"))

        self.dialog_outcome_int = CLOSED_RESULT_INT

        vbox_l2 = QtWidgets.QVBoxLayout(self)
        # -please note: If we don't send "self" to the QVBoxLayout we won't see the main window
        #  in the background of the dialog. Also we don't need to use self.setLayout(vbox)

        self.tabs = QtWidgets.QTabWidget()
        vbox_l2.addWidget(self.tabs)
        self.tabs.setTabPosition(QtWidgets.QTabWidget.West)

        rest_actions_widget = RestReminderActions()
        self.tabs.addTab(rest_actions_widget, "Rest actions")

        rest_quotes_widget = RestReminderQuotes()
        self.tabs.addTab(rest_quotes_widget, "Wisdom")



        hbox = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox)

        wait_qpb = QtWidgets.QPushButton("Wait")
        hbox.addWidget(wait_qpb)
        wait_qpb.clicked.connect(self.on_wait_clicked)
        hbox.addWidget(QtWidgets.QLabel("for"))
        self.wait_qsb = QtWidgets.QSpinBox()
        self.wait_qsb.setMinimum(1)
        hbox.addWidget(self.wait_qsb)
        hbox.addWidget(QtWidgets.QLabel("minutes"))
        hbox.addStretch(1)

        close_qpb = QtWidgets.QPushButton("Close")
        hbox.addWidget(close_qpb)
        close_qpb.clicked.connect(self.on_close_button_clicked)
        # Roles: http://doc.qt.io/qt-5/qdialogbuttonbox.html#ButtonRole-enum

    def on_wait_clicked(self):
        self.parent().show()
        # -this is done to avoid the dialog closing in cases when the application is
        # "running in the tray"
        minutes_int = self.wait_qsb.value()
        self.dialog_outcome_int = minutes_int
        self.accept()

    def on_close_button_clicked(self):
        self.parent().show()
        # -this is done to avoid the dialog closing in cases when the application is
        # "running in the tray"
        self.dialog_outcome_int = CLOSED_RESULT_INT
        self.accept()

    @staticmethod
    def show_dialog(i_parent):
        rest_reminder_dialog = RestReminderDialog(i_parent)
        rest_reminder_dialog.show()  # -modeless


class CustomPushButton(QtWidgets.QPushButton):
    button_clicked_signal = QtCore.pyqtSignal(int)
    def __init__(self, i_title: str, i_id: int):
        super().__init__(i_title)  # -TODO: Send parent as well here?
        self.id_int = i_id
        self.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        self.button_clicked_signal.emit(self.id_int)


class RestReminderActions(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        hbox_l2 = QtWidgets.QHBoxLayout()
        self.setLayout(hbox_l2)

        vbox_l3 = QtWidgets.QVBoxLayout()
        hbox_l2.addLayout(vbox_l3)

        # Rest actions
        self.rest_actions_qbg = QtWidgets.QButtonGroup()

        rest_kindness_actions_qgb = QtWidgets.QGroupBox()
        vbox_l3.addWidget(rest_kindness_actions_qgb)
        self.rka_vbox_l3 = QtWidgets.QVBoxLayout()
        rest_kindness_actions_qgb.setLayout(self.rka_vbox_l3)

        self.populate_list_of_buttons()

        self.image_qll = QtWidgets.QLabel()
        hbox_l2.addWidget(self.image_qll)
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

    def populate_list_of_buttons(self):

        for rest_action in model.RestActionsM.get_all():
            rest_action_cpb = CustomPushButton(
                rest_action.title_str,
                rest_action.id_int
            )
            rest_action_cpb.setCheckable(True)
            self.rest_actions_qbg.addButton(rest_action_cpb)
            self.rka_vbox_l3.addWidget(rest_action_cpb)

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
            self.image_qll.setText(rest_action.title_str)
            new_font = QtGui.QFont()
            new_font.setPointSize(14)
            self.image_qll.setFont(new_font)
            self.image_qll.setWordWrap(True)

    def resize_image(self):
        if self.image_qll.pixmap() is None:
            return
        old_width_int = self.image_qll.pixmap().width()
        old_height_int = self.image_qll.pixmap().height()
        if old_width_int == 0:
            return
        width_relation_float = old_width_int / IMAGE_GOAL_WIDTH_INT
        height_relation_float = old_height_int / IMAGE_GOAL_HEIGHT_INT

        if width_relation_float > height_relation_float:
            scaled_width_int = IMAGE_GOAL_WIDTH_INT
            scaled_height_int = (scaled_width_int / old_width_int) * old_height_int
        else:
            scaled_height_int = IMAGE_GOAL_HEIGHT_INT
            scaled_width_int = (scaled_height_int / old_height_int) * old_width_int

        self.image_qll.setFixedWidth(scaled_width_int)
        self.image_qll.setFixedHeight(scaled_height_int)


class RestReminderQuotes(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)


        quotes_widget = mc.win.quotes.CompositeQuotesWidget()
        vbox_l2.addWidget(quotes_widget)


