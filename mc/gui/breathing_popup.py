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
        self.keyboard_active_bool = True
        self.state = mc.mc_global.BreathingState.inactive
        self.ib_qtimer = None
        self.ob_qtimer = None
        self.setWindowFlags(
            QtCore.Qt.Popup
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
        )
        self.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.setLineWidth(1)
        # self.setStyleSheet("background-color: rgba(0,0,0,0)")
        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)
        # (left, right, top, bottom) = vbox_l2.getContentsMargins()
        # vbox_l2.setContentsMargins(0, 0, 5, 5)

        self.breathing_graphicsview_l3 = GraphicsView(self)
        vbox_l2.addWidget(self.breathing_graphicsview_l3)

        buttons_hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(buttons_hbox_l3)

        self.phrases_qcb = QtWidgets.QComboBox()
        buttons_hbox_l3.addWidget(self.phrases_qcb)
        for phrase in mc.model.PhrasesM.get_all():
            self.phrases_qcb.addItem(phrase.title_str, phrase.id_int)
        self.phrases_qcb.activated.connect(self.on_phrases_combo_activated)

        self.close_qpb = QtWidgets.QPushButton("Close")
        buttons_hbox_l3.addWidget(self.close_qpb)
        self.close_qpb.pressed.connect(self.on_close_button_clicked)
        # self.close_qpb.entered_signal.connect(self.on_close_button_hover)

        self.help_qll = QtWidgets.QLabel(
            "Hover over the central area breathing in and over the background breathing out"
        )
        vbox_l2.addWidget(self.help_qll, alignment=QtCore.Qt.AlignHCenter)
        font = self.help_qll.font()
        font.setItalic(True)
        self.help_qll.setFont(font)
        self.help_qll.setWordWrap(True)

        self.shortened_phrase_qcb = QtWidgets.QCheckBox("Use shortened")
        vbox_l2.addWidget(self.shortened_phrase_qcb)
        self.shortened_phrase_qcb.toggled.connect(self.on_shortened_phrase_toggled)

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

    def on_shortened_phrase_toggled(self):
        if self.shortened_phrase_qcb.isChecked():
            pass
        else:
            pass

    # overridden
    def keyPressEvent(self, i_qkeyevent):
        if not self.keyboard_active_bool:
            return
        if i_qkeyevent.key() == QtCore.Qt.Key_Shift:
            logging.info("shift key pressed")
            self.breathing_graphicsview_l3.start_breathing_in()
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
            self.breathing_graphicsview_l3.start_breathing_out()
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
        if QtWidgets.QApplication.mouseButtons() & QtCore.Qt.LeftButton:
            logging.debug("--------Left button--------")
        elif QtWidgets.QApplication.mouseButtons() & QtCore.Qt.NoButton:
            logging.debug("--------No button--------")
        logging.debug("int(QtWidgets.QApplication.mouseButtons()) = " + str(int(QtWidgets.QApplication.mouseButtons())))
        logging.debug("QtWidgets.QApplication.mouseButtons() = " + str(QtWidgets.QApplication.mouseButtons()))

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
        self.setStyleSheet(
            "background-color: white; color: rgb("
            + str(self.bw_color_int) + ", "
            + str(self.bw_color_int) + ", "
            + str(self.bw_color_int)
            + ")"
        )

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
    def __init__(self, i_parent):
        super().__init__()
        self.parent_obj = i_parent

        self.view_width_int = 300
        self.view_height_int = 200
        self.setFixedWidth(self.view_width_int)
        self.setFixedHeight(self.view_height_int)
        t_brush = QtGui.QBrush(QtGui.QColor(20, 100, 10))
        self.setBackgroundBrush(t_brush)
        self.setRenderHints(
            QtGui.QPainter.Antialiasing |
            QtGui.QPainter.SmoothPixmapTransform
        )
        self.setAlignment(QtCore.Qt.AlignCenter)

        self.graphics_scene = QtWidgets.QGraphicsScene()
        self.setScene(self.graphics_scene)

        # Custom dynamic breathing graphic
        self.custom_gi = BreathingGraphicsObject(self)
        self.graphics_scene.addItem(self.custom_gi)
        self.custom_gi.update_pos_and_origin_point(self.view_width_int, self.view_height_int)
        self.custom_gi.enter_signal.connect(self.start_breathing_in)
        self.custom_gi.leave_signal.connect(self.start_breathing_out)

        # Text
        self.text_gi = TextGraphicsItem()
        self.graphics_scene.addItem(self.text_gi)
        self.text_gi.setAcceptHoverEvents(False)
        # -so that the underlying item will not be disturbed
        ib_str = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it).ib_str
        # self.text_gi.setPlainText(ib_str)
        self.text_gi.setHtml(mc.mc_global.get_html(ib_str))
        self.text_gi.setTextWidth(200)
        self.text_gi.update_pos_and_origin_point(self.view_width_int, self.view_height_int)
        self.text_gi.setDefaultTextColor(QtGui.QColor(200, 190, 10))

        # Animation
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

        if self.parent_obj.shortened_phrase_qcb.isChecked():
            breathing_str = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it).ib_short_str
        else:
            breathing_str = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it).ib_str
        self.text_gi.setHtml(mc.mc_global.get_html(breathing_str))
        self.text_gi.update_pos_and_origin_point(self.view_width_int, self.view_height_int)
        self.custom_gi.update_pos_and_origin_point(self.view_width_int, self.view_height_int)
        self.ib_qtimeline.start()

    def start_breathing_out(self):
        self.ib_qtimeline.stop()
        self.peak_scale_ft = self.text_gi.scale()

        if self.parent_obj.shortened_phrase_qcb.isChecked():
            breathing_str = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it).ob_short_str
        else:
            breathing_str = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it).ob_str
        self.text_gi.setHtml(mc.mc_global.get_html(breathing_str))
        self.text_gi.update_pos_and_origin_point(self.view_width_int, self.view_height_int)
        self.custom_gi.update_pos_and_origin_point(self.view_width_int, self.view_height_int)
        self.ob_qtimeline.start()


class TextGraphicsItem(QtWidgets.QGraphicsTextItem):
    def __init__(self):
        super().__init__()

    def update_pos_and_origin_point(self, i_view_width: int, i_view_height: int):
        t_pointf = QtCore.QPointF(
            i_view_width / 2 - self.boundingRect().width() / 2,
            i_view_height / 2 - self.boundingRect().height() / 2
        )
        self.setPos(t_pointf)

        self.setTransformOriginPoint(self.boundingRect().center())


class BreathingGraphicsObject(QtWidgets.QGraphicsObject):
    enter_signal = QtCore.pyqtSignal()
    leave_signal = QtCore.pyqtSignal()

    def __init__(self, i_parent):
        super().__init__()
        self.rectf = QtCore.QRectF(0.0, 0.0, 50.0, 50.0)
        self.setAcceptHoverEvents(True)

    # Overridden
    def paint(self, i_QPainter, QStyleOptionGraphicsItem, widget=None):
        t_brush = QtGui.QBrush(QtGui.QColor(200, 10, 100))
        i_QPainter.fillRect(self.rectf, t_brush)

    # Overridden
    def boundingRect(self):
        return self.rectf

    # Overridden
    def hoverEnterEvent(self, i_QGraphicsSceneHoverEvent):
        logging.debug("hoverEnterEvent")
        self.enter_signal.emit()

    # Overridden
    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        # Please note that this function is entered in case the user hovers over something on top of this graphics item
        logging.debug("hoverLeaveEvent")

        # TODO: Check to see if the mouse is outside the bounding rectangle
        self.leave_signal.emit()

    def update_pos_and_origin_point(self, i_view_width: int, i_view_height: int):
        t_pointf = QtCore.QPointF(
            i_view_width / 2 - self.boundingRect().width() / 2,
            i_view_height / 2 - self.boundingRect().height() / 2
        )
        self.setPos(t_pointf)

        self.setTransformOriginPoint(self.boundingRect().center())

