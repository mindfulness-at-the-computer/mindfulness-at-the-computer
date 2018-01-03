from PyQt5 import QtCore
from PyQt5 import QtWidgets
import mc.mc_global


class ToggleSwitchWt(QtWidgets.QWidget):
    toggled_signal = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.updating_gui_bool = False

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)
        # (left, right, top, bottom) = vbox.getContentsMargins()
        vbox.setContentsMargins(0, 0, 5, 5)

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)

        self.on_qpb = QtWidgets.QPushButton(self.tr("On"))
        hbox.addWidget(self.on_qpb)
        self.on_qpb.setFixedWidth(40)
        self.on_qpb.setCheckable(True)
        self.on_qpb.toggled.connect(self.on_on_toggled)

        self.off_qpb = QtWidgets.QPushButton(self.tr("Off"))
        hbox.addWidget(self.off_qpb)
        self.off_qpb.setFixedWidth(40)
        self.off_qpb.setCheckable(True)
        self.off_qpb.toggled.connect(self.on_off_toggled)

        self.state_qll = QtWidgets.QLabel(self.tr("Enabled"))
        hbox.addWidget(self.state_qll)
        self.state_qll.setFont(mc.mc_global.get_font_medium(i_bold=True))

    def on_on_toggled(self, i_checked: bool):
        if self.updating_gui_bool:
            return
        self.toggled_signal.emit(i_checked)
        self.update_gui(i_checked)

    def on_off_toggled(self, i_checked: bool):
        if self.updating_gui_bool:
            return
        self.toggled_signal.emit(not i_checked)
        self.update_gui(not i_checked)
        """
        if i_checked:
            self.toggled_signal.emit(False)
            self.update_gui(False)
        """

    def update_gui(self, i_enabled: bool):
        self.updating_gui_bool = True

        if i_enabled:
            self.on_qpb.setChecked(True)
            self.off_qpb.setChecked(False)
            self.state_qll.setText(self.tr("Enabled"))
            self.state_qll.setFont(mc.mc_global.get_font_medium(i_bold=True))
        else:
            self.on_qpb.setChecked(False)
            self.off_qpb.setChecked(True)
            self.state_qll.setText(self.tr("Disabled"))
            self.state_qll.setFont(mc.mc_global.get_font_medium(i_bold=False))

        self.updating_gui_bool = False
