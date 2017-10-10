import logging
import os

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from mc import model, mc_global
import mc.gui.quotes_cw

IMAGE_GOAL_WIDTH_INT = 240
IMAGE_GOAL_HEIGHT_INT = IMAGE_GOAL_WIDTH_INT
CLOSED_RESULT_INT = -1


class RestReminderComposite(QtWidgets.QWidget):
    result_signal = QtCore.pyqtSignal(int)
    # -used both for wait and for closing

    def __init__(self):
        super().__init__()
        self.show()

        self.rest_actions_qbg = QtWidgets.QButtonGroup()

        # self.setWindowTitle("Please take care of yourself")
        # self.setWindowIcon(QtGui.QIcon(mc.mc_global.get_app_icon_path()))
        # self.setMinimumWidth(IMAGE_GOAL_WIDTH_INT * 2)
        # self.setMinimumHeight(IMAGE_GOAL_WIDTH_INT)
        # self.setSizePolicy(asdf)

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        # Main area
        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)

        # Rest actions
        vbox_l4 = QtWidgets.QVBoxLayout()
        hbox_l3.addLayout(vbox_l4)
        rest_kindness_actions_qgb_l5 = QtWidgets.QGroupBox()
        vbox_l4.addStretch(1)
        vbox_l4.addWidget(rest_kindness_actions_qgb_l5)
        vbox_l4.addStretch(1)
        self.rka_vbox_l5 = QtWidgets.QVBoxLayout()
        rest_kindness_actions_qgb_l5.setLayout(self.rka_vbox_l5)
        self.populate_list_of_buttons()

        # Image (or text if image is missing)
        self.image_qll = QtWidgets.QLabel()
        hbox_l3.addWidget(self.image_qll)
        self.image_qll.setScaledContents(True)
        self.image_qll.setMinimumWidth(IMAGE_GOAL_WIDTH_INT)
        self.image_qll.setMinimumHeight(IMAGE_GOAL_HEIGHT_INT)
        # self.image_qll.setPixmap(QtGui.QPixmap(mc_global.active_rest_image_full_path_str))
        # self.resize_image()

        # Line of buttons (and widgets) at the bottom of the widget
        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)

        wait_qpb = QtWidgets.QPushButton("Wait")
        hbox_l3.addWidget(wait_qpb)
        wait_qpb.clicked.connect(self.on_wait_clicked)
        hbox_l3.addWidget(QtWidgets.QLabel("for"))
        self.wait_qsb = QtWidgets.QSpinBox()
        self.wait_qsb.setMinimum(1)
        hbox_l3.addWidget(self.wait_qsb)
        hbox_l3.addWidget(QtWidgets.QLabel("minutes"))
        hbox_l3.addStretch(1)

        self.close_qpb = QtWidgets.QPushButton("Close and Reset Rest Timer")
        hbox_l3.addWidget(self.close_qpb)
        self.close_qpb.clicked.connect(self.on_close_button_clicked)

    def on_wait_clicked(self):
        # minutes_int = self.wait_qsb.value()
        # self.dialog_outcome_int = minutes_int
        # self.accept()
        self.result_signal.emit(self.wait_qsb.value())

    def on_close_button_clicked(self):
        # self.dialog_outcome_int = CLOSED_RESULT_INT
        # self.accept()
        self.result_signal.emit(CLOSED_RESULT_INT)

    def populate_list_of_buttons(self):
        for rest_action in model.RestActionsM.get_all():
            rest_action_cpb = CustomPushButton(
                rest_action.title_str,
                rest_action.id_int
            )
            rest_action_cpb.setCheckable(True)
            self.rest_actions_qbg.addButton(rest_action_cpb)
            self.rka_vbox_l5.addWidget(rest_action_cpb)
            rest_action_cpb.button_clicked_signal.connect(self.on_rest_action_button_clicked)

    def on_rest_action_button_clicked(self, i_id: int):
        logging.debug("Id of button clicked: " + str(i_id))
        rest_action = model.RestActionsM.get(i_id)
        if rest_action.image_path_str and os.path.isfile(rest_action.image_path_str):
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


class CustomPushButton(QtWidgets.QPushButton):
    button_clicked_signal = QtCore.pyqtSignal(int)

    def __init__(self, i_title: str, i_id: int):
        super().__init__(i_title)  # -TODO: Send parent as well here?
        self.id_int = i_id
        self.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        self.button_clicked_signal.emit(self.id_int)

