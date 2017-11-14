from PyQt5 import QtCore
from PyQt5 import QtWidgets
from mc import model, mc_global
import mc.gui.toggle_switch_widget

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

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.toggle_switch = mc.gui.toggle_switch_widget.ToggleSwitchComposite()
        vbox_l2.addWidget(self.toggle_switch)
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

        vbox_l2.addStretch(1)

        # self.breathing_reminder_qgb.setDisabled(True)  # -disabled until a phrase has been selected
        self.setDisabled(True)

        self.update_gui()

    def on_breathing_test_clicked(self):
        self.breathing_test_button_clicked_signal.emit()

    def on_switch_toggled(self, i_checked_bool):
        if self.updating_gui_bool:
            return
        model.SettingsM.update_breathing_reminder_active(i_checked_bool)
        self.breathing_settings_updated_signal.emit()

    def on_breathing_interval_value_changed(self, i_new_value: int):
        if self.updating_gui_bool:
            return
        model.SettingsM.update_breathing_reminder_interval(i_new_value)
        self.breathing_settings_updated_signal.emit()

    def update_gui(self):
        self.updating_gui_bool = True

        # Breathing reminder
        if mc_global.active_phrase_id_it != mc_global.NO_PHRASE_SELECTED_INT:
            self.setDisabled(False)
        else:
            self.setDisabled(True)

        br_enabled = model.SettingsM.get().breathing_reminder_active_bool
        self.toggle_switch.update_gui(br_enabled)

        breathing_reminder_interval_minutes_int = model.SettingsM.get().breathing_reminder_interval_int
        self.breathing_reminder_interval_qsb.setValue(breathing_reminder_interval_minutes_int)
        """
        breathing_reminder_length_minutes_int = model.SettingsM.get().breathing_reminder_length_int
        self.breathing_reminder_length_qsb.setValue(breathing_reminder_length_minutes_int)
        """

        self.updating_gui_bool = False
