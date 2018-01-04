import os

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from mc import model, mc_global
import mc.gui.breathing_dlg


class IntroDlg(QtWidgets.QDialog):
    close_signal = QtCore.pyqtSignal(bool)
    # -the boolean indicates whether or not we want the breathing dialog to open

    def __init__(self):
        super().__init__()

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        vbox_l2.addSpacing(40)

        # Main area

        self.info_qll = QtWidgets.QLabel(self.tr("1. Info text, describing mindfulness"))
        vbox_l2.addWidget(self.info_qll)

        vbox_l2.addSpacing(40)

        vbox_l2.addWidget(QtWidgets.QLabel("2. Use the breathing dialog"))
        self.breathing_dlg = mc.gui.breathing_dlg.BreathingDlg()
        # self.breathing_dlg.show()
        vbox_l2.addWidget(self.breathing_dlg)

        vbox_l2.addSpacing(40)

        self.wizard_qll = QtWidgets.QLabel(self.tr("3. Please choose your initial settings"))
        vbox_l2.addWidget(self.wizard_qll)
        self.setting_example_interval_qsb = QtWidgets.QSpinBox()
        vbox_l2.addWidget(self.setting_example_interval_qsb)
        self.setting_example_audio_qcb = QtWidgets.QCheckBox("Audio active")
        vbox_l2.addWidget(self.setting_example_audio_qcb)

        vbox_l2.addSpacing(40)

        self.close_qpb = QtWidgets.QPushButton("Close")
        vbox_l2.addWidget(self.close_qpb)
        self.close_qpb.clicked.connect(self.on_close_clicked)

        # self.setup_rest_action_list()
        self.show()

    def on_close_clicked(self):
        self.close_signal.emit(False)
        self.close()
