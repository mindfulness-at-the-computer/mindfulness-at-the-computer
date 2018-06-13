import os
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from mc import mc_global
import mc.model
from mc.gui.toggle_switch_wt import ToggleSwitchWt
from mc.gui.rest_action_list_wt import RestActionListWt
from mc.gui.reusable_components import PageGrid, H2, HorizontalLine, RadioButtonLeft, RadioButtonMiddle, \
    RadioButtonRight, H1

NO_AUDIO_SELECTED_STR = "No audio selected"


class RestSettingsWt(QtWidgets.QWidget):
    settings_updated_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.updating_gui_bool = False

        self.toggle_switch = ToggleSwitchWt()
        self.both_qrb = RadioButtonLeft(self.tr("Visual + Audio"))
        self.visual_qrb = RadioButtonMiddle(self.tr("Visual"))
        self.audio_qrb = RadioButtonRight(self.tr("Audio"))
        self.notification_interval_qsb = QtWidgets.QSpinBox()
        self.notif_select_audio_qpb = QtWidgets.QPushButton(self.tr("Select audio"))
        self.notif_volume_qsr = QtWidgets.QSlider()

        self.phrases_qlw = RestActionListWt()

        self._init_ui()
        self._connect_slots_to_signals()

    def _init_ui(self):
        settings = mc.model.SettingsM.get()

        # initializing the values of the controls
        if settings.rest_reminder_notification_type == mc_global.NotificationType.Audio:
            self.audio_qrb.setChecked(True)
        if settings.rest_reminder_notification_type == mc_global.NotificationType.Visual:
            self.visual_qrb.setChecked(True)
        if settings.rest_reminder_notification_type == mc_global.NotificationType.Both:
            self.both_qrb.setChecked(True)
        self.toggle_switch.turn_on_off_qcb.setChecked(settings.rest_reminder_active_bool)
        self.notif_select_audio_qpb.setObjectName("notif_select_audio_qpb")

        # Notification settings
        notification_type_grid = PageGrid()
        notification_type_grid.setColumnMinimumWidth(0, 120)
        notification_type_grid.setColumnMinimumWidth(1, 120)
        notification_type_grid.setColumnMinimumWidth(2, 125)
        notification_type_grid.setColumnStretch(3, 1)
        notification_type_grid.addWidget(self.both_qrb, 0, 0)
        notification_type_grid.addWidget(self.visual_qrb, 0, 1)
        notification_type_grid.addWidget(self.audio_qrb, 0, 2)
        notification_type_grid.setSpacing(0)
        notification_type_qgb = QtWidgets.QGroupBox()
        notification_type_qgb.setStyleSheet("border: none;")
        notification_type_qgb.setLayout(notification_type_grid)

        # Settings for audio
        self.notif_volume_qsr.setOrientation(QtCore.Qt.Horizontal)
        self.notif_volume_qsr.setMinimum(0)
        self.notif_volume_qsr.setMaximum(100)
        audio_qhl = QtWidgets.QHBoxLayout()
        audio_qhl.addWidget(self.notif_select_audio_qpb)
        audio_qhl.addWidget(self.notif_volume_qsr)

        # PUT EVERYTHING ON THE PAGE......
        grid = PageGrid()

        # first grid column
        grid.addWidget(self.toggle_switch, 0, 0)
        grid.addWidget(H2(self.tr("Notifications")), 1, 0)
        grid.addWidget(HorizontalLine(), 2, 0)
        grid.addWidget(QtWidgets.QLabel(self.tr("Notification type")), 3, 0)
        grid.addWidget(notification_type_qgb, 4, 0)
        grid.addWidget(QtWidgets.QLabel(), 5, 0)
        grid.addWidget(H2(self.tr("Audio")), 6, 0)
        grid.addWidget(HorizontalLine(), 7, 0)
        grid.addLayout(audio_qhl, 8, 0)

        # second grid column
        grid.addWidget(self.phrases_qlw, 0, 8, 20, 1)

        vbox_l2 = QtWidgets.QVBoxLayout()
        vbox_l2.addWidget(H1(self.tr("Settings for Resting")))
        vbox_l2.addWidget(HorizontalLine())
        vbox_l2.addStretch(1)
        vbox_l2.addLayout(grid)
        vbox_l2.addStretch(3)
        self.setLayout(vbox_l2)

        self.update_gui()

    def _connect_slots_to_signals(self):
        self.toggle_switch.toggled_signal.connect(self.on_switch_toggled)
        self.audio_qrb.clicked.connect(self.on_notification_type_audio_activated)
        self.visual_qrb.clicked.connect(self.on_notification_type_visual_activated)
        self.both_qrb.clicked.connect(self.on_notification_type_both_activated)
        self.notif_select_audio_qpb.clicked.connect(self.on_select_audio_clicked)
        self.notif_volume_qsr.valueChanged.connect(self.volume_changed)

    def on_notification_type_audio_activated(self, i_index: int):
        print('on notification type audio activated works')
        print(mc_global.NotificationType.Audio.value)
        # -activated is only triggered on user action
        mc.model.SettingsM.update_rest_reminder_notification_type(mc_global.NotificationType.Audio.value)

    def on_notification_type_visual_activated(self, i_index: int):
        print('on notification type visual activated works')
        print(mc_global.NotificationType.Visual.value)
        # -activated is only triggered on user action
        mc.model.SettingsM.update_rest_reminder_notification_type(mc_global.NotificationType.Visual.value)

    def on_notification_type_both_activated(self, i_index: int):
        print('on notification type audio activated works')
        print(mc_global.NotificationType.Both.value)
        # -activated is only triggered on user action
        mc.model.SettingsM.update_rest_reminder_notification_type(mc_global.NotificationType.Both.value)

    def volume_changed(self, i_value: int):
        print('rest volume changed')
        if self.updating_gui_bool:
            return
        mc.model.SettingsM.get().rest_reminder_volume = i_value
        # -prev: mc.model.SettingsM.update_rest_reminder_volume(i_value)

    def on_select_audio_clicked(self):
        print('select rest audio clicked')
        # noinspection PyCallByClass
        audio_file_result_tuple = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Please choose a wav audio file"),
            mc.mc_global.get_user_audio_path(),
            self.tr("Wav files (*.wav)")
        )
        new_file_path_str = audio_file_result_tuple[0]
        if new_file_path_str:
            new_filename_str = os.path.basename(new_file_path_str)  # -we store the name instead of the path
            mc.model.SettingsM.get().rest_reminder_audio_filename = new_filename_str
        else:
            pass
        self.update_gui_audio_details()

    def update_gui_audio_details(self):
        self.updating_gui_bool = True
        settings = mc.model.SettingsM.get()

        audio_path_str = settings.rest_reminder_audio_filename_str
        audio_file_name_str = os.path.basename(audio_path_str)
        if audio_file_name_str:
            self.notif_select_audio_qpb.setText(audio_file_name_str)
        else:
            self.notif_select_audio_qpb.setText(NO_AUDIO_SELECTED_STR)

        self.notif_volume_qsr.setValue(settings.rest_reminder_volume_int)

        self.updating_gui_bool = False

    def on_switch_toggled(self, i_checked_bool):
        if self.updating_gui_bool:
            return
        mc.model.SettingsM.get().rest_reminder_active = i_checked_bool

        self.settings_updated_signal.emit()

    def update_gui(self):
        self.updating_gui_bool = True

        # Rest reminder
        rr_enabled = mc.model.SettingsM.get().rest_reminder_active
        self.toggle_switch.update_gui(rr_enabled)

        self.update_gui_audio_details()
        self.updating_gui_bool = False
