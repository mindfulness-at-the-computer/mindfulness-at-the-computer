from mc.gui.breathing_history_wt import BreathingHistoryWt
from mc.gui.breathing_settings_wt import BreathingSettingsWt
from mc.gui.rest_settings_wt import RestSettingsWt
from mc.gui.timing_settings_wt import TimingSettingsWt
from mc.gui.general_settings_wt import RunOnStartupWt
from mc.gui.reusable_components import *


class SettingsPageWt(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self.breathing_settings_wt = BreathingSettingsWt()
        self.rest_settings_wt = RestSettingsWt()
        self.breathing_history_wt = BreathingHistoryTabWt()
        self.timing_settings_wt = TimingSettingsWt()
        self.general_settings_wt = GeneralSettingsWt()
        self._init_ui()

    def _init_ui(self):
        self.setGeometry(100, 64, 900, 670)

        self.setTabPosition(self.West)

        self.addTab(self.breathing_settings_wt, self.tr("Breathing"))
        self.addTab(self.rest_settings_wt, self.tr("Resting"))
        self.addTab(self.timing_settings_wt, self.tr("Timers"))
        self.addTab(self.breathing_history_wt, self.tr("History"))
        self.addTab(self.general_settings_wt, self.tr("General settings"))


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


class GeneralSettingsWt(QtWidgets.QScrollArea):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 64, 900, 670)
        self.run_on_startup_wt = None
        self._init_ui()

    def _init_ui(self):
        grid = PageGrid()

        if QtCore.QSysInfo.kernelType() == 'darwin':
            self.run_on_startup_wt = RunOnStartupWt()
            grid.addWidget(self.run_on_startup_wt, 0, 1)
            self.run_on_startup_wt.run_on_startup_qcb.toggled.connect(self.run_on_startup_wt.on_run_on_startup_toggled)

        vbox_l2 = QtWidgets.QVBoxLayout()
        vbox_l2.addWidget(H1(self.tr("General Settings")))
        vbox_l2.addWidget(HorizontalLine())
        vbox_l2.addStretch(1)
        vbox_l2.addLayout(grid)
        vbox_l2.addStretch(3)
        self.setLayout(vbox_l2)

