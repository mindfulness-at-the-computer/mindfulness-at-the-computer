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

SHOWN_TIMER_TIME_INT = 8000


class RestPrepareDlg(QtWidgets.QFrame):
    rest_signal = QtCore.pyqtSignal()
    skip_signal = QtCore.pyqtSignal()
    wait_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__(None, WINDOW_FLAGS)

        self.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.setLineWidth(1)

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.setMinimumHeight(80)

        self.title_qll = QtWidgets.QLabel("Please prepare for rest")
        vbox_l2.addWidget(self.title_qll)
        self.title_qll.setWordWrap(True)

        self.reminder_qll = QtWidgets.QLabel("One minute left until the next rest")
        vbox_l2.addWidget(self.reminder_qll)
        self.reminder_qll.setWordWrap(True)

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

        self.setStyleSheet("background-color: #101010; color: #999999;")

        # self.setStyleSheet("QPushButton {background-color: red;}")
        # border-style: outset;border-width: 2px;border-color: beige;
        # self.setStyleSheet("QPushButton {border-style: solid;border-width: 1px;border-color: black;}")
        # self.setStyleSheet("QPushButton:hover {background-color:green;}")

    def start_shown_timer(self):
        self.shown_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.shown_qtimer.setSingleShot(True)
        self.shown_qtimer.timeout.connect(self.shown_timer_timeout)
        self.shown_qtimer.start(SHOWN_TIMER_TIME_INT)

    def shown_timer_timeout(self):
        self.close()

    # overridden
    def mousePressEvent(self, i_QMouseEvent):
        self.close()

    """
    def on_rest_button_clicked(self):
        self.rest_signal.emit()
        self.close()

    def on_skip_button_clicked(self):
        self.skip_signal.emit()
        self.close()

    def on_wait_button_clicked(self):
        self.wait_signal.emit()
        self.close()
    """
