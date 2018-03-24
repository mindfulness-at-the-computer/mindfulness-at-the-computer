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
import mc.gui.breathing_prepare

SLIDER_MIN_MINUTES_INT = 0
# -this must be zero so that the ticks are in the right positions, if we have 1 here for example, the ticks will be
#  off by one
SLIDER_MAX_MINUTES_INT = 180
DEFAULT_SUSPENT_MINUTES_INT = 30


class SysinfoDialog(QtWidgets.QDialog):
    """
    Inspiration: Answer by lou here:
    https://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
    """
    def __init__(self, i_parent=None):
        super(SysinfoDialog, self).__init__(i_parent)

        self.setModal(True)

        vbox_l2 = QtWidgets.QVBoxLayout(self)

        self._info_str = '\n'.join([
            descr_str + ": " + str(value) for (descr_str, value) in mc.mc_global.sys_info_telist
        ])

        self.system_info_qll = QtWidgets.QLabel(self._info_str)
        vbox_l2.addWidget(self.system_info_qll)

        self.copy_qpb = QtWidgets.QPushButton("Copy to clipboard")
        self.copy_qpb.clicked.connect(self.on_copy_button_clicked)
        vbox_l2.addWidget(self.copy_qpb)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtCore.Qt.Horizontal,
            self
        )
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        #.addButton(QtWidgets.QDialogButtonBox.Close)

        vbox_l2.addWidget(self.button_box)
        # self.button_box.accep.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        # -accept and reject are "slots" built into Qt

    def on_copy_button_clicked(self):
        qclipboard = QtGui.QGuiApplication.clipboard()
        qclipboard.setText(self._info_str)
        # -this will copy the text to the system clipboard

    """
    def update_gui(self):
        self.updating_gui_bool = True

        self.suspend_time_qll.setText(
            "Application will be suspended for " + str(self.suspend_time_qsr.value()) + " minutes"
        )

        self.updating_gui_bool = False
    """
