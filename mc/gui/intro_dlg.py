import logging
import mc.model
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import mc.gui.breathing_dlg
import mc.mc_global

NEXT_STR = "Next >>"
PARAGRAPH_SPACING_INT = 10


class IntroDlg(QtWidgets.QDialog):
    close_signal = QtCore.pyqtSignal(bool)
    # -the boolean indicates whether or not we want the breathing dialog to open

    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 550, 450)

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)
        self.wizard_qsw_w3 = QtWidgets.QStackedWidget()
        vbox_l2.addWidget(self.wizard_qsw_w3)

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        hbox_l3.addStretch(1)
        self.prev_qpb = QtWidgets.QPushButton("<< Prev")
        hbox_l3.addWidget(self.prev_qpb, stretch=1)
        self.prev_qpb.clicked.connect(self.on_prev_clicked)
        self.next_qpb = QtWidgets.QPushButton(NEXT_STR)
        hbox_l3.addWidget(self.next_qpb, stretch=1)
        hbox_l3.addStretch(1)
        self.next_qpb.clicked.connect(self.on_next_clicked)

        self.info = InformationPage()
        self.wizard_qsw_w3.addWidget(self.info)

        self.initial_setup = BreathingInitSetupPage()
        self.wizard_qsw_w3.addWidget(self.initial_setup)

        self.breathing_dialog_coming = BreathingDialogComing()
        self.wizard_qsw_w3.addWidget(self.breathing_dialog_coming)

        self.update_gui()

        self.show()

    def on_next_clicked(self):
        current_index_int = self.wizard_qsw_w3.currentIndex()
        if current_index_int >= self.wizard_qsw_w3.count() - 1:
            self.close_signal.emit(True)
            self.close()
        logging.debug("current_index_int = " + str(current_index_int))
        self.wizard_qsw_w3.setCurrentIndex(current_index_int + 1)
        self.update_gui()

    def on_prev_clicked(self):
        current_index_int = self.wizard_qsw_w3.currentIndex()
        if current_index_int <= 0:
            return
        logging.debug("current_index_int = " + str(current_index_int))
        self.wizard_qsw_w3.setCurrentIndex(current_index_int - 1)
        self.update_gui()

    def update_gui(self):
        current_index_int = self.wizard_qsw_w3.currentIndex()
        self.prev_qpb.setDisabled(current_index_int == 0)

        if current_index_int == self.wizard_qsw_w3.count() - 1:
            self.next_qpb.setText("Finish")  # "open breathing dialog"
        else:
            self.next_qpb.setText(NEXT_STR)


class InformationPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.title_qll = QtWidgets.QLabel("Introduction")
        self.title_qll.setFont(mc.mc_global.get_font_xlarge())
        vbox_l2.addWidget(self.title_qll)

        vbox_l2.addStretch(1)

        self.text_qll = QtWidgets.QLabel(
            'Welcome! You can use this wizard to read about and set up the application. '
            'You can return to this wizard later by going to "help" -> "setup wizard"'
        )
        self.text_qll.setWordWrap(True)
        vbox_l2.addWidget(self.text_qll)

        vbox_l2.addSpacing(PARAGRAPH_SPACING_INT)

        self.text_2_qll = QtWidgets.QLabel(
            "This application reminds you to stay aware of your breathing and to take breaks. "
            "These are the parts of the interface:"
            "\n1. The breathing dialog and notifications"
            "\n2. The rest dialog and notifications"
            '\n3. The settings window (available from systray menu -> "open settings")'
            "\n4. The system tray icon and menu"
        )
        self.text_2_qll.setWordWrap(True)
        vbox_l2.addWidget(self.text_2_qll)

        vbox_l2.addStretch(1)


class BreathingDialogComing(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.title_qll = QtWidgets.QLabel("Breathing Dialog")
        self.title_qll.setFont(mc.mc_global.get_font_xlarge())
        vbox_l2.addWidget(self.title_qll)

        vbox_l2.addStretch(1)

        self.text_qll = QtWidgets.QLabel(
            "When you click on finish and exit this wizard a breathing dialog will be shown. "
            "You can use it by holding the mouse cursor over the central breathing square while breathing in, "
            "and over the background area/rectangle while breathing out"
        )
        self.text_qll.setWordWrap(True)
        vbox_l2.addWidget(self.text_qll)

        vbox_l2.addStretch(1)


class BreathingInitSetupPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        settings = mc.model.SettingsM.get()

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.title_qll = QtWidgets.QLabel("Initial setup (breathing)")
        self.title_qll.setFont(mc.mc_global.get_font_xlarge())
        vbox_l2.addWidget(self.title_qll)

        vbox_l2.addStretch(1)

        self.text_qll = QtWidgets.QLabel(
            "Please select the initial setup parameters for the breathing dialog. "
            "It's possible to change the values later on using the settings window "
            '(available from the systray menu -> "Open Settings").'
        )
        self.text_qll.setWordWrap(True)
        vbox_l2.addWidget(self.text_qll)

        vbox_l2.addStretch(1)

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        hbox_l3.addWidget(QtWidgets.QLabel("Time between breathing notifications"))
        self.time_btw_notifications_qsb = QtWidgets.QSpinBox()
        hbox_l3.addWidget(self.time_btw_notifications_qsb)
        self.time_btw_notifications_qsb.valueChanged.connect(
            self.on_time_btw_notifications_value_changed
        )
        self.time_btw_notifications_qsb.setValue(settings.breathing_reminder_interval_int)

        vbox_l2.addStretch(1)

        """
        self.play_audio_qcb = QtWidgets.QCheckBox("Play Audio")
        vbox_l2.addWidget(self.play_audio_qcb)
        self.play_audio_qcb.toggled.connect(self.on_play_audio_toggled)
        """

    def on_time_btw_notifications_value_changed(self, i_new_value: int):
        logging.debug("on_time_btw_notifications_value_changed, i_new_value = " + str(i_new_value))
        mc.model.SettingsM.update_breathing_reminder_interval(i_new_value)

    def on_play_audio_toggled(self, i_checked: bool):
        mc.model.SettingsM.update_breathing_dialog_audio_active(i_checked)
        if not mc.model.SettingsM.get().breathing_reminder_audio_path_str:
            mc.model.SettingsM.update_breathing_reminder_audio_path("small_bell_long[cc0].wav")

