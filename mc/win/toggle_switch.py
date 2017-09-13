from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui


class ToggleSwitchComposite(QtWidgets.QWidget):
    toggled_signal = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.widget_can_be_enabled_bool = False

        self.updating_gui_bool = False

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)
        # vbox.setContentsMargins(0, -1, -1, 0)
        (left, right, top, bottom) = vbox.getContentsMargins()
        vbox.setContentsMargins(0, 0, 5, 5)

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)


        self.on_qpb = QtWidgets.QPushButton("On")
        hbox.addWidget(self.on_qpb)
        self.on_qpb.setFixedWidth(40)
        self.on_qpb.setCheckable(True)
        self.on_qpb.toggled.connect(self.on_on_toggled)

        self.off_qpb = QtWidgets.QPushButton("Off")
        hbox.addWidget(self.off_qpb)
        self.off_qpb.setFixedWidth(40)
        self.off_qpb.setCheckable(True)
        self.off_qpb.toggled.connect(self.on_off_toggled)

        self.state_qll = QtWidgets.QLabel("Enabled")
        hbox.addWidget(self.state_qll)
        new_font = QtGui.QFont()
        new_font.setBold(True)
        self.state_qll.setFont(new_font)

    def on_on_toggled(self, i_checked: bool):
        if self.updating_gui_bool:
            return
        if i_checked:
            self.toggled_signal.emit(True)
            self.update_gui(True)

    def on_off_toggled(self, i_checked: bool):
        if self.updating_gui_bool:
            return
        if i_checked:
            self.toggled_signal.emit(False)
            self.update_gui(False)

    def update_gui(self, i_enabled: bool):
        self.updating_gui_bool = True

        if i_enabled:
            self.on_qpb.setChecked(True)
            self.off_qpb.setChecked(False)
            self.state_qll.setText("Enabled")
        else:
            self.on_qpb.setChecked(False)
            self.off_qpb.setChecked(True)
            self.state_qll.setText("Disabled")

        if self.widget_can_be_enabled_bool:
            pass
        else:
            pass
            # self.state_qll.setText("Disabled")

        self.updating_gui_bool = False

