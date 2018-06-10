from mc.gui.breathing_history_wt import BreathingHistoryWt
from mc.gui.breathing_settings_2_wt import BreathingSettings2Wt
from mc.gui.breathing_settings_wt import BreathingSettingsWt
from mc.gui.rest_settings_wt import RestSettingsWt
from mc.gui.timing_settings_wt import TimingSettingsWt
from mc.gui.reusable_components import *


class SettingsPageWt(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self.breathing_settings_wt = BreathingSettingsWt()
        self.resting_settings_wt = RestSettingsWt()
        self.breathing_history_wt = BreathingHistoryTabWt()
        self.timing_settings_wt = TimingSettingsWt()
        self.breathing_settings_2_wt = BreathingSettings2Wt()
        self._init_ui()

    def _init_ui(self):
        self.setGeometry(100, 64, 900, 670)

        self.setTabPosition(self.West)

        self.addTab(self.breathing_settings_2_wt, self.tr("Breathe"))
        self.addTab(self.resting_settings_wt, self.tr("Resting"))
        self.addTab(self.timing_settings_wt, self.tr("Timers"))
        self.addTab(self.breathing_history_wt, self.tr("History"))
        self.addTab(self.breathing_settings_wt, self.tr("Breathing"))


class BreathingHistoryTabWt(QtWidgets.QScrollArea):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 64, 900, 670)
        self.breathing_history_wt = BreathingHistoryWt()
        self._init_ui()

    def _init_ui(self):
        grid = PageGrid()
        grid.addWidget(self.breathing_history_wt, 0, 1)

        vbox_l2 = QtWidgets.QVBoxLayout()
        vbox_l2.addWidget(H1(self.tr("Breathing history")))
        vbox_l2.addWidget(HorizontalLine())
        vbox_l2.addStretch(1)
        vbox_l2.addLayout(grid)
        vbox_l2.addStretch(3)
        self.setLayout(vbox_l2)
