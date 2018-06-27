from PyQt5 import QtCore
from PyQt5 import QtWidgets
from mc import model, mc_global
import pygame

class RestDlg(QtWidgets.QDialog):
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


        self.choose_music_qpb = QtWidgets.QPushButton("Choose music")
        buttons_hbox_l3.addWidget(self.choose_music_qpb, stretch=2)
        self.choose_music_qpb.clicked.connect(self.on_choose_music_clicked)

        buttons_hbox_l3.addStretch(3)

        self.setup_rest_action_list()

        self.setStyleSheet(
            "background-color:#101010;"
            "color: #999999;"
            "selection-background-color:" + mc_global.MC_LIGHT_GREEN_COLOR_STR + ";"
            "selection-color:#000000;"
        )

        self.showFullScreen()

        mc_global.rest_window_shown_bool = True


    def on_choose_music_clicked(self):
        audio_file_result_tuple = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Please choose an mp3 audio file"),
            mc_global.get_user_audio_path(),
            self.tr("Mp3 files (*.mp3)")
            )
        if audio_file_result_tuple[0] != '':
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file_result_tuple[0])
            pygame.mixer.music.play(0)

    def on_close_clicked(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        self.showNormal()
        # -for MacOS. showNormal is used here rather than showMinimized to avoid animation
        self.close_signal.emit(False)
        mc_global.rest_window_shown_bool = False
        self.close()

    def on_close_and_breathe_clicked(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        self.showMinimized()
        # -for MacOS
        self.close_signal.emit(True)
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
