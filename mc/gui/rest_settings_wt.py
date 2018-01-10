import os
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import mc.gui.toggle_switch_wt
import mc.model
import mc.mc_global

MIN_REST_REMINDER_INT = 1  # -in minutes
MAX_REST_REMINDER_INT = 99
NO_AUDIO_SELECTED_STR = "No audio selected"


class RestSettingsWt(QtWidgets.QWidget):
    settings_updated_signal = QtCore.pyqtSignal()
    rest_now_button_clicked_signal = QtCore.pyqtSignal()
    rest_reset_button_clicked_signal = QtCore.pyqtSignal()
    rest_slider_value_changed_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.updating_gui_bool = False

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.rest_reminder_switch = mc.gui.toggle_switch_wt.ToggleSwitchWt()
        vbox_l2.addWidget(self.rest_reminder_switch)
        self.rest_reminder_switch.toggled_signal.connect(self.on_switch_toggled)

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        hbox_l3.addWidget(QtWidgets.QLabel(self.tr("Interval:")))
        self.rest_reminder_interval_qsb = QtWidgets.QSpinBox()
        hbox_l3.addWidget(self.rest_reminder_interval_qsb)
        hbox_l3.addWidget(QtWidgets.QLabel(self.tr("minutes")))
        hbox_l3.addStretch(1)
        self.rest_reminder_interval_qsb.setMinimum(MIN_REST_REMINDER_INT)
        self.rest_reminder_interval_qsb.setMaximum(MAX_REST_REMINDER_INT)
        self.rest_reminder_interval_qsb.valueChanged.connect(self.on_rest_interval_value_changed)
        vbox_l2.addWidget(QtWidgets.QLabel(self.tr("Time until next break:")))

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        self.rest_reminder_qsr = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)  # .QProgressBar()
        hbox_l3.addWidget(self.rest_reminder_qsr)
        self.rest_reminder_qsr.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.rest_reminder_qsr.valueChanged.connect(self.on_rest_reminder_slider_value_changed)
        self.rest_reminder_qsr.setPageStep(5)

        self.rest_reminder_reset_qpb = QtWidgets.QPushButton()  # -"Reset timer"
        self.rest_reminder_reset_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("reload-2x.png")))
        self.rest_reminder_reset_qpb.setToolTip(self.tr("Reset the rest timer"))
        self.rest_reminder_reset_qpb.clicked.connect(self.on_rest_reset_clicked)
        hbox_l3.addWidget(self.rest_reminder_reset_qpb)

        """
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        vbox_l2.addWidget(self.slider)
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
        # vbox_l2.addWidget(CustomFrame())
        self.rest_reminder_test_qpb = QtWidgets.QPushButton(self.tr("Take a break now"))  # -from the computer
        vbox_l2.addWidget(self.rest_reminder_test_qpb)
        self.rest_reminder_test_qpb.clicked.connect(self.on_rest_test_clicked)


        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        hbox_l3.addWidget(QtWidgets.QLabel(self.tr("Notification type: ")))
        hbox_l3.addStretch(1)
        self.notification_type_qcb = QtWidgets.QComboBox()
        hbox_l3.addWidget(self.notification_type_qcb)
        self.notification_type_qcb.addItems([
            mc.mc_global.NotificationType.Visual.name,
            mc.mc_global.NotificationType.Audio.name,
            mc.mc_global.NotificationType.Both.name
        ])
        self.notification_type_qcb.activated.connect(self.on_notification_type_activated)


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

        # vbox_l2.addWidget(QtWidgets.QLabel("<i>All changes are automatically saved</i>"))

        self.update_gui()

    def on_notification_type_activated(self, i_index: int):
        # -activated is only triggered on user action
        mc.model.SettingsM.update_rest_reminder_notification_type(i_index)

    def volume_changed(self, i_value: int):
        if self.updating_gui_bool:
            return
        # Prev: mc.model.SettingsM.update_rest_reminder_volume(i_value)
        mc.model.SettingsM.get().rest_reminder_volume = i_value

    def on_select_audio_clicked(self):
        # noinspection PyCallByClass
        audio_file_result_tuple = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Please choose a wav audio file"),
            mc.mc_global.get_user_audio_path(),
            self.tr("Wav files (*.wav)")
        )
        new_file_path_str = audio_file_result_tuple[0]
        if new_file_path_str:
            mc.model.SettingsM.get().rest_reminder_audio_path = new_file_path_str
        else:
            pass
        self.update_gui_audio_details()

    def update_gui_audio_details(self):
        self.updating_gui_bool = True
        settings = mc.model.SettingsM.get()

        audio_path_str = settings.rest_reminder_audio_path_str
        audio_file_name_str = os.path.basename(audio_path_str)
        if audio_file_name_str:
            self.audio_path_qll.setText(audio_file_name_str)
        else:
            self.audio_path_qll.setText(NO_AUDIO_SELECTED_STR)

        self.volume_qsr.setValue(settings.rest_reminder_volume_int)

        self.updating_gui_bool = False

    def on_rest_reminder_slider_value_changed(self, i_new_value: int):
        if self.updating_gui_bool:
            return
        mc.mc_global.rest_reminder_minutes_passed_int = i_new_value
        self.rest_slider_value_changed_signal.emit()

    def on_rest_reset_clicked(self):
        self.rest_reset_button_clicked_signal.emit()

    def on_rest_test_clicked(self):
        self.rest_now_button_clicked_signal.emit()

    def on_switch_toggled(self, i_checked_bool):
        if self.updating_gui_bool:
            return
        mc.model.SettingsM.get().rest_reminder_active = i_checked_bool

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

        settings = mc.model.SettingsM.get()

        # Rest reminder
        rr_enabled = mc.model.SettingsM.get().rest_reminder_active
        self.rest_reminder_switch.update_gui(rr_enabled)
        interval_minutes_int = mc.model.SettingsM.get().rest_reminder_interval_int
        self.rest_reminder_interval_qsb.setValue(interval_minutes_int)
        self.rest_reminder_qsr.setMinimum(0)
        self.rest_reminder_qsr.setMaximum(interval_minutes_int)
        self.rest_reminder_qsr.setValue(mc.mc_global.rest_reminder_minutes_passed_int)

        self.update_gui_audio_details()

        rest_notification_type_enum = mc.mc_global.NotificationType(
            settings.rest_reminder_notification_type_int
        )
        self.notification_type_qcb.setCurrentText(rest_notification_type_enum.name)

        self.updating_gui_bool = False
