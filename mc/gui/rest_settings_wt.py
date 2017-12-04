from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import mc.gui.toggle_switch_wt
import mc.model
import mc.mc_global

MIN_REST_REMINDER_INT = 1  # -in minutes
MAX_REST_REMINDER_INT = 99


class RestSettingsWt(QtWidgets.QWidget):
    settings_updated_signal = QtCore.pyqtSignal()
    rest_test_button_clicked_signal = QtCore.pyqtSignal()
    rest_reset_button_clicked_signal = QtCore.pyqtSignal()
    rest_slider_value_changed_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.updating_gui_bool = False

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        self.rest_reminder_switch = mc.gui.toggle_switch_wt.ToggleSwitchWt()
        vbox.addWidget(self.rest_reminder_switch)
        self.rest_reminder_switch.toggled_signal.connect(self.on_switch_toggled)

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addWidget(QtWidgets.QLabel("Interval:"))
        self.rest_reminder_interval_qsb = QtWidgets.QSpinBox()
        hbox.addWidget(self.rest_reminder_interval_qsb)
        hbox.addWidget(QtWidgets.QLabel("minutes"))
        hbox.addStretch(1)
        self.rest_reminder_interval_qsb.setMinimum(MIN_REST_REMINDER_INT)
        self.rest_reminder_interval_qsb.setMaximum(MAX_REST_REMINDER_INT)
        self.rest_reminder_interval_qsb.valueChanged.connect(self.on_rest_interval_value_changed)
        vbox.addWidget(QtWidgets.QLabel("Time until next break:"))

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        self.rest_reminder_qsr = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)  # .QProgressBar()
        hbox.addWidget(self.rest_reminder_qsr)
        self.rest_reminder_qsr.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.rest_reminder_qsr.valueChanged.connect(self.on_rest_reminder_slider_value_changed)
        self.rest_reminder_qsr.setPageStep(5)
        self.rest_reminder_reset_qpb = QtWidgets.QPushButton()  # -"Reset timer"
        hbox.addWidget(self.rest_reminder_reset_qpb)
        self.rest_reminder_reset_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("reload-2x.png")))
        self.rest_reminder_reset_qpb.clicked.connect(self.on_rest_reset_clicked)

        """
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        vbox.addWidget(self.slider)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.setValue(20)
        """
        # self.rest_reminder_qprb.set
        # self.rest_reminder_qprb.setTextVisible(False)
        """
        base_qcolor = QtGui.QColor(41, 163, 41, 0)
        base_qpalette = QtGui.QPalette()
        base_qpalette.setColor(QtGui.QPalette.Base, base_qcolor)
        self.rest_reminder_qprb.setPalette(base_qpalette)
        """
        # self.rest_reminder_qprb.setStyleSheet("background-color: #f4fde7;")

        # Take break button
        # vbox.addWidget(CustomFrame())
        self.rest_reminder_test_qpb = QtWidgets.QPushButton("Take a break now")  # -from the computer
        vbox.addWidget(self.rest_reminder_test_qpb)
        self.rest_reminder_test_qpb.clicked.connect(self.on_rest_test_clicked)

        vbox.addStretch(1)
        
        # vbox.addWidget(QtWidgets.QLabel("<i>All changes are automatically saved</i>"))

        self.update_gui()

    def on_rest_reminder_slider_value_changed(self, i_new_value: int):
        if self.updating_gui_bool:
            return
        mc.mc_global.rest_reminder_minutes_passed_int = i_new_value
        self.rest_slider_value_changed_signal.emit()

    def on_rest_reset_clicked(self):
        self.rest_reset_button_clicked_signal.emit()

    def on_rest_test_clicked(self):
        self.rest_test_button_clicked_signal.emit()

    def on_switch_toggled(self, i_checked_bool):
        if self.updating_gui_bool:
            return
        mc.model.SettingsM.update_rest_reminder_active(i_checked_bool)
        self.settings_updated_signal.emit()

    def on_rest_interval_value_changed(self, i_new_value: int):
        # -PLEASE NOTE: During debug this event is fired twice, this must be a bug in Qt or PyQt
        # (there is no problem when running normally, that is without debug)
        if self.updating_gui_bool:
            return
        # mc_global.rest_reminder_minutes_remaining_int = i_new_value
        mc.model.SettingsM.update_rest_reminder_interval(i_new_value)

        rest_reminder_interval_minutes_int = mc.model.SettingsM.get().rest_reminder_interval_int
        self.rest_reminder_qsr.setMinimum(0)
        self.rest_reminder_qsr.setMaximum(rest_reminder_interval_minutes_int)
        self.rest_reminder_qsr.setValue(mc.mc_global.rest_reminder_minutes_passed_int)

        self.settings_updated_signal.emit()

    def update_gui(self):
        self.updating_gui_bool = True

        # Rest reminder
        rr_enabled = mc.model.SettingsM.get().rest_reminder_active_bool
        self.rest_reminder_switch.update_gui(rr_enabled)
        interval_minutes_int = mc.model.SettingsM.get().rest_reminder_interval_int
        self.rest_reminder_interval_qsb.setValue(interval_minutes_int)
        self.rest_reminder_qsr.setMinimum(0)
        self.rest_reminder_qsr.setMaximum(interval_minutes_int)
        self.rest_reminder_qsr.setValue(mc.mc_global.rest_reminder_minutes_passed_int)

        self.updating_gui_bool = False
