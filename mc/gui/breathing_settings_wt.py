import os
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from mc import model, mc_global
import mc.gui.toggle_switch_wt

MIN_REST_REMINDER_INT = 1  # -in minutes
NO_AUDIO_SELECTED_STR = "No audio selected"


class BreathingSettingsWt(QtWidgets.QWidget):
    rest_settings_updated_signal = QtCore.pyqtSignal()
    updated_signal = QtCore.pyqtSignal()
    breathe_now_button_clicked_signal = QtCore.pyqtSignal()
    rest_test_button_clicked_signal = QtCore.pyqtSignal()
    rest_reset_button_clicked_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.updating_gui_bool = False

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        self.toggle_switch = mc.gui.toggle_switch_wt.ToggleSwitchWt()
        hbox_l3.addWidget(self.toggle_switch)
        self.toggle_switch.toggled_signal.connect(self.on_switch_toggled)

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        self.breathing_reminder_interval_qll = QtWidgets.QLabel("Interval:")
        hbox_l3.addWidget(self.breathing_reminder_interval_qll)
        self.breathing_reminder_interval_qsb = QtWidgets.QSpinBox()
        hbox_l3.addWidget(self.breathing_reminder_interval_qsb)
        self.breathing_reminder_interval_qsb.valueChanged.connect(
            self.on_breathing_interval_value_changed
        )
        hbox_l3.addWidget(QtWidgets.QLabel("minutes"))
        hbox_l3.addStretch(1)

        self.test_breathing_dialog_qpb = QtWidgets.QPushButton("Open breathing dialog")
        vbox_l2.addWidget(self.test_breathing_dialog_qpb)
        self.test_breathing_dialog_qpb.clicked.connect(self.on_test_breathing_dialog_button_clicked)


        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        hbox_l3.addWidget(QtWidgets.QLabel("Notification type: "))
        hbox_l3.addStretch(1)
        self.notification_type_qcb = QtWidgets.QComboBox()
        hbox_l3.addWidget(self.notification_type_qcb)
        self.notification_type_qcb.addItems([
            mc.mc_global.BreathingNotificationType.Visual.name,
            mc.mc_global.BreathingNotificationType.Audio.name,
            mc.mc_global.BreathingNotificationType.Both.name
        ])
        self.notification_type_qcb.activated.connect(self.on_notification_type_activated)


        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        hbox_l3.addWidget(QtWidgets.QLabel("Phrase setup: "))
        hbox_l3.addStretch(1)
        self.phrase_setup_qcb = QtWidgets.QComboBox()
        hbox_l3.addWidget(self.phrase_setup_qcb)
        self.phrase_setup_qcb.activated.connect(self.on_phrase_setup_activated)
        self.phrase_setup_qcb.addItems([
            mc.mc_global.PhraseSetup.Long.name,
            mc.mc_global.PhraseSetup.Switch.name,
            mc.mc_global.PhraseSetup.Short.name
        ])

        self.active_breathing_phrase_qgb = QtWidgets.QGroupBox("Active Breathing Phrase")
        vbox_l2.addWidget(self.active_breathing_phrase_qgb)
        vbox_l3 = QtWidgets.QVBoxLayout()
        self.active_breathing_phrase_qgb.setLayout(vbox_l3)
        self.title_text_qll = QtWidgets.QLabel("title")
        vbox_l3.addWidget(self.title_text_qll)
        self.in_text_qll = QtWidgets.QLabel("in")
        vbox_l3.addWidget(self.in_text_qll)
        self.out_text_qll = QtWidgets.QLabel("out")
        vbox_l3.addWidget(self.out_text_qll)

        self.audio_qgb = QtWidgets.QGroupBox("Audio")
        vbox_l2.addWidget(self.audio_qgb)
        vbox_l3 = QtWidgets.QVBoxLayout()
        self.audio_qgb.setLayout(vbox_l3)
        self.select_audio_qpb = QtWidgets.QPushButton("Select audio")
        vbox_l3.addWidget(self.select_audio_qpb)
        self.select_audio_qpb.clicked.connect(self.on_select_audio_clicked)
        self.audio_path_qll = QtWidgets.QLabel(NO_AUDIO_SELECTED_STR)
        vbox_l3.addWidget(self.audio_path_qll)
        self.audio_path_qll.setWordWrap(True)
        self.volume_qsr = QtWidgets.QSlider()
        vbox_l3.addWidget(self.volume_qsr)
        self.volume_qsr.setOrientation(QtCore.Qt.Horizontal)
        self.volume_qsr.setMinimum(0)
        self.volume_qsr.setMaximum(100)
        self.volume_qsr.valueChanged.connect(self.volume_changed)

        vbox_l2.addStretch(1)

        # self.breathing_reminder_qgb.setDisabled(True)  # -disabled until a phrase has been selected
        self.setDisabled(True)

        self.update_gui()

    def on_phrase_setup_activated(self, i_index: int):
        # -activated is only triggered on user action
        mc.model.SettingsM.update_breathing_reminder_notification_phrase_setup(i_index)

    def on_notification_type_activated(self, i_index: int):
        # -activated is only triggered on user action
        mc.model.SettingsM.update_breathing_reminder_notification_type(i_index)

    def volume_changed(self, i_value: int):
        if self.updating_gui_bool:
            return
        mc.model.SettingsM.update_breathing_reminder_volume(i_value)

    def on_select_audio_clicked(self):
        # noinspection PyCallByClass
        audio_file_result_tuple = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Please choose a wav audio file",
            mc_global.get_user_audio_path(),
            "Wav files (*.wav)"
        )
        new_file_path_str = audio_file_result_tuple[0]
        if new_file_path_str:
            mc.model.SettingsM.update_breathing_reminder_audio_path(new_file_path_str)
        else:
            pass
        self.update_gui_audio_details()

    def update_gui_audio_details(self):
        self.updating_gui_bool = True
        settings = mc.model.SettingsM.get()

        audio_path_str = settings.breathing_reminder_audio_path_str
        audio_file_name_str = os.path.basename(audio_path_str)
        if audio_file_name_str:
            self.audio_path_qll.setText(audio_file_name_str)
        else:
            self.audio_path_qll.setText(NO_AUDIO_SELECTED_STR)

        self.volume_qsr.setValue(settings.breathing_reminder_volume_int)

        self.updating_gui_bool = False

    def on_test_breathing_dialog_button_clicked(self):
        self.breathe_now_button_clicked_signal.emit()

    def on_switch_toggled(self, i_checked_bool):
        if self.updating_gui_bool:
            return
        model.SettingsM.update_breathing_reminder_active(i_checked_bool)
        self.updated_signal.emit()

    def on_breathing_interval_value_changed(self, i_new_value: int):
        if self.updating_gui_bool:
            return
        model.SettingsM.update_breathing_reminder_interval(i_new_value)
        self.updated_signal.emit()

    def update_gui(self):
        self.updating_gui_bool = True

        settings = mc.model.SettingsM.get()

        # Breathing reminder
        if mc_global.active_phrase_id_it != mc_global.NO_PHRASE_SELECTED_INT:
            self.setDisabled(False)
            breathing_phrase = mc.model.PhrasesM.get(mc_global.active_phrase_id_it)
            self.title_text_qll.setText(breathing_phrase.title_str)
            self.in_text_qll.setText(breathing_phrase.ib_str)
            self.out_text_qll.setText(breathing_phrase.ob_str)
        else:
            self.setDisabled(True)

        br_enabled = settings.breathing_reminder_active_bool
        self.toggle_switch.update_gui(br_enabled)

        breathing_reminder_interval_minutes_int = settings.breathing_reminder_interval_int
        self.breathing_reminder_interval_qsb.setValue(breathing_reminder_interval_minutes_int)
        """
        breathing_reminder_length_minutes_int = model.SettingsM.get().breathing_reminder_length_int
        self.breathing_reminder_length_qsb.setValue(breathing_reminder_length_minutes_int)
        """

        self.update_gui_audio_details()

        breathing_notification_type_enum = mc.mc_global.BreathingNotificationType(
            settings.breathing_reminder_notification_type_int
        )
        self.notification_type_qcb.setCurrentText(breathing_notification_type_enum.name)
        phrase_setup_enum = mc.mc_global.PhraseSetup(
            settings.breathing_reminder_phrase_setup_int
        )
        self.phrase_setup_qcb.setCurrentText(phrase_setup_enum.name)

        self.updating_gui_bool = False
