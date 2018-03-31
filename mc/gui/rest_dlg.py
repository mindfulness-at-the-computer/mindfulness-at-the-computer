from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSysInfo

from mc import model, mc_global


class RestDlg(QtWidgets.QDialog):
    # result_signal = QtCore.pyqtSignal(int)
    # -used both for wait and for closing
    close_signal = QtCore.pyqtSignal(bool)
    intention_signal = QtCore.pyqtSignal(bool)
    # -the boolean indicates whether or not we want the breathing or intention dialog to open

    def __init__(self):
        super().__init__()

        self.show()
        self.raise_()
        self.showNormal()

        self.updating_gui_bool = False
        # self.rest_actions_qbg = QtWidgets.QButtonGroup()
        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        # Centering vertically and horizontally
        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addStretch(1)
        vbox_l2.addLayout(hbox_l3)
        vbox_l2.addStretch(1)
        # vbox_l4 = QtWidgets.QVBoxLayout()
        hbox_l3.addStretch(2)
        # hbox_l3.addLayout(vbox_l4)

        # Main area
        self.main_area_qgb = QtWidgets.QGroupBox("Rest Actions")
        hbox_l3.addWidget(self.main_area_qgb, stretch=3)

        self.actions_list_vbox_l4 = QtWidgets.QVBoxLayout()
        self.main_area_qgb.setLayout(self.actions_list_vbox_l4)

        walking_mindfully_qll = QtWidgets.QLabel("Please move and walk mindfully when leaving the computer")
        walking_mindfully_qll.setFont(mc_global.get_font_xxlarge())
        walking_mindfully_qll.setWordWrap(True)
        hbox_l3.addWidget(walking_mindfully_qll, stretch=3)

        hbox_l3.addStretch(2)


        buttons_hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(buttons_hbox_l3)
        buttons_hbox_l3.addStretch(3)

        self.close_qpb = QtWidgets.QPushButton("Close")
        buttons_hbox_l3.addWidget(self.close_qpb, stretch=2)
        self.close_qpb.clicked.connect(self.on_close_clicked)

        self.close_and_breathe_qpb = QtWidgets.QPushButton("Close and Breathe")
        buttons_hbox_l3.addWidget(self.close_and_breathe_qpb, stretch=2)
        self.close_and_breathe_qpb.clicked.connect(self.on_close_and_breathe_clicked)

        self.close_and_set_intention_qpb = QtWidgets.QPushButton("Close and set an intention")
        buttons_hbox_l3.addWidget(self.close_and_set_intention_qpb, stretch=2)
        self.close_and_set_intention_qpb.clicked.connect(self.on_close_and_set_intention_clicked)

        buttons_hbox_l3.addStretch(3)

        self.setup_rest_action_list()

        self.setStyleSheet(
            "background-color:#101010;"
            "color: #999999;"
            "selection-background-color:" + mc_global.MC_LIGHT_GREEN_COLOR_STR + ";"
            "selection-color:#000000;"
        )

        #  On MacOs showFullScreen has unwanted side effects. Therefore we choose showMaximized on MacOS
        if QSysInfo.kernelType() == "darwin":
            self.showMaximized()
        else:
            self.showFullScreen()

        mc_global.rest_window_shown_bool = True

    def on_close_clicked(self):
        self.close_signal.emit(False)
        mc_global.rest_window_shown_bool = False
        self.close()

    def on_close_and_breathe_clicked(self):
        self.close_signal.emit(True)
        mc_global.rest_window_shown_bool = False
        self.close()

    def on_close_and_set_intention_clicked(self):
        self.intention_signal.emit(True)
        mc_global.rest_window_shown_bool = False
        self.close()


    def setup_rest_action_list(self):
        rest_action_list = model.RestActionsM.get_all()

        for rest_action in rest_action_list:
            rest_action_title_qll = QtWidgets.QLabel(rest_action.title)
            rest_action_title_qll.setWordWrap(True)
            rest_action_title_qll.setFont(mc_global.get_font_large())
            rest_action_title_qll.setContentsMargins(10, 5, 10, 5)
            self.actions_list_vbox_l4.addWidget(rest_action_title_qll)

    def update_gui(self):
        self.updating_gui_bool = True
        pass
        self.updating_gui_bool = False
