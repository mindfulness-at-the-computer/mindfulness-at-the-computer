import logging
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import mc.gui.rest_action_list_wt
import mc.model
import mc.mc_global
import mc.gui.breathing_history_wt
import mc.gui.breathing_settings_wt
import mc.gui.breathing_phrase_list_wt
import mc.gui.rest_settings_wt
import mc.gui.rest_dlg
import mc.gui.breathing_dlg
import mc.gui.breathing_notification
import mc.gui.rest_notification
import mc.gui.rest_dlg
import mc.gui.intro_dlg
import mc.gui.rest_prepare

SLIDER_MIN_MINUTES_INT = 0
# -this must be zero so that the ticks are in the right positions, if we have 1 here for example, the ticks will be
#  off by one
SLIDER_MAX_MINUTES_INT = 180
DEFAULT_SUSPEND_MINUTES_INT = 30


class SysinfoDialog(QtWidgets.QDialog):
    def __init__(self, i_parent=None):
        super(SysinfoDialog, self).__init__(i_parent)
        self.setModal(True)

        vbox_l2 = QtWidgets.QVBoxLayout(self)

        self._system_info_str = '\n'.join([
            descr_str + ": " + str(value) for (descr_str, value) in mc.mc_global.sys_info_telist
        ])

        self.system_info_qll = QtWidgets.QLabel(self._system_info_str)
        vbox_l2.addWidget(self.system_info_qll)

        self.copy_qpb = QtWidgets.QPushButton(self.tr("Copy to clipboard"))
        self.copy_qpb.clicked.connect(self.on_copy_button_clicked)
        vbox_l2.addWidget(self.copy_qpb)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtCore.Qt.Horizontal,
            self
        )
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Close)

        vbox_l2.addWidget(self.button_box)
        self.button_box.rejected.connect(self.reject)
        # -accepted and rejected are "slots" built into Qt

    def on_copy_button_clicked(self):
        qclipboard = QtGui.QGuiApplication.clipboard()
        qclipboard.setText(self._system_info_str)
        # -this will copy the text to the system clipboard
