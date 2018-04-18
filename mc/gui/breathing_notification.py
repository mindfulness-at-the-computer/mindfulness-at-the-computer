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
IMAGE_GOAL_WIDTH_INT = 70
IMAGE_GOAL_HEIGHT_INT = 70


class BreathingNotification(QtWidgets.QFrame):
    # close_signal = QtCore.pyqtSignal(list, list)
    breathe_signal = QtCore.pyqtSignal()
    close_signal = QtCore.pyqtSignal()
    # wait_signal = QtCore.pyqtSignal()

    def __init__(self, i_preparatory: bool=False):
        super().__init__(None, WINDOW_FLAGS)

        # self.setWindowFlags()
        # -To avoid the window getting focus we need to set both QtCore.Qt.Dialog
        #  and QtCore.Qt.WindowDoesNotAcceptFocus (setting QtCore.Qt.Popup +
        #  QtCore.Qt.WindowDoesNotAcceptFocus doesn't work)

        # | QtCore.Qt.WindowStaysOnTopHint
        # | QtCore.Qt.X11BypassWindowManagerHint

        self.preparatory_bool = i_preparatory

        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.setLineWidth(1)

        hbox_l2 = QtWidgets.QHBoxLayout()
        self.setLayout(hbox_l2)

        self.image_qll = QtWidgets.QLabel()
        hbox_l2.addWidget(self.image_qll)

        image_filename_str = "stones.png"
        if self.preparatory_bool:
            image_filename_str = "bikkhu-hands.png"
        self.image_qll.setPixmap(
            QtGui.QPixmap(mc.mc_global.get_user_images_path(image_filename_str))
        )
        self.image_qll.setScaledContents(True)
        self.resize_image()

        vbox_l3 = QtWidgets.QVBoxLayout()
        hbox_l2.addLayout(vbox_l3)

        if self.preparatory_bool:
            self.prep_qll = QtWidgets.QLabel("Please slow down and prepare for your breathing break. Please adjust your posture")
            self.prep_qll.setWordWrap(True)
            vbox_l3.addWidget(self.prep_qll)
        else:
            phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)
            self.ib_qll = QtWidgets.QLabel(phrase.ib)
            vbox_l3.addWidget(self.ib_qll)
            self.ob_qll = QtWidgets.QLabel(phrase.ob)
            vbox_l3.addWidget(self.ob_qll)

        hbox_l4 = QtWidgets.QHBoxLayout()
        vbox_l3.addLayout(hbox_l4)

        hbox_l4.addStretch(1)

        self.breathe_qpb = QtWidgets.QPushButton(self.tr("Open Dialog"))
        hbox_l4.addWidget(self.breathe_qpb)
        self.breathe_qpb.setFlat(True)
        self.breathe_qpb.clicked.connect(self.on_breathe_button_clicked)
        self.breathe_qpb.setFont(mc.mc_global.get_font_small())

        self.skip_qpb = QtWidgets.QPushButton(self.tr("Close"))
        hbox_l4.addWidget(self.skip_qpb)
        self.skip_qpb.clicked.connect(self.on_close_button_clicked)
        self.skip_qpb.setFlat(True)
        self.skip_qpb.hide()

        self.show()  # -done after all the widget have been added so that the right size is set
        self.raise_()
        self.showNormal()

        # Set position - done after show to get the right size hint
        screen_qrect = QtWidgets.QApplication.desktop().availableGeometry()
        xpos_int = screen_qrect.right() - self.sizeHint().width() - 30
        ypos_int = screen_qrect.bottom() - self.sizeHint().height() - 30
        self.move(xpos_int, ypos_int)

        self.shown_qtimer = None
        self.start_shown_timer()

    def start_shown_timer(self):
        self.shown_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.shown_qtimer.setSingleShot(True)
        self.shown_qtimer.timeout.connect(self.shown_timer_timeout)
        self.shown_qtimer.start(SHOWN_TIMER_TIME_INT)

    def shown_timer_timeout(self):
        if self.preparatory_bool:
            self.breathe_signal.emit()
            self.close()
        else:
            self.on_close_button_clicked()

    # overridden
    def mousePressEvent(self, i_qmouseevent):
        if self.breathe_qpb.isEnabled():
            self.close_signal.emit()
            self.close()

    def on_breathe_button_clicked(self):
        if self.breathe_qpb.isEnabled():
            self.close()  # -closing first to avoid collision between dialogs
            self.breathe_signal.emit()

    def on_close_button_clicked(self):
        if self.breathe_qpb.isEnabled():
            self.close_signal.emit()
            self.close()

    def resize_image(self):
        if self.image_qll.pixmap() is None:
            return
        old_width_int = self.image_qll.pixmap().width()
        old_height_int = self.image_qll.pixmap().height()
        if old_width_int == 0:
            return
        width_relation_float = old_width_int / IMAGE_GOAL_WIDTH_INT
        height_relation_float = old_height_int / IMAGE_GOAL_HEIGHT_INT

        if width_relation_float > height_relation_float:
            scaled_width_int = IMAGE_GOAL_WIDTH_INT
            scaled_height_int = (scaled_width_int / old_width_int) * old_height_int
        else:
            scaled_height_int = IMAGE_GOAL_HEIGHT_INT
            scaled_width_int = (scaled_height_int / old_height_int) * old_width_int

        self.image_qll.setFixedWidth(scaled_width_int)
        self.image_qll.setFixedHeight(scaled_height_int)
