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

        self.test_breathing_dialog_qpb = QtWidgets.QPushButton("Test breathing dialog")
        vbox_l2.addWidget(self.test_breathing_dialog_qpb)
        self.test_breathing_dialog_qpb.clicked.connect(self.on_test_breathing_dialog_button_clicked)

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

        vbox_l2.addStretch(1)

        # self.breathing_reminder_qgb.setDisabled(True)  # -disabled until a phrase has been selected
        self.setDisabled(True)

        self.update_gui()

    def on_test_breathing_dialog_button_clicked(self):
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
            breathing_phrase = mc.model.PhrasesM.get(mc_global.active_phrase_id_it)
            self.title_text_qll.setText(breathing_phrase.title_str)
            self.in_text_qll.setText(breathing_phrase.ib_str)
            self.out_text_qll.setText(breathing_phrase.ob_str)
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
