from PyQt5 import QtCore
from PyQt5 import QtWidgets

from mc import model, mc_global

# Here we place settings for the application, for example the time between notifications,
# as well as if there is audio as well as the notification
# Perhaps we want to hide some of these settings?
# All intervals are in minutes

MIN_REST_REMINDER_INT = 1  # -in minutes


class BreathingSettingsComposite(QtWidgets.QWidget):
    rest_settings_updated_signal = QtCore.pyqtSignal()
    breathing_settings_updated_signal = QtCore.pyqtSignal()
    breathing_test_button_clicked_signal = QtCore.pyqtSignal()
    rest_test_button_clicked_signal = QtCore.pyqtSignal()
    rest_reset_button_clicked_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.updating_gui_bool = False

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        self.breathing_reminder_qgb = QtWidgets.QGroupBox("Breathing Reminder")
        vbox.addWidget(self.breathing_reminder_qgb)
        br_vbox = QtWidgets.QVBoxLayout()
        self.breathing_reminder_qgb.setLayout(br_vbox)
        self.breathing_reminder_enabled_qcb = QtWidgets.QCheckBox("Active")
        br_vbox.addWidget(self.breathing_reminder_enabled_qcb)
        self.breathing_reminder_enabled_qcb.toggled.connect(self.on_breathing_active_toggled)
        self.breathing_reminder_interval_qll = QtWidgets.QLabel("Interval (seconds)")
        br_vbox.addWidget(self.breathing_reminder_interval_qll)
        self.breathing_reminder_interval_qsb = QtWidgets.QSpinBox()
        br_vbox.addWidget(self.breathing_reminder_interval_qsb)
        self.breathing_reminder_interval_qsb.valueChanged.connect(
            self.on_breathing_interval_value_changed
        )
        self.breathing_reminder_length_qll = QtWidgets.QLabel("Length (seconds)")
        br_vbox.addWidget(self.breathing_reminder_length_qll)
        self.breathing_reminder_length_qsb = QtWidgets.QSpinBox()
        br_vbox.addWidget(self.breathing_reminder_length_qsb)
        self.breathing_reminder_length_qsb.valueChanged.connect(
            self.on_breathing_length_value_changed
        )
        self.breathing_reminder_test_qpb = QtWidgets.QPushButton("Test")
        br_vbox.addWidget(self.breathing_reminder_test_qpb)
        self.breathing_reminder_test_qpb.clicked.connect(self.on_breathing_test_clicked)

        vbox.addStretch(1)

        self.breathing_reminder_qgb.setDisabled(True)  # -disabled until a phrase has been selected

        self.update_gui()

    def on_breathing_test_clicked(self):
        self.breathing_test_button_clicked_signal.emit()

    def on_breathing_active_toggled(self, i_checked_bool):
        if self.updating_gui_bool:
            return
        self.breathing_reminder_interval_qsb.setDisabled(not i_checked_bool)
        self.breathing_reminder_length_qsb.setDisabled(not i_checked_bool)
        self.breathing_reminder_test_qpb.setDisabled(not i_checked_bool)
        model.SettingsM.update_breathing_reminder_active(i_checked_bool)
        self.breathing_settings_updated_signal.emit()

    def on_breathing_interval_value_changed(self, i_new_value: int):
        if self.updating_gui_bool:
            return
        model.SettingsM.update_breathing_reminder_interval(i_new_value)
        self.breathing_settings_updated_signal.emit()

    def on_breathing_length_value_changed(self, i_new_value: int):
        if self.updating_gui_bool:
            return
        model.SettingsM.update_breathing_reminder_length(i_new_value)
        self.breathing_settings_updated_signal.emit()


    def update_gui(self):
        self.updating_gui_bool = True

        # Breathing reminder
        if mc_global.active_phrase_id_it != mc_global.NO_PHRASE_SELECTED_INT:
            self.breathing_reminder_qgb.setDisabled(False)
        self.breathing_reminder_enabled_qcb.setChecked(
            model.SettingsM.get().breathing_reminder_active_bool
        )
        breathing_reminder_interval_minutes_int = model.SettingsM.get().breathing_reminder_interval_int
        self.breathing_reminder_interval_qsb.setValue(breathing_reminder_interval_minutes_int)
        breathing_reminder_length_minutes_int = model.SettingsM.get().breathing_reminder_length_int
        self.breathing_reminder_length_qsb.setValue(breathing_reminder_length_minutes_int)

        self.updating_gui_bool = False

