import logging
import time
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import mc.mc_global
import mc.model

BAR_HEIGHT_FT = 16.0
POINT_SIZE_INT = 16
GRADIENT_IN_FT = 120.0
GRADIENT_OUT_FT = 150.0


class ExpNotificationWidget(QtWidgets.QWidget):
    breathing_cycle_completed_signal = QtCore.pyqtSignal(int, int)

    def __init__(self):
        super().__init__()

        self.state = mc.mc_global.BreathingState.inactive
        self.ib_qtimer = None
        self.ob_qtimer = None

        self.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.X11BypassWindowManagerHint
        )
        # | QtCore.Qt.WindowStaysOnTopHint
        # | QtCore.Qt.X11BypassWindowManagerHint

        # self.setStyleSheet("background-color: rgba(0,0,0,0)")

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)
        # (left, right, top, bottom) = vbox_l2.getContentsMargins()
        # vbox_l2.setContentsMargins(0, 0, 5, 5)

        in_str = "-----------------"
        out_str = "-"
        if mc.mc_global.active_phrase_id_it != mc.mc_global.NO_PHRASE_SELECTED_INT:
            breathing_phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)
            in_str = breathing_phrase.ib_str
            out_str = breathing_phrase.ob_str

        self.cll_one = CustomLabel(in_str)
        vbox_l2.addWidget(self.cll_one)
        #self.qll_one.mouse.connect(self.on_mouse_over_one)
        self.qll_two = QtWidgets.QLabel(out_str)
        vbox_l2.addWidget(self.qll_two)

        self.breathing_graphicsview_l3 = QtWidgets.QGraphicsView()  # QGraphicsScene
        vbox_l2.addWidget(self.breathing_graphicsview_l3)
        self.breathing_graphicsview_l3.setFixedHeight(BAR_HEIGHT_FT)  # + 2 * SMALL_MARGIN_FT
        self.breathing_graphicsview_l3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.breathing_graphicsview_l3.setAlignment(QtCore.Qt.AlignAbsolute)
        self.breathing_graphicsscene_l4 = QtWidgets.QGraphicsScene()
        self.breathing_graphicsview_l3.setScene(self.breathing_graphicsscene_l4)

        hbox = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox)
        self.in_qpb = CustomButton("In")
        hbox.addWidget(self.in_qpb)
        self.in_qpb.clicked.connect(self.on_in_button_clicked)
        self.out_qpb = CustomButton("Out")
        hbox.addWidget(self.out_qpb)
        self.out_qpb.clicked.connect(self.on_out_button_clicked)
        self.close_qpb = CustomButton("Close")
        hbox.addWidget(self.close_qpb)
        self.close_qpb.clicked.connect(self.on_close_button_clicked)

        self.show()  # -done after all the widget have been added so that the right size is set

        # Set position - done after show to get the right size hint
        screen_qrect = QtWidgets.QApplication.desktop().availableGeometry()
        xpos_int = screen_qrect.left() + (screen_qrect.width() - self.sizeHint().width()) // 2
        ypos_int = screen_qrect.bottom() - self.sizeHint().height() - 50
        self.move(xpos_int, ypos_int)

        self.in_breath_graphics_qgri_list = []
        self.out_breath_graphics_qgri_list = []
        # self.start_breathing_in_timer()

        cursor = QtGui.QCursor()
        cursor.setPos(xpos_int + self.width() // 2, ypos_int + self.height() // 2)
        self.setCursor(cursor)

    def breathing_in(self):
        self.state = mc.mc_global.BreathingState.breathing_in
        self.stop_breathing_out_timer()
        self.start_breathing_in_timer()

    def breathing_out(self):
        self.state = mc.mc_global.BreathingState.breathing_out
        self.stop_breathing_in_timer()
        self.start_breathing_out_timer()

    def on_in_button_clicked(self):
        if self.state == mc.mc_global.BreathingState.inactive:
            self.breathing_in()

    def on_out_button_clicked(self):
        if self.state == mc.mc_global.BreathingState.breathing_in:
            self.breathing_out()

    def on_close_button_clicked(self):
        if len(self.in_breath_graphics_qgri_list) > 0:
            last_ib_rect = self.in_breath_graphics_qgri_list[-1].rect()
            last_ob_rect = self.out_breath_graphics_qgri_list[-1].rect()
            self.breathing_cycle_completed_signal.emit(
                last_ib_rect.width(),
                last_ob_rect.width()
            )
            # TODO: send all to the main window --- assuming that we want to allow more than
            # one breath in this dialog. The alternative would be to allow the user to open
            # the main breathing dialog if she wanted to follow the breath for more than one
            # breathing cycle

        self.close()

    def start_breathing_in_timer(self):
        self.ib_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.ib_qtimer.timeout.connect(self.breathing_in_timer_timeout)
        self.ib_qtimer.start(100)
        logging.info("Timer started at " + str(time.time()))

        t_drawrect = QtCore.QRectF(0.0, 0.0, 1.0, BAR_HEIGHT_FT)

        t_start_qpointf = QtCore.QPointF(t_drawrect.left() - GRADIENT_IN_FT, t_drawrect.top())
        t_stop_qpointf = t_drawrect.bottomRight()  # QtCore.QPointF(0.0, 50.0)
        t_linear_gradient = QtGui.QLinearGradient(t_start_qpointf, t_stop_qpointf)
        t_linear_gradient.setColorAt(0.0, QtGui.QColor(204, 255, 77))
        t_linear_gradient.setColorAt(1.0, QtGui.QColor(164, 230, 0))
        t_brush = QtGui.QBrush(t_linear_gradient)

        t_pen = QtGui.QPen(QtCore.Qt.NoPen)

        t_graphics_rect_item = self.breathing_graphicsscene_l4.addRect(
            t_drawrect,
            pen=t_pen,
            brush=t_brush
        )
        self.in_breath_graphics_qgri_list.append(t_graphics_rect_item)

    def breathing_in_timer_timeout(self):
        t_graphics_rect_item = self.in_breath_graphics_qgri_list[-1]
        new_rect = t_graphics_rect_item.rect()
        new_rect.setLeft(new_rect.left() - 1)
        t_graphics_rect_item.setRect(new_rect)

        # self.breathing_graphicsview_l3.centerOn(t_graphics_rect_item)

    def stop_breathing_in_timer(self):
        if self.ib_qtimer is None:
            return
        self.ib_qtimer.stop()
        logging.debug("Timer stopped at " + str(time.time()))

    def start_breathing_out_timer(self):
        self.ob_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.ob_qtimer.timeout.connect(self.breathing_out_timer_timeout)
        self.ob_qtimer.start(100)
        logging.info("Timer started at " + str(time.time()))

        t_drawrect = QtCore.QRectF(0.0, 0.0, 1.0, BAR_HEIGHT_FT)

        t_start_qpointf = QtCore.QPointF(t_drawrect.x() + GRADIENT_OUT_FT, t_drawrect.y())
        t_stop_qpointf = t_drawrect.bottomLeft()  # QtCore.QPointF(0.0, 50.0)
        t_linear_gradient = QtGui.QLinearGradient(t_start_qpointf, t_stop_qpointf)
        # t_linear_gradient.setColorAt(0.0, QtGui.QColor(230, 230, 230))
        # t_linear_gradient.setColorAt(1.0, QtGui.QColor(190, 190, 190))
        t_linear_gradient.setColorAt(0.0, QtGui.QColor(219, 255, 128))
        t_linear_gradient.setColorAt(1.0, QtGui.QColor(183, 255, 0))
        t_brush = QtGui.QBrush(t_linear_gradient)

        t_pen = QtGui.QPen(QtCore.Qt.NoPen)

        t_graphics_rect_item = self.breathing_graphicsscene_l4.addRect(
            t_drawrect,
            brush=t_brush,
            pen=t_pen
        )

        self.out_breath_graphics_qgri_list.append(t_graphics_rect_item)

    def stop_breathing_out_timer(self):
        if self.ob_qtimer is None:
            return
        self.ob_qtimer.stop()
        logging.debug("Timer stopped at " + str(time.time()))

    def breathing_out_timer_timeout(self):
        t_graphics_rect_item = self.out_breath_graphics_qgri_list[-1]
        new_rect = t_graphics_rect_item.rect()
        new_rect.setRight(new_rect.right() + 1)
        t_graphics_rect_item.setRect(new_rect)


    """
    # overridden
    def show(self):
        screen_qrect = QtWidgets.QApplication.desktop().availableGeometry()
        xpos_int = screen_qrect.left() + (screen_qrect.width() - self.sizeHint().width()) // 2
        ypos_int = screen_qrect.bottom() - self.sizeHint().height() - 50
        super().show()
    """


class CustomLabel(QtWidgets.QLabel):
    def __init__(self, i_title: str):
        super().__init__(i_title)

    # Overridden
    def enterEvent(self, i_QEvent):
        logging.debug("enterEvent")


class CustomButton(QtWidgets.QPushButton):
    def __init__(self, i_title: str):
        super().__init__(i_title)

    # Overridden
    def enterEvent(self, i_QEvent):
        logging.debug("CustomButton: enterEvent")

