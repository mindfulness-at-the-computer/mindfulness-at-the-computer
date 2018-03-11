import mc.mc_global
import mc.model
import os
from PyQt5 import QtWidgets
from shutil import copyfile
from sys import platform


class RunOnStartupWt(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.show()
        self.run_on_startup = QtWidgets.QCheckBox(self.tr("Run on startup"))
        self._init_ui()

    def _init_ui(self):
        hbox_l2 = QtWidgets.QHBoxLayout()
        hbox_l2.addWidget(self.run_on_startup)
        self.run_on_startup.setChecked(bool(mc.model.SettingsM.run_on_startup))
        self.setLayout(hbox_l2)

    @classmethod
    def on_run_on_startup_toggled(self, i_checked_bool):
        if platform == "linux" or platform == "linux2":
            pass
        elif platform == "darwin":
            plist = "com.matc.mindfulness-at-the-computer.plist"
            source_file = mc.mc_global.get_user_files_path(plist)
            target_dir = os.path.join(os.path.expanduser("~"), "Library/LaunchAgents/")

            if i_checked_bool and os.path.isdir("/Applications/mindfulness-at-the-computer.app"):
                copyfile(source_file, os.path.join(target_dir, plist))

            elif os.path.isfile(os.path.join(target_dir, plist)):
                os.remove(os.path.join(target_dir, plist))
        elif platform == "win32":
            pass

        mc.model.SettingsM.get().run_on_startup = i_checked_bool
