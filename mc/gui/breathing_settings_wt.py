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

        # Notifications
        self.notifications_qgb = QtWidgets.QGroupBox(self.tr("Notifications"))
        vbox_l2.addWidget(self.notifications_qgb)
        vbox_l3 = QtWidgets.QVBoxLayout()
        self.notifications_qgb.setLayout(vbox_l3)

        hbox_l4 = QtWidgets.QHBoxLayout()
        vbox_l3.addLayout(hbox_l4)
        hbox_l4.addWidget(QtWidgets.QLabel(self.tr("Notification type: ")))
        hbox_l4.addStretch(1)
        self.notification_type_qcb = QtWidgets.QComboBox()
        hbox_l4.addWidget(self.notification_type_qcb)
        self.notification_type_qcb.addItems([
            mc.mc_global.NotificationType.Visual.name,
            mc.mc_global.NotificationType.Audio.name,
            mc.mc_global.NotificationType.Both.name
        ])
        self.notification_type_qcb.activated.connect(self.on_notification_type_activated)

        hbox_l4 = QtWidgets.QHBoxLayout()
        vbox_l3.addLayout(hbox_l4)
        self.breathing_reminder_interval_qll = QtWidgets.QLabel(self.tr("Interval:"))
        hbox_l4.addWidget(self.breathing_reminder_interval_qll)
        self.breathing_reminder_interval_qsb = QtWidgets.QSpinBox()
        hbox_l4.addWidget(self.breathing_reminder_interval_qsb)
        self.breathing_reminder_interval_qsb.valueChanged.connect(
            self.on_breathing_interval_value_changed
        )
        hbox_l4.addWidget(QtWidgets.QLabel(self.tr("minutes")))
        hbox_l4.addStretch(1)

        # Dialog
        self.dialog_qgb = QtWidgets.QGroupBox(self.tr("Dialog"))
        vbox_l2.addWidget(self.dialog_qgb)
        vbox_l3 = QtWidgets.QVBoxLayout()
        self.dialog_qgb.setLayout(vbox_l3)

        hbox_l4 = QtWidgets.QHBoxLayout()
        vbox_l3.addLayout(hbox_l4)
        hbox_l4.addWidget(QtWidgets.QLabel(self.tr("Phrase setup: ")))
        hbox_l4.addStretch(1)
        self.phrase_setup_qcb = QtWidgets.QComboBox()
        hbox_l4.addWidget(self.phrase_setup_qcb)
        self.phrase_setup_qcb.activated.connect(self.on_phrase_setup_activated)
        self.phrase_setup_qcb.addItems([
            mc.mc_global.PhraseSetup.Long.name,
            mc.mc_global.PhraseSetup.Switch.name,
            mc.mc_global.PhraseSetup.Short.name
        ])

        hbox_l4 = QtWidgets.QHBoxLayout()
        vbox_l3.addLayout(hbox_l4)
        hbox_l4.addWidget(QtWidgets.QLabel(self.tr("Show after")))
        self.notifications_per_dialog_qsb = QtWidgets.QSpinBox()
        hbox_l4.addWidget(self.notifications_per_dialog_qsb)
        self.notifications_per_dialog_qsb.valueChanged.connect(self.on_notifications_per_dialog_qsb_changed)
        hbox_l4.addWidget(QtWidgets.QLabel(self.tr("notifications")))
        hbox_l4.addStretch(1)

        self.dialog_audio_qcb = QtWidgets.QCheckBox(self.tr("Play Audio"))
        vbox_l3.addWidget(self.dialog_audio_qcb)
        self.dialog_audio_qcb.toggled.connect(self.on_dialog_audio_toggled)

        self.test_breathing_dialog_qpb = QtWidgets.QPushButton(self.tr("Open breathing dialog"))
        vbox_l3.addWidget(self.test_breathing_dialog_qpb)
        self.test_breathing_dialog_qpb.clicked.connect(self.on_open_breathing_dialog_button_clicked)

        # Audio
        self.audio_qgb = QtWidgets.QGroupBox(self.tr("Audio"))
        vbox_l2.addWidget(self.audio_qgb)
        vbox_l3 = QtWidgets.QVBoxLayout()
        self.audio_qgb.setLayout(vbox_l3)
        self.select_audio_qpb = QtWidgets.QPushButton(self.tr("Select audio"))
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

    def on_dialog_audio_toggled(self, i_checked: bool):
        if self.updating_gui_bool:
            return
        mc.model.SettingsM.update_breathing_dialog_audio_active(i_checked)

    def on_phrase_setup_activated(self, i_index: int):
        # -activated is only triggered on user action
        mc.model.SettingsM.update_breathing_reminder_notification_phrase_setup(i_index)

    def on_notification_type_activated(self, i_index: int):
        # -activated is only triggered on user action
        mc.model.SettingsM.update_breathing_reminder_notification_type(i_index)

    def on_notifications_per_dialog_qsb_changed(self, i_new_value: int):
        if self.updating_gui_bool:
            return
        mc.model.SettingsM.update_breathing_reminder_nr_per_dialog(i_new_value)

    def volume_changed(self, i_value: int):
        if self.updating_gui_bool:
            return
        mc.model.SettingsM.update_breathing_reminder_volume(i_value)

    def on_select_audio_clicked(self):
        # noinspection PyCallByClass
        audio_file_result_tuple = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Please choose a wav audio file"),
            mc_global.get_user_audio_path(),
            self.tr("Wav files (*.wav)")
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

    def on_open_breathing_dialog_button_clicked(self):
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

        breathing_notification_type_enum = mc.mc_global.NotificationType(
            settings.breathing_reminder_notification_type_int
        )
        self.notification_type_qcb.setCurrentText(breathing_notification_type_enum.name)
        phrase_setup_enum = mc.mc_global.PhraseSetup(
            settings.breathing_reminder_phrase_setup_int
        )
        self.phrase_setup_qcb.setCurrentText(phrase_setup_enum.name)

        self.dialog_audio_qcb.setChecked(settings.breathing_reminder_dialog_audio_active_bool)

        self.notifications_per_dialog_qsb.setValue(
            settings.breathing_reminder_nr_before_dialog_int
        )

        self.updating_gui_bool = False
