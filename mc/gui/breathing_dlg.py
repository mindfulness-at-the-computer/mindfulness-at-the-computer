import logging
import time
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import mc.mc_global
import mc.model


class BreathingDlg(QtWidgets.QFrame):
    close_signal = QtCore.pyqtSignal(list, list)
    phrase_changed_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.hover_active_bool = False
        self.keyboard_active_bool = False
        self.state = mc.mc_global.BreathingState.inactive
        self.ib_qtimer = None
        self.ob_qtimer = None
        self.setWindowFlags(
            QtCore.Qt.Tool
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
        )
        # QtCore.Qt.Dialog
        # | QtCore.Qt.WindowStaysOnTopHint
        # | QtCore.Qt.X11BypassWindowManagerHint
        self.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.setLineWidth(1)
        # self.setStyleSheet("background-color: rgba(0,0,0,0)")
        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)
        # (left, right, top, bottom) = vbox_l2.getContentsMargins()
        # vbox_l2.setContentsMargins(0, 0, 5, 5)

        self.breathing_graphicsview_l3 = GraphicsView()
        vbox_l2.addWidget(self.breathing_graphicsview_l3)

        buttons_hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(buttons_hbox_l3)

        self.phrases_qcb = QtWidgets.QComboBox()
        buttons_hbox_l3.addWidget(self.phrases_qcb)
        for phrase in mc.model.PhrasesM.get_all():
            self.phrases_qcb.addItem(phrase.title_str,phrase.id_int)
        self.phrases_qcb.activated.connect(self.on_phrases_combo_activated)

        self.close_qpb = QtWidgets.QPushButton("Close")
        buttons_hbox_l3.addWidget(self.close_qpb)
        self.close_qpb.clicked.connect(self.on_close_button_clicked)
        # self.close_qpb.entered_signal.connect(self.on_close_button_hover)

        self.help_qll = QtWidgets.QLabel("Hover over the central area to breath in")
        vbox_l2.addWidget(self.help_qll, alignment=QtCore.Qt.AlignHCenter)
        font = self.help_qll.font()
        font.setItalic(True)
        self.help_qll.setFont(font)

        self.show()  # -done after all the widget have been added so that the right size is set
        self.raise_()
        self.showNormal()

        # Set position - done after show to get the right size hint
        screen_qrect = QtWidgets.QApplication.desktop().availableGeometry()
        self.xpos_int = screen_qrect.left() + (screen_qrect.width() - self.sizeHint().width()) // 2
        self.ypos_int = screen_qrect.bottom() - self.sizeHint().height() - 50
        self.move(self.xpos_int, self.ypos_int)

        self.ib_length_ft_list = []
        self.ob_length_int_list = []

        self.start_cursor_timer()

        self.update_gui()

    # overridden
    def keyPressEvent(self, i_qkeyevent):
        if not self.keyboard_active_bool:
            return
        if i_qkeyevent.key() == QtCore.Qt.Key_Shift:
            logging.info("shift key pressed")
            # self.in_qpb.click()
        else:
            pass
            # super().keyPressEvent(self, iQKeyEvent)

    # overridden
    def keyReleaseEvent(self, i_qkeyevent):
        if not self.keyboard_active_bool:
            return
        if i_qkeyevent.key() == QtCore.Qt.Key_Shift:
            logging.info("shift key released")
            # self.out_qpb.click()
        else:
            pass

    def on_phrases_combo_activated(self, i_index: int):
        logging.debug("on_phrases_combo_activated, index = " + str(i_index))
        # for i in range(0, self.phrases_qcb.count() - 1):
        db_id_int = self.phrases_qcb.itemData(i_index)
        mc.mc_global.active_phrase_id_it = db_id_int
        self.phrase_changed_signal.emit()
        self.update_gui()

    def start_cursor_timer(self):
        self.cursor_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.cursor_qtimer.setSingleShot(True)
        self.cursor_qtimer.timeout.connect(self.cursor_timer_timeout)
        self.cursor_qtimer.start(2500)

    def cursor_timer_timeout(self):
        cursor = QtGui.QCursor()
        if self.geometry().contains(cursor.pos()):
            pass
        else:
            cursor.setPos(
                self.xpos_int + self.width() // 2,
                self.ypos_int + self.height() // 2
            )
            self.setCursor(cursor)

    def breathing_in(self):
        self.state = mc.mc_global.BreathingState.breathing_in
        self.stop_breathing_out_timer()
        self.start_breathing_in_timer()

        self.ib_cll.set_active()
        self.ob_cll.set_inactive()

    def breathing_out(self):
        self.state = mc.mc_global.BreathingState.breathing_out
        self.stop_breathing_in_timer()
        self.start_breathing_out_timer()

        self.ib_cll.set_inactive()
        self.ob_cll.set_active()

    def on_close_button_clicked(self):
        self.stop_breathing_in_timer()
        self.stop_breathing_out_timer()
        self.cursor_qtimer.stop()
        self.close_signal.emit(
            self.ib_length_ft_list,
            self.ob_length_int_list
        )
        self.close()

    def start_breathing_in_timer(self):
        logging.info("Timer started at " + str(time.time()))
        self.ib_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.ib_qtimer.timeout.connect(self.breathing_in_timer_timeout)
        self.ib_qtimer.start(100)
        self.start_time_ft = time.time()

    def breathing_in_timer_timeout(self):
        pass

    def stop_breathing_in_timer(self):
        logging.debug("Timer stopped at " + str(time.time()))
        if self.ib_qtimer is None:
            return
        self.ib_qtimer.stop()
        self.ib_length_ft_list.append(time.time() - self.start_time_ft)

    def start_breathing_out_timer(self):
        self.ob_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.ob_qtimer.timeout.connect(self.breathing_out_timer_timeout)
        self.ob_qtimer.start(100)
        logging.info("Timer started at " + str(time.time()))
        self.start_time_ft = time.time()

    def stop_breathing_out_timer(self):
        logging.debug("Timer stopped at " + str(time.time()))
        if self.ob_qtimer is None:
            return
        self.ob_qtimer.stop()
        self.ob_length_ft_list.append(time.time() - self.start_time_ft)

    def breathing_out_timer_timeout(self):
        t_graphics_rect_item = self.ob_qgri_list[-1]
        new_rect = t_graphics_rect_item.rect()
        new_rect.setRight(new_rect.right() + 1)
        t_graphics_rect_item.setRect(new_rect)

    def update_gui(self):
        breathing_phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)
        in_str = breathing_phrase.ib_str
        out_str = breathing_phrase.ob_str

        for i in range(0, self.phrases_qcb.count()):
            if self.phrases_qcb.itemData(i) == mc.mc_global.active_phrase_id_it:
                self.phrases_qcb.setCurrentIndex(i)
                break


BREATHING_LABEL_MARGIN_INT = 16
BRIGHT_INT = 196
DIM_INT = 144
DARK_INT = 64


class CustomLabel(QtWidgets.QLabel):
    entered_signal = QtCore.pyqtSignal()
    pressed_signal = QtCore.pyqtSignal()

    def __init__(self, i_title: str):
        super().__init__(i_title)

        # self.color_te = (64, 64, 64)
        self.bw_color_int = BRIGHT_INT
        self.update_stylesheet()

        self.setFont(mc.mc_global.get_font_xlarge(i_underscore=False, i_bold=True))
        self.setMargin(BREATHING_LABEL_MARGIN_INT)

    def update_stylesheet(self):
        self.setStyleSheet("background-color: white; color: rgb("
            + str(self.bw_color_int) + ", "
            + str(self.bw_color_int) + ", "
            + str(self.bw_color_int)
            + ")")

    def set_active(self):
        self.setFont(mc.mc_global.get_font_xlarge(i_underscore=True, i_bold=True))
        # self.color_te =
        self.bw_color_int = DIM_INT
        self.update_stylesheet()

    def set_inactive(self):
        self.setFont(mc.mc_global.get_font_xlarge(i_underscore=False, i_bold=True))
        # self.setStyleSheet("background-color: black; color: #404040")
        # self.color_te = (64, 64, 64)
        self.bw_color_int = BRIGHT_INT
        self.update_stylesheet()

    def fade_in(self, i_fade_speed: int):
        self.bw_color_int -= i_fade_speed
        if self.bw_color_int < DARK_INT:
            self.bw_color_int = DARK_INT
        self.update_stylesheet()

    # Overridden
    # noinspection PyPep8Naming
    def enterEvent(self, i_QEvent):
        self.entered_signal.emit()
        logging.debug("CustomLabel: enterEvent")

    # Overridden
    # noinspection PyPep8Naming
    def mousePressEvent(self, i_QMouseEvent):
        self.pressed_signal.emit()
        logging.debug("CustomLabel: mousePressEvent")


class GraphicsView(QtWidgets.QGraphicsView):
    # Also contains the graphics scene
    def __init__(self):
        super().__init__()

        self.setFixedWidth(300)
        self.setFixedHeight(200)
        t_brush = QtGui.QBrush(QtGui.QColor(20, 100, 10))
        self.setBackgroundBrush(t_brush)
        self.setRenderHints(
            QtGui.QPainter.Antialiasing |
            QtGui.QPainter.SmoothPixmapTransform
        )
        self.setAlignment(QtCore.Qt.AlignCenter)

        self.graphics_scene = QtWidgets.QGraphicsScene()
        self.setScene(self.graphics_scene)

        t_pointf = QtCore.QPointF(0.0, 0.0)

        # Ellipse
        self.custom_gi = CustomGraphicsItem()
        self.graphics_scene.addItem(self.custom_gi)
        self.custom_gi.setPos(t_pointf)
        t_brush = QtGui.QBrush(QtGui.QColor(200, 10, 100))
        t_pen = QtGui.QPen(QtCore.Qt.NoPen)
        t_rectf = QtCore.QRectF(0.0, 0.0, 100.0, 100.0)
        # self.ellipse_gi.setRect(t_rectf)
        # self.ellipse_gi.setPen(t_pen)
        # self.ellipse_gi.setBrush(t_brush)
        self.custom_gi.setAcceptHoverEvents(True)
        # self.ellipse_gi.installSceneEventFilter(self.ellipse_gi)
        self.custom_gi.enter_signal.connect(self.start_breathing_in)
        self.custom_gi.leave_signal.connect(self.start_breathing_out)
        self.custom_gi.setTransformOriginPoint(self.custom_gi.boundingRect().center())

        # Text
        self.text_gi = QtWidgets.QGraphicsTextItem()
        self.text_gi.setPlainText("please breathe mindfully")
        self.graphics_scene.addItem(self.text_gi)
        self.text_gi.setPos(t_pointf)
        self.text_gi.setDefaultTextColor(QtGui.QColor(200, 190, 10))
        # self.setTextWidth(20)
        self.text_gi.setTransformOriginPoint(self.text_gi.boundingRect().center())

        self.ib_qtimeline = QtCore.QTimeLine(duration=4000)
        self.ib_qtimeline.setFrameRange(1, 400)
        self.ib_qtimeline.setCurveShape(QtCore.QTimeLine.EaseInOutCurve)
        self.ib_qtimeline.frameChanged.connect(self.frame_change_breathing_in)
        self.ob_qtimeline = QtCore.QTimeLine(duration=7000)
        self.ob_qtimeline.setFrameRange(1, 400)
        self.ob_qtimeline.setCurveShape(QtCore.QTimeLine.EaseInOutCurve)
        self.ob_qtimeline.frameChanged.connect(self.frame_change_breathing_out)

        self.peak_scale_ft = 1

    def frame_change_breathing_in(self, i_frame_nr_int):
        self.text_gi.setScale(1 + 0.001 * i_frame_nr_int)
        self.custom_gi.setScale(1 + 0.001 * i_frame_nr_int)
        # self.setTextWidth(self.textWidth() + 1)

    def frame_change_breathing_out(self, i_frame_nr_int):
        self.text_gi.setScale(self.peak_scale_ft - 0.001 * i_frame_nr_int)
        self.custom_gi.setScale(self.peak_scale_ft - 0.001 * i_frame_nr_int)
        # self.setTextWidth(self.textWidth() + 1)

    def start_breathing_in(self):
        self.ob_qtimeline.stop()

        self.text_gi.setPlainText("breathing in")
        self.text_gi.setTransformOriginPoint(self.text_gi.boundingRect().center())
        self.ib_qtimeline.start()

    def start_breathing_out(self):
        self.ib_qtimeline.stop()
        self.peak_scale_ft = self.text_gi.scale()

        self.text_gi.setPlainText("breathing out")
        self.text_gi.setTransformOriginPoint(self.text_gi.boundingRect().center())
        self.ob_qtimeline.start()


class CustomGraphicsItem(QtWidgets.QGraphicsObject):
    enter_signal = QtCore.pyqtSignal()
    leave_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.xpos_ft = 0.0
        self.ypos_ft = 0.0
        self.width_ft = 50.0
        self.height_ft = 50.0
        self.setAcceptHoverEvents(True)

    # Overridden
    def paint(self, i_QPainter, QStyleOptionGraphicsItem, widget=None):
        t_rectf = QtCore.QRectF(0.0, 0.0, 50.0, 50.0)
        t_brush = QtGui.QBrush(QtGui.QColor(200, 10, 100))
        i_QPainter.fillRect(t_rectf, t_brush)

    # Overridden
    def boundingRect(self):
        t_qrect = QtCore.QRectF(
            self.xpos_ft, self.ypos_ft,
            self.width_ft, self.height_ft
        )
        return t_qrect

    def hoverEnterEvent(self, i_QGraphicsSceneHoverEvent):
        self.enter_signal.emit()

    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        self.leave_signal.emit()
