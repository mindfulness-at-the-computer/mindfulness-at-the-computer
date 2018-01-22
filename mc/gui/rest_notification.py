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

SHOWN_TIMER_TIME_INT = 10000


class RestReminderDlg(QtWidgets.QFrame):
    rest_signal = QtCore.pyqtSignal()
    skip_signal = QtCore.pyqtSignal()
    wait_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__(None, WINDOW_FLAGS)

        self.hover_and_kb_active_bool = False

        self.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.setLineWidth(1)

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.reminder_qll = QtWidgets.QLabel(self.tr("Please take good care of your body and mind"))
        vbox_l2.addWidget(self.reminder_qll)
        self.reminder_qll.setWordWrap(True)

        self.rest_qpb = QtWidgets.QPushButton(self.tr("Rest"))
        vbox_l2.addWidget(self.rest_qpb, stretch=1)
        self.rest_qpb.setFont(mc.mc_global.get_font_large(i_bold=False))
        self.rest_qpb.clicked.connect(self.on_rest_button_clicked)
        self.rest_qpb.setStyleSheet("background-color:" + mc.mc_global.MC_DARK_GREEN_COLOR_STR + "; color:#000000;")
        # self.rest_qpb.clicked.connect(self.on_close_button_clicked)
        # self.rest_qpb.entered_signal.connect(self.on_close_button_hover)

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        hbox_l3.addStretch(1)
        self.wait_qpb = QtWidgets.QPushButton(self.tr("Wait"))
        hbox_l3.addWidget(self.wait_qpb)
        self.wait_qpb.setFlat(True)
        self.wait_qpb.clicked.connect(self.on_wait_button_clicked)
        self.skip_qpb = QtWidgets.QPushButton(self.tr("Skip"))
        hbox_l3.addWidget(self.skip_qpb)
        self.skip_qpb.setFlat(True)
        self.skip_qpb.clicked.connect(self.on_skip_button_clicked)
        hbox_l3.addStretch(1)

        self.show()  # -done after all the widget have been added so that the right size is set
        self.raise_()
        self.showNormal()

        # Set position - done after show to get the right size hint
        screen_qrect = QtWidgets.QApplication.desktop().availableGeometry()
        xpos_int = screen_qrect.right() - self.sizeHint().width() - 30
        ypos_int = screen_qrect.top() + 30
        self.move(xpos_int, ypos_int)

        self.shown_qtimer = None
        ##### self.start_shown_timer()

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
        self.on_wait_button_clicked()

    def on_rest_button_clicked(self):
        self.rest_signal.emit()
        self.close()

    def on_skip_button_clicked(self):
        self.skip_signal.emit()
        self.close()

    def on_wait_button_clicked(self):
        self.wait_signal.emit()
        self.close()

    # overridden
    def mousePressEvent(self, i_QMouseEvent):
        self.wait_signal.emit()
        self.close()


class CustomLabel(QtWidgets.QLabel):
    def __init__(self, i_title: str):
        super().__init__(i_title)

    # Overridden
    # noinspection PyPep8Naming
    def enterEvent(self, i_QEvent):
        logging.debug("enterEvent")


class CustomButton(QtWidgets.QPushButton):
    entered_signal = QtCore.pyqtSignal()

    def __init__(self, i_title: str):
        super().__init__(i_title)

    # Overridden
    # noinspection PyPep8Naming
    def enterEvent(self, i_QEvent):
        self.entered_signal.emit()
        logging.debug("CustomButton: enterEvent")

