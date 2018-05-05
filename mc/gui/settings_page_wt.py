import mc.mc_global
import mc.model
from PyQt5 import QtWidgets
from mc.gui.reusable_components import H1, H2, HorizontalLine


class SettingsPageWt(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self.breathing_settings_wt = QtWidgets.QWidget()
        self.turn_breathing_on_off_qcb = QtWidgets.QCheckBox()
        self._init_ui()

    def _init_ui(self):
        settings = mc.model.SettingsM.get()
        self.setGeometry(100, 64, 900, 670)

        self.setTabPosition(self.West)
        self.addTab(self.breathing_settings_wt, self.tr("Breathing"))

        # initializing the values of the controls (for now only breathing on/off is initialized)
        self.turn_breathing_on_off_qcb.setChecked(settings.breathing_reminder_active_bool)

        # Setting up the radio buttons for the notification type
        # note that this is not hooked up to any functionality yet.
        # They do respond visually to checking/unchecking them
        both_qrb = QtWidgets.QRadioButton()
        both_qrb.setObjectName("both_qrb")

        visual_qrb = QtWidgets.QRadioButton()
        visual_qrb.setObjectName("visual_qrb")

        audio_qrb = QtWidgets.QRadioButton()
        audio_qrb.setObjectName("audio_qrb")

        notification_type_qhl = QtWidgets.QHBoxLayout()
        notification_type_qhl.addWidget(both_qrb)
        notification_type_qhl.addWidget(visual_qrb)
        notification_type_qhl.addWidget(audio_qrb)

        grid = QtWidgets.QGridLayout()

        # first grid column
        grid.addWidget(QtWidgets.QLabel(self.tr("Turn the breathing dialog and notifications on or off")), 0, 0)
        grid.addWidget(H2(self.tr("Notifications")), 2, 0)
        grid.addWidget(HorizontalLine(), 3, 0, 1, 2)
        grid.addWidget(QtWidgets.QLabel(self.tr("Notification type")), 4, 0)
        grid.addLayout(notification_type_qhl, 5, 0)

        # second grid column
        grid.addWidget(self.turn_breathing_on_off_qcb, 0, 1)

        # third grid column
        grid.addWidget(QtWidgets.QLabel(self.tr("These are the sentences that appear in the `breathing dialog`")), 0, 3)
        grid.addWidget(QtWidgets.QLabel(self.tr("They also appear in the `breathing notification`")), 1, 3)

        vbox_l2 = QtWidgets.QVBoxLayout()
        vbox_l2.addWidget(H1(self.tr("Settings for Breathing")))
        vbox_l2.addWidget(HorizontalLine())
        vbox_l2.addStretch(1)
        vbox_l2.addLayout(grid)
        vbox_l2.addStretch(3)
        self.breathing_settings_wt.setLayout(vbox_l2)

