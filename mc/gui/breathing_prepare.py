from PyQt5 import QtCore
from PyQt5 import QtWidgets
import mc.mc_global

WINDOW_FLAGS = (
    QtCore.Qt.Dialog
    | QtCore.Qt.WindowStaysOnTopHint
    | QtCore.Qt.FramelessWindowHint
    | QtCore.Qt.WindowDoesNotAcceptFocus
    | QtCore.Qt.BypassWindowManagerHint
)

SHOWN_TIMER_TIME_INT = 5000

# TODO: Change name to "notification"?
class BreathingPrepareDlg(QtWidgets.QFrame):
    closed_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__(None, WINDOW_FLAGS)

        self.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.setLineWidth(1)
        self.setMouseTracking(True)

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.setMinimumHeight(80)

        self.title_qll = QtWidgets.QLabel("Breathing break soon")
        self.title_qll.setWordWrap(True)
        self.title_qll.setFont(mc.mc_global.get_font_large())
        vbox_l2.addWidget(self.title_qll)

        self.reminder_qll = QtWidgets.QLabel("Please slow down and prepare for your breathing break. Please adjust your posture")
        self.reminder_qll.setWordWrap(True)
        self.reminder_qll.setFont(mc.mc_global.get_font_medium())
        vbox_l2.addWidget(self.reminder_qll)


        """
        self.time_remaining_qpb = QtWidgets.QProgressBar()
        vbox_l2.addWidget(self.time_remaining_qpb)


        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)

        self.rest_qpb = QtWidgets.QPushButton(self.tr("Breathe"))
        hbox_l3.addWidget(self.rest_qpb, stretch=1)
        self.rest_qpb.setFont(mc.mc_global.get_font_large(i_bold=False))
        # self.rest_qpb.clicked.connect(self.on_rest_button_clicked)
        self.rest_qpb.setStyleSheet("background-color:" + mc.mc_global.MC_DARK_GREEN_COLOR_STR + "; color:#000000;")

        hbox_l3.addStretch(1)
        self.move_qpb = QtWidgets.QPushButton(self.tr("Move"))  # alt: Arrows for where to move
        hbox_l3.addWidget(self.move_qpb)
        self.move_qpb.setFlat(True)
        self.wait_qpb = QtWidgets.QPushButton(self.tr("Wait"))
        hbox_l3.addWidget(self.wait_qpb)
        self.wait_qpb.setFlat(True)
        # self.wait_qpb.clicked.connect(self.on_wait_button_clicked)
        self.skip_qpb = QtWidgets.QPushButton(self.tr("Skip"))
        hbox_l3.addWidget(self.skip_qpb)
        self.skip_qpb.setFlat(True)
        # self.skip_qpb.clicked.connect(self.on_skip_button_clicked)
        hbox_l3.addStretch(1)

        """

        self.show()  # -done after all the widget have been added so that the right size is set
        self.raise_()
        self.showNormal()

        # Set position - done after show to get the right size hint
        screen_qrect = QtWidgets.QApplication.desktop().availableGeometry()
        self.xpos_int = (screen_qrect.right() / 2) - (self.sizeHint().width() / 2)
        self.ypos_upper_int = screen_qrect.top() + 30
        self.ypos_lower_int = screen_qrect.bottom() - 30 - self.sizeHint().height()
        self.ypos_int = self.ypos_lower_int
        self.move(self.xpos_int, self.ypos_int)

        self.shown_qtimer = None
        self.start_shown_timer()

        ##### self.setStyleSheet("background-color: #101010; color: #999999;")

        # self.setStyleSheet("QPushButton {background-color: red;}")
        # border-style: outset;border-width: 2px;border-color: beige;
        # self.setStyleSheet("QPushButton {border-style: solid;border-width: 1px;border-color: black;}")
        # self.setStyleSheet("QPushButton:hover {background-color:green;}")

    #TODO: On hover - moving

    def start_shown_timer(self):
        self.shown_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.shown_qtimer.setSingleShot(True)
        self.shown_qtimer.timeout.connect(self.shown_timer_timeout)
        self.shown_qtimer.start(SHOWN_TIMER_TIME_INT)

    def close_prepare_frame(self):
        self.closed_signal.emit()
        self.close()

    def shown_timer_timeout(self):
        self.shown_qtimer.stop()
        self.close_prepare_frame()

    # overridden
    def mouseMoveEvent(self, i_qmouseevent):
        if self.ypos_int == self.ypos_upper_int:
            self.ypos_int = self.ypos_lower_int
        else:
            self.ypos_int = self.ypos_upper_int
        self.move(self.xpos_int, self.ypos_int)

    # overridden
    def mousePressEvent(self, i_qmouseevent):
        self.close_prepare_frame()

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
