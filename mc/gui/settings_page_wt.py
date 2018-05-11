import mc.mc_global
import mc.model
from PyQt5 import QtWidgets, QtCore
from mc.gui.reusable_components import *


class SettingsPageWt(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self.breathing_settings_wt = BreathingSettingsWt()
        self.resting_settings_wt = RestingSettingsWt()
        self._init_ui()

    def _init_ui(self):
        self.setGeometry(100, 64, 900, 670)

        self.setTabPosition(self.West)

        self.addTab(self.breathing_settings_wt, self.tr("Breathing"))
        self.addTab(self.resting_settings_wt, self.tr("Resting"))


class BreathingSettingsWt(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.turn_breathing_on_off_qcb = QtWidgets.QCheckBox()
        self.both_qrb = RadioButtonLeft(self.tr("Visual + Audio"))
        self.visual_qrb = RadioButtonMiddle(self.tr("Visual"))
        self.audio_qrb = RadioButtonRight(self.tr("Audio"))
        self.notification_interval_qsb = QtWidgets.QSpinBox()
        self.close_on_hover_qcb = QtWidgets.QCheckBox()
        self.same_qrb = RadioButtonLeft(self.tr("Same"))
        self.random_qrb = RadioButtonRight(self.tr("Random"))
        self.show_after_qsb = QtWidgets.QSpinBox()
        self.notif_select_audio_qpb = QtWidgets.QPushButton(self.tr("Select audio"))
        self.notif_volume_qsr = QtWidgets.QSlider()

        self._init_ui()

    def _init_ui(self):
        settings = mc.model.SettingsM.get()

        # initializing the values of the controls
        self.turn_breathing_on_off_qcb.setChecked(settings.breathing_reminder_active_bool)
        self.close_on_hover_qcb.setChecked(settings.breathing_reminder_dialog_audio_active_bool)
        self.notif_select_audio_qpb.setObjectName("notif_select_audio_qpb")

        # General settings
        on_off_qhl = QtWidgets.QHBoxLayout()
        on_off_qhl.addWidget(QtWidgets.QLabel(self.tr("Turn the breathing dialog and notifications on or off")))
        on_off_qhl.addStretch(1)
        on_off_qhl.addWidget(self.turn_breathing_on_off_qcb)

        notification_type_qhl = QtWidgets.QGridLayout()
        notification_type_qhl.setColumnMinimumWidth(0, 120)
        notification_type_qhl.setColumnMinimumWidth(1, 120)
        notification_type_qhl.setColumnMinimumWidth(2, 120)
        notification_type_qhl.setColumnStretch(3, 1)
        notification_type_qhl.addWidget(self.both_qrb, 0, 0)
        notification_type_qhl.addWidget(self.visual_qrb, 0, 1)
        notification_type_qhl.addWidget(self.audio_qrb, 0, 2)
        notification_type_qhl.setSpacing(0)
        notification_type_qgb = QtWidgets.QGroupBox()
        notification_type_qgb.setLayout(notification_type_qhl)

        notification_interval_qhl = QtWidgets.QHBoxLayout()
        notification_interval_qhl.addWidget(QtWidgets.QLabel(self.tr("Interval every:")))
        notification_interval_qhl.addWidget(self.notification_interval_qsb)
        notification_interval_qhl.addWidget(QtWidgets.QLabel(self.tr("minutes")))
        notification_interval_qhl.addStretch(1)

        # Settings for the breathing dialog
        dialog_qhl = QtWidgets.QHBoxLayout()
        dialog_qhl.addWidget(H2(self.tr("Dialog")))
        dialog_qhl.addStretch(1)
        dialog_qhl.addWidget(QtWidgets.QLabel(self.tr("Close on hover")))
        dialog_qhl.addWidget(self.close_on_hover_qcb)
        dialog_qhl.setSpacing(20)

        dialog_type_qhl = QtWidgets.QGridLayout()
        dialog_type_qhl.setColumnMinimumWidth(0, 120)
        dialog_type_qhl.setColumnMinimumWidth(1, 120)
        dialog_type_qhl.setColumnStretch(2, 1)
        dialog_type_qhl.addWidget(self.same_qrb, 0, 0)
        dialog_type_qhl.addWidget(self.random_qrb, 0, 1)
        dialog_type_qhl.setSpacing(0)
        dialog_type_qgb = QtWidgets.QGroupBox()
        dialog_type_qgb.setLayout(dialog_type_qhl)

        show_after_qhl = QtWidgets.QHBoxLayout()
        show_after_qhl.addWidget(QtWidgets.QLabel(self.tr("Show after:")))
        show_after_qhl.addWidget(self.show_after_qsb)
        show_after_qhl.addWidget(QtWidgets.QLabel(self.tr("notifications")))
        show_after_qhl.addStretch(1)

        # Settings for audio
        self.notif_volume_qsr.setOrientation(QtCore.Qt.Horizontal)
        self.notif_volume_qsr.setMinimum(0)
        self.notif_volume_qsr.setMaximum(100)
        audio_qhl = QtWidgets.QHBoxLayout()
        audio_qhl.addWidget(self.notif_select_audio_qpb)
        audio_qhl.addWidget(self.notif_volume_qsr)

        # PUT EVERYTHING ON THE PAGE......
        grid = QtWidgets.QGridLayout()

        # first grid column
        grid.addLayout(on_off_qhl, 0, 0)
        grid.addWidget(H2(self.tr("Notifications")), 2, 0)
        grid.addWidget(RaisedHorizontalLine(), 3, 0)
        grid.addWidget(QtWidgets.QLabel(self.tr("Notification type")), 4, 0)
        grid.addWidget(notification_type_qgb, 5, 0)
        grid.addWidget(SunkenHorizontalLine(), 6, 0)
        grid.addLayout(notification_interval_qhl, 7, 0)
        grid.addWidget(QtWidgets.QLabel(), 8, 0)
        grid.addLayout(dialog_qhl, 9, 0)
        grid.addWidget(RaisedHorizontalLine(), 10, 0)
        grid.addWidget(QtWidgets.QLabel(self.tr("Do you always want the same phrase or a random one?")), 11, 0)
        grid.addWidget(dialog_type_qgb, 12, 0)
        grid.addWidget(SunkenHorizontalLine(), 13, 0)
        grid.addLayout(show_after_qhl, 14, 0)
        grid.addWidget(QtWidgets.QLabel(), 15, 1)
        grid.addWidget(H2(self.tr("Audio")), 16, 0)
        grid.addWidget(RaisedHorizontalLine(), 17, 0)
        grid.addLayout(audio_qhl, 18, 0)

        # second grid column
        grid.addWidget(QtWidgets.QLabel(self.tr("These are the sentences that appear in the `breathing dialog`")), 0, 2)
        grid.addWidget(QtWidgets.QLabel(self.tr("They also appear in the `breathing notification`")), 1, 2)

        vbox_l2 = QtWidgets.QVBoxLayout()
        vbox_l2.addWidget(H1(self.tr("Settings for Breathing")))
        vbox_l2.addWidget(SunkenHorizontalLine())
        vbox_l2.addStretch(1)
        vbox_l2.addLayout(grid)
        vbox_l2.addStretch(3)
        self.setLayout(vbox_l2)


class RestingSettingsWt(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
