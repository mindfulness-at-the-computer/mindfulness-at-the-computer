import mc.mc_global
import mc.model
from PyQt5 import QtWidgets, QtCore
from mc.gui.reusable_components import H1, H2, SunkenHorizontalLine, RaisedHorizontalLine


class SettingsPageWt(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self.breathing_settings_wt = QtWidgets.QWidget()
        self.turn_breathing_on_off_qcb = QtWidgets.QCheckBox()
        self.breathing_reminder_interval_qsb = QtWidgets.QSpinBox()
        self.show_after_qsb = QtWidgets.QSpinBox()
        self.close_on_hover_qcb = QtWidgets.QCheckBox()
        self.notif_select_audio_qpb = QtWidgets.QPushButton(self.tr("Select audio"))
        self.notif_volume_qsr = QtWidgets.QSlider()

        self._init_ui()

    def _init_ui(self):
        settings = mc.model.SettingsM.get()
        self.setGeometry(100, 64, 900, 670)

        self.setTabPosition(self.West)
        self.addTab(self.breathing_settings_wt, self.tr("Breathing"))

        # initializing the values of the controls
        self.turn_breathing_on_off_qcb.setChecked(settings.breathing_reminder_active_bool)
        self.close_on_hover_qcb.setChecked(settings.breathing_reminder_dialog_audio_active_bool)
        self.notif_select_audio_qpb.setObjectName("notif_select_audio_qpb")

        # Setting up the radio buttons for the notification type
        both_qrb = QtWidgets.QRadioButton()
        both_qrb.setObjectName("both_qrb")

        visual_qrb = QtWidgets.QRadioButton()
        visual_qrb.setObjectName("visual_qrb")

        audio_qrb = QtWidgets.QRadioButton()
        audio_qrb.setObjectName("audio_qrb")

        same_qrb = QtWidgets.QRadioButton()
        same_qrb.setObjectName("same_qrb")

        random_qrb = QtWidgets.QRadioButton()
        random_qrb.setObjectName("random_qrb")

        on_off_qhl = QtWidgets.QHBoxLayout()
        on_off_qhl.addWidget(QtWidgets.QLabel(self.tr("Turn the breathing dialog and notifications on or off")))
        on_off_qhl.addStretch(1)
        on_off_qhl.addWidget(self.turn_breathing_on_off_qcb)

        notification_type_qhl = QtWidgets.QHBoxLayout()
        notification_type_qhl.addWidget(both_qrb)
        notification_type_qhl.addWidget(visual_qrb)
        notification_type_qhl.addWidget(audio_qrb)
        notification_type_qhl.setSpacing(0)
        notification_type_qhl.addStretch(1)
        notification_type_qgb = QtWidgets.QGroupBox()
        notification_type_qgb.setLayout(notification_type_qhl)

        dialog_type_qhl = QtWidgets.QHBoxLayout()
        dialog_type_qhl.addWidget(same_qrb)
        dialog_type_qhl.addWidget(random_qrb)
        dialog_type_qhl.setSpacing(0)
        dialog_type_qhl.addStretch(1)
        dialog_type_qgb = QtWidgets.QGroupBox()
        dialog_type_qgb.setLayout(dialog_type_qhl)

        breathing_reminder_interval_qhl = QtWidgets.QHBoxLayout()
        breathing_reminder_interval_qhl.addWidget(QtWidgets.QLabel(self.tr("Interval every:")))
        breathing_reminder_interval_qhl.addWidget(self.breathing_reminder_interval_qsb)
        breathing_reminder_interval_qhl.addWidget(QtWidgets.QLabel(self.tr("minutes")))
        breathing_reminder_interval_qhl.addStretch(1)

        show_after_qhl = QtWidgets.QHBoxLayout()
        show_after_qhl.addWidget(QtWidgets.QLabel(self.tr("Show after:")))
        show_after_qhl.addWidget(self.show_after_qsb)
        show_after_qhl.addWidget(QtWidgets.QLabel(self.tr("notifications")))
        show_after_qhl.addStretch(1)

        dialog_qhl = QtWidgets.QHBoxLayout()
        dialog_qhl.addWidget(H2(self.tr("Dialog")))
        dialog_qhl.addStretch(1)
        dialog_qhl.addWidget(QtWidgets.QLabel(self.tr("Close on hover")))
        dialog_qhl.addWidget(self.close_on_hover_qcb)
        dialog_qhl.setSpacing(20)

        self.notif_volume_qsr.setOrientation(QtCore.Qt.Horizontal)
        self.notif_volume_qsr.setMinimum(0)
        self.notif_volume_qsr.setMaximum(100)
        audio_qhl = QtWidgets.QHBoxLayout()
        audio_qhl.addWidget(self.notif_select_audio_qpb)
        audio_qhl.addWidget(self.notif_volume_qsr)

        grid = QtWidgets.QGridLayout()

        # first grid column
        grid.addLayout(on_off_qhl, 0, 0)
        grid.addWidget(H2(self.tr("Notifications")), 2, 0)
        grid.addWidget(RaisedHorizontalLine(), 3, 0)
        grid.addWidget(QtWidgets.QLabel(self.tr("Notification type")), 4, 0)
        grid.addWidget(notification_type_qgb, 5, 0)
        grid.addWidget(SunkenHorizontalLine(), 6, 0)
        grid.addLayout(breathing_reminder_interval_qhl, 7, 0)
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
        self.breathing_settings_wt.setLayout(vbox_l2)

