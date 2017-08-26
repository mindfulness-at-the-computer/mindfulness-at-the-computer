import logging
import sys
import functools
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import mb_global
import mb_model
import mb_breathing
import mb_phrase_list


# Here we place settings for the application, for example the time between notifications,
# as well as if there is audio as well as the notification
# Perhaps we want to hide some of these settings?
# All intervals are in minutes

MIN_REST_REMINDER_INT = 1  # -in minutes


class SettingsComposite(QtWidgets.QWidget):
    settings_updated_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.updating_gui_bool = False

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        self.rest_reminder_enabled_qcb = QtWidgets.QCheckBox("Rest reminder")
        vbox.addWidget(self.rest_reminder_enabled_qcb)
        self.rest_reminder_interval_qsb = QtWidgets.QSpinBox()
        vbox.addWidget(self.rest_reminder_interval_qsb)
        self.rest_reminder_interval_qsb.setMinimum(MIN_REST_REMINDER_INT)
        self.rest_reminder_interval_qsb.valueChanged.connect(self.on_rest_interval_value_changed)

        self.update_gui()

    def on_rest_interval_value_changed(self, i_new_value: int):
        # -PLEASE NOTE: During debug this event is fired twice, this must be a bug in Qt or PyQt
        # (there is no problem when running normally, that is without debug)
        if self.updating_gui_bool:
            return
        new_interval_minutes_int = self.rest_reminder_interval_qsb.value()

        mb_model.SettingsM.update_rest_reminder_interval(i_new_value)

        self.settings_updated_signal.emit()

    def update_gui(self):
        self.updating_gui_bool = True

        rest_reminder_interval_minutes_int = mb_model.SettingsM.get().rest_reminder_interval_int
        self.rest_reminder_interval_qsb.setValue(rest_reminder_interval_minutes_int)

        self.updating_gui_bool = False
