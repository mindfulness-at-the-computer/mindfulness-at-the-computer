import os

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from mc import model, mc_global

IMAGE_GOAL_WIDTH_INT = 240
IMAGE_GOAL_HEIGHT_INT = IMAGE_GOAL_WIDTH_INT
CLOSED_RESULT_INT = -1
CLOSED_WITH_BREATHING_RESULT_INT = -2

class RestComposite(QtWidgets.QWidget):
    result_signal = QtCore.pyqtSignal(int)
    # -used both for wait and for closing

    def __init__(self):
        super().__init__()
        self.show()

        self.updating_gui_bool = False

        self.rest_actions_qbg = QtWidgets.QButtonGroup()

        # self.setWindowTitle("Please take care of yourself")
        # self.setWindowIcon(QtGui.QIcon(mc.mc_global.get_app_icon_path()))
        # self.setMinimumWidth(IMAGE_GOAL_WIDTH_INT * 2)
        # self.setMinimumHeight(IMAGE_GOAL_WIDTH_INT)
        # self.setSizePolicy(asdf)

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        # Main area

        title_qll = QtWidgets.QLabel("Please take good care of yourself")
        vbox_l2.addWidget(title_qll)
        vbox_l2.addStretch(1)

        # Image (or text if image is missing)
        self.image_qll = QtWidgets.QLabel()
        vbox_l2.addWidget(self.image_qll)
        self.image_qll.setScaledContents(True)
        self.image_qll.setMinimumWidth(IMAGE_GOAL_WIDTH_INT)
        self.image_qll.setMinimumHeight(IMAGE_GOAL_HEIGHT_INT)

        self.title_qll = QtWidgets.QLabel()
        vbox_l2.addWidget(self.title_qll)

        # self.image_qll.setPixmap(QtGui.QPixmap(mc_global.active_rest_image_full_path_str))
        # self.resize_image()

        vbox_l2.addStretch(1)

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
        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        hbox_l3.addWidget(self.close_qpb)
        self.close_qpb.clicked.connect(self.on_close_button_clicked)
        self.close_qpb.setFont(mc_global.get_font_large())
        hbox_l3.addStretch(1)

        self.start_breathing_qcb = QtWidgets.QCheckBox("Start breathing automatically")
        vbox_l2.addWidget(self.start_breathing_qcb)

    def on_wait_clicked(self):
        # minutes_int = self.wait_qsb.value()
        # self.dialog_outcome_int = minutes_int
        # self.accept()
        self.result_signal.emit(self.wait_qsb.value())

    def on_close_button_clicked(self):
        # self.dialog_outcome_int = CLOSED_RESULT_INT
        # self.accept()
        if self.start_breathing_qcb.isChecked():
            self.result_signal.emit(CLOSED_WITH_BREATHING_RESULT_INT)
        else:
            self.result_signal.emit(CLOSED_RESULT_INT)

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

    def update_gui(self):
        if mc_global.active_rest_action_id_it == mc_global.NO_REST_ACTION_SELECTED_INT:
            return
        self.updating_gui_bool = True

        rest_action = model.RestActionsM.get(mc_global.active_rest_action_id_it)
        if rest_action.image_path_str and os.path.isfile(rest_action.image_path_str):
            self.image_qll.show()
            self.image_qll.setPixmap(
                QtGui.QPixmap(
                    rest_action.image_path_str
                )
            )
            self.resize_image()
        else:
            self.image_qll.hide()
            self.image_qll.clear()

        self.title_qll.setText(rest_action.title_str)
        self.title_qll.setFont(mc_global.get_font_large())
        self.title_qll.setWordWrap(True)

        self.updating_gui_bool = False
