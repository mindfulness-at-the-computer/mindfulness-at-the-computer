import logging
from PyQt5 import QtCore
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
DEFAULT_SUSPENT_MINUTES_INT = 60


class SuspendTimeDialog(QtWidgets.QDialog):
    """
    Inspiration: Answer by lou here:
    https://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
    """
    def __init__(self, i_parent=None):
        super(SuspendTimeDialog, self).__init__(i_parent)

        self.setModal(True)

        self.updating_gui_bool = False

        active_phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)

        vbox_l2 = QtWidgets.QVBoxLayout(self)

        self.suspend_time_qsr = QtWidgets.QSlider(self)
        self.suspend_time_qsr.setOrientation(QtCore.Qt.Horizontal)
        self.suspend_time_qsr.setMinimum(SLIDER_MIN_MINUTES_INT)
        self.suspend_time_qsr.setMaximum(SLIDER_MAX_MINUTES_INT)
        self.suspend_time_qsr.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.suspend_time_qsr.setTickInterval(30)
        self.suspend_time_qsr.setFixedWidth(320)
        # self.suspend_time_qsr.setSingleStep(5)
        self.suspend_time_qsr.setPageStep(30)
        self.suspend_time_qsr.setValue(DEFAULT_SUSPENT_MINUTES_INT)
        self.suspend_time_qsr.valueChanged.connect(self.on_suspend_time_slider_value_changed)
        vbox_l2.addWidget(self.suspend_time_qsr)

        self.suspend_time_qll = QtWidgets.QLabel()
        self.suspend_time_qll.setFont(mc.mc_global.get_font_large())
        self.suspend_time_qll.setWordWrap(True)
        vbox_l2.addWidget(self.suspend_time_qll)

        self.help_qll= QtWidgets.QLabel(
            "To resume after having suspended the application, drag the slider to the far left"
        )
        self.help_qll.setWordWrap(True)
        vbox_l2.addWidget(self.help_qll)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )
        vbox_l2.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        # -accept and reject are "slots" built into Qt

        self.update_gui()

    def on_suspend_time_slider_value_changed(self):
        self.update_gui()

    def update_gui(self):
        self.updating_gui_bool = True

        if self.suspend_time_qsr.value() == 0:
            self.suspend_time_qll.setText(
                "Application will resume in normal mode"
            )
        else:
            self.suspend_time_qll.setText(
                "Application will be suspended for " + str(self.suspend_time_qsr.value()) + " minutes"
            )

        self.updating_gui_bool = False
