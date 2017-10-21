from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from mc import model, mc_global

import mc.gui.toggle_switch_widget

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

        self.toggle_switch = mc.gui.toggle_switch_widget.ToggleSwitchComposite()
        vbox.addWidget(self.toggle_switch)
        self.toggle_switch.toggled_signal.connect(self.on_switch_toggled)

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        self.breathing_reminder_interval_qll = QtWidgets.QLabel("Interval:")
        hbox.addWidget(self.breathing_reminder_interval_qll)
        self.breathing_reminder_interval_qsb = QtWidgets.QSpinBox()
        hbox.addWidget(self.breathing_reminder_interval_qsb)
        self.breathing_reminder_interval_qsb.valueChanged.connect(
            self.on_breathing_interval_value_changed
        )
        hbox.addWidget(QtWidgets.QLabel("seconds"))
        hbox.addStretch(1)

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        self.breathing_reminder_length_qll = QtWidgets.QLabel("Length:")
        hbox.addWidget(self.breathing_reminder_length_qll)
        self.breathing_reminder_length_qsb = QtWidgets.QSpinBox()
        hbox.addWidget(self.breathing_reminder_length_qsb)
        self.breathing_reminder_length_qsb.valueChanged.connect(
            self.on_breathing_length_value_changed
        )
        hbox.addWidget(QtWidgets.QLabel("seconds"))
        """
        self.presets_qcb = QtWidgets.QComboBox()
        self.presets_qcb.addItems(["30", "45", "60", "90"])
        hbox.addWidget(self.presets_qcb)
        """

        hbox.addStretch(1)

        self.breathing_reminder_test_qpb = QtWidgets.QPushButton("Test")
        vbox.addWidget(self.breathing_reminder_test_qpb)
        self.breathing_reminder_test_qpb.clicked.connect(self.on_breathing_test_clicked)

        vbox.addStretch(1)


        # self.breathing_reminder_qgb.setDisabled(True)  # -disabled until a phrase has been selected
        self.setDisabled(True)

        self.update_gui()

    def on_breathing_test_clicked(self):
        self.breathing_test_button_clicked_signal.emit()

    def on_switch_toggled(self, i_checked_bool):
        if self.updating_gui_bool:
            return
        model.SettingsM.update_breathing_reminder_active(i_checked_bool)
        mc_global.update_tray_breathing_checked(i_checked_bool)
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
            self.setDisabled(False)
            mc_global.update_tray_breathing_enabled(True)
        else:
            self.setDisabled(True)
            mc_global.update_tray_breathing_enabled(False)

        br_enabled = model.SettingsM.get().breathing_reminder_active_bool
        self.toggle_switch.update_gui(br_enabled)

        breathing_reminder_interval_minutes_int = model.SettingsM.get().breathing_reminder_interval_int
        self.breathing_reminder_interval_qsb.setValue(breathing_reminder_interval_minutes_int)
        breathing_reminder_length_minutes_int = model.SettingsM.get().breathing_reminder_length_int
        self.breathing_reminder_length_qsb.setValue(breathing_reminder_length_minutes_int)

        self.updating_gui_bool = False

