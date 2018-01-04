import logging
import time
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import mc.mc_global
import mc.model

WINDOW_FLAGS = (
    QtCore.Qt.Dialog
    | QtCore.Qt.WindowStaysOnTopHint
    | QtCore.Qt.FramelessWindowHint
    | QtCore.Qt.WindowDoesNotAcceptFocus
    | QtCore.Qt.BypassWindowManagerHint
)


class BreathingNotification(QtWidgets.QFrame):
    # close_signal = QtCore.pyqtSignal(list, list)
    breathe_signal = QtCore.pyqtSignal()
    close_signal = QtCore.pyqtSignal()
    # wait_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__(None, WINDOW_FLAGS)

        # self.setWindowFlags()
        # -To avoid the window getting focus we need to set both QtCore.Qt.Dialog
        #  and QtCore.Qt.WindowDoesNotAcceptFocus (setting QtCore.Qt.Popup +
        #  QtCore.Qt.WindowDoesNotAcceptFocus doesn't work)

        # | QtCore.Qt.WindowStaysOnTopHint
        # | QtCore.Qt.X11BypassWindowManagerHint

        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.setLineWidth(1)

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)
        self.ib_qll = QtWidgets.QLabel(phrase.ib)
        vbox_l2.addWidget(self.ib_qll)
        self.ob_qll = QtWidgets.QLabel(phrase.ob)
        vbox_l2.addWidget(self.ob_qll)

        hbox = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox)

        self.breathe_qpb = QtWidgets.QPushButton(self.tr("Open Dialog"))
        hbox.addWidget(self.breathe_qpb)
        # self.breathe_qpb.setFocusPolicy(QtCore.Qt.NoFocus)
        self.breathe_qpb.clicked.connect(self.on_breathe_button_clicked)
        self.breathe_qpb.setFont(mc.mc_global.get_font_medium(i_bold=True))

        self.skip_qpb = QtWidgets.QPushButton(self.tr("Close"))
        hbox.addWidget(self.skip_qpb)
        # self.skip_qpb.setFocusPolicy(QtCore.Qt.NoFocus)
        self.skip_qpb.clicked.connect(self.on_close_button_clicked)

        self.show()  # -done after all the widget have been added so that the right size is set
        self.raise_()
        self.showNormal()

        # Set position - done after show to get the right size hint
        screen_qrect = QtWidgets.QApplication.desktop().availableGeometry()
        xpos_int = screen_qrect.right() - self.sizeHint().width() - 30
        ypos_int = screen_qrect.top() + 30
        self.move(xpos_int, ypos_int)

        self.shown_qtimer = None
        self.start_shown_timer()

    def start_shown_timer(self):
        self.shown_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.shown_qtimer.setSingleShot(True)
        self.shown_qtimer.timeout.connect(self.shown_timer_timeout)
        self.shown_qtimer.start(8500)

    def shown_timer_timeout(self):
        self.on_close_button_clicked()

    def on_breathe_button_clicked(self):
        self.close()  # -closing first to avoid collision between dialogs
        self.breathe_signal.emit()

    def on_close_button_clicked(self):
        self.close_signal.emit()
        self.close()
