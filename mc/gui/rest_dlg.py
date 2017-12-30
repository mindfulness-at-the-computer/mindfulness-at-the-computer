import os

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from mc import model, mc_global


class RestDlg(QtWidgets.QDialog):
    # result_signal = QtCore.pyqtSignal(int)
    # -used both for wait and for closing
    close_signal = QtCore.pyqtSignal(bool)
    # -the boolean indicates whether or not we want the breathing dialog to open

    def __init__(self):
        super().__init__()
        self.show()
        self.raise_()
        self.showNormal()

        self.updating_gui_bool = False
        # self.rest_actions_qbg = QtWidgets.QButtonGroup()
        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addStretch(1)
        vbox_l2.addLayout(hbox_l3)
        vbox_l2.addStretch(1)

        # Main area
        self.main_area_qgb = QtWidgets.QGroupBox("Rest Actions")
        hbox_l3.addWidget(self.main_area_qgb)

        self.actions_list_vbox_l4 = QtWidgets.QVBoxLayout()
        self.main_area_qgb.setLayout(self.actions_list_vbox_l4)

        walking_mindfully_qll = QtWidgets.QLabel("Please move and walk mindfully when leaving the computer")
        walking_mindfully_qll.setFont(mc_global.get_font_medium())
        vbox_l2.addWidget(walking_mindfully_qll)
        vbox_l2.addStretch(1)

        buttons_hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(buttons_hbox_l3)

        self.close_qpb = QtWidgets.QPushButton("Close")
        buttons_hbox_l3.addWidget(self.close_qpb)
        self.close_qpb.clicked.connect(self.on_close_clicked)

        self.close_and_breathe_qpb = QtWidgets.QPushButton("Close and Breathe")
        buttons_hbox_l3.addWidget(self.close_and_breathe_qpb)
        self.close_and_breathe_qpb.clicked.connect(self.on_close_and_breathe_clicked)

        self.setup_rest_action_list()

    def on_close_clicked(self):
        self.close_signal.emit(False)
        self.close()

    def on_close_and_breathe_clicked(self):
        self.close_signal.emit(True)
        self.close()

    def setup_rest_action_list(self):
        rest_action_list = model.RestActionsM.get_all()
        for rest_action in rest_action_list:
            rest_action_title_qll = QtWidgets.QLabel(rest_action.title)
            rest_action_title_qll.setWordWrap(True)
            self.actions_list_vbox_l4.addWidget(rest_action_title_qll)

    def update_gui(self):
        self.updating_gui_bool = True

        pass

        self.updating_gui_bool = False
