from PyQt5 import QtCore
from PyQt5 import QtWidgets

WINDOW_FLAGS = (
    QtCore.Qt.Dialog
    | QtCore.Qt.WindowStaysOnTopHint
    | QtCore.Qt.FramelessWindowHint
    | QtCore.Qt.WindowDoesNotAcceptFocus
    | QtCore.Qt.BypassWindowManagerHint
)

SHOWN_TIMER_TIME_INT = 8000
MIN_HEIGHT_INT = 80


class RestPrepareDlg(QtWidgets.QFrame):
    def __init__(self):
        super().__init__(None, WINDOW_FLAGS)

        self.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.setLineWidth(1)

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.setMinimumHeight(MIN_HEIGHT_INT)

        self.title_qll = QtWidgets.QLabel(self.tr("Please prepare for rest"))
        vbox_l2.addWidget(self.title_qll)
        self.title_qll.setWordWrap(True)

        self.reminder_qll = QtWidgets.QLabel(self.tr("One minute left until the next rest"))
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

    def start_shown_timer(self):
        self.shown_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.shown_qtimer.setSingleShot(True)
        self.shown_qtimer.timeout.connect(self.shown_timer_timeout)
        self.shown_qtimer.start(SHOWN_TIMER_TIME_INT)

    def shown_timer_timeout(self):
        self.close()

    # overridden
    def mousePressEvent(self, i_qmouseevent):
        self.close()
