import logging
import time
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import mc.mc_global
import mc.model

BAR_HEIGHT_FT = 4.0
POINT_SIZE_INT = 16
GRADIENT_IN_FT = 120.0
GRADIENT_OUT_FT = 150.0


class BreathingDlg(QtWidgets.QFrame):
    close_signal = QtCore.pyqtSignal(list, list)
    phrase_changed_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.hover_and_kb_active_bool = False
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

        in_str = "-----------------"
        out_str = "-"
        if mc.mc_global.active_phrase_id_it != mc.mc_global.NO_PHRASE_SELECTED_INT:
            breathing_phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)
            in_str = breathing_phrase.ib_str
            out_str = breathing_phrase.ob_str
        self.ib_cll = CustomLabel(in_str)
        vbox_l2.addWidget(self.ib_cll, alignment=QtCore.Qt.AlignHCenter)
        self.ib_cll.entered_signal.connect(self.on_in_button_hover)
        # self.qll_one.mouse.connect(self.on_mouse_over_one)

        """
        self.hline_frame = QtWidgets.QFrame()
        vbox_l2.addWidget(self.hline_frame, alignment=QtCore.Qt.AlignHCenter)
        self.hline_frame.setFrameShape(QtWidgets.QFrame.HLine)
        self.hline_frame.setFixedWidth(100)
        """

        self.breathing_graphicsview_l3 = QtWidgets.QGraphicsView()  # QGraphicsScene
        vbox_l2.addWidget(self.breathing_graphicsview_l3)
        self.breathing_graphicsview_l3.setFixedHeight(BAR_HEIGHT_FT)  # + 2 * SMALL_MARGIN_FT
        self.breathing_graphicsview_l3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.breathing_graphicsview_l3.setAlignment(QtCore.Qt.AlignAbsolute)
        self.breathing_graphicsscene_l4 = QtWidgets.QGraphicsScene()
        self.breathing_graphicsview_l3.setScene(self.breathing_graphicsscene_l4)

        self.breathing_graphicsview_l3.hide()  # -this is removed for now

        self.ob_cll = CustomLabel(out_str)
        vbox_l2.addWidget(self.ob_cll, alignment=QtCore.Qt.AlignHCenter)
        self.ob_cll.entered_signal.connect(self.on_out_button_hover)

        hbox = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox)
        self.in_and_activate_qpb = CustomButton("activate hover")
        hbox.addWidget(self.in_and_activate_qpb)
        self.in_and_activate_qpb.clicked.connect(self.on_in_and_activate_button_clicked)
        self.in_qpb = CustomButton("In")
        hbox.addWidget(self.in_qpb)
        self.in_qpb.clicked.connect(self.on_in_button_clicked)
        self.in_qpb.entered_signal.connect(self.on_in_button_hover)
        self.out_qpb = CustomButton("Out")
        hbox.addWidget(self.out_qpb)
        self.out_qpb.clicked.connect(self.on_out_button_clicked)
        self.out_qpb.entered_signal.connect(self.on_out_button_hover)
        self.close_qpb = CustomButton("Close")
        hbox.addWidget(self.close_qpb)
        self.close_qpb.clicked.connect(self.on_close_button_clicked)
        self.close_qpb.entered_signal.connect(self.on_close_button_hover)

        self.phrases_qcb = QtWidgets.QComboBox()
        hbox.addWidget(self.phrases_qcb)
        for phrase in mc.model.PhrasesM.get_all():
            self.phrases_qcb.addItem(
                phrase.title_str,
                phrase.id_int
            )
        """
        self.phrases_qcb.addItems(
            [p.title_str for p in mc.model.PhrasesM.get_all()]
        )
        """
        self.phrases_qcb.activated.connect(self.on_phrases_combo_activated)

        self.show()  # -done after all the widget have been added so that the right size is set
        self.raise_()
        self.showNormal()

        # Set position - done after show to get the right size hint
        screen_qrect = QtWidgets.QApplication.desktop().availableGeometry()
        self.xpos_int = screen_qrect.left() + (screen_qrect.width() - self.sizeHint().width()) // 2
        self.ypos_int = screen_qrect.bottom() - self.sizeHint().height() - 50
        self.move(self.xpos_int, self.ypos_int)

        self.ib_qgri_list = []
        self.ob_qgri_list = []
        self.ib_length_int_list = []
        self.ob_length_int_list = []
        # -the lengths have to be stored separately since the qgri items are removed once
        #  they are no longer visible

        # self.start_breathing_in_timer()

        """
        cursor = QtGui.QCursor()
        cursor.setPos(xpos_int + self.width() // 2, ypos_int + self.height() // 2)
        self.setCursor(cursor)
        """
        self.start_cursor_timer()

        self.update_gui()

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

    def on_in_and_activate_button_clicked(self):
        self.hover_and_kb_active_bool = True
        self.on_in_button_clicked()

    def on_in_button_hover(self):
        if self.hover_and_kb_active_bool:
            self.on_in_button_clicked()

    def on_out_button_hover(self):
        if self.hover_and_kb_active_bool:
            self.on_out_button_clicked()

    def on_close_button_hover(self):
        if self.hover_and_kb_active_bool:
            self.on_close_button_clicked()

    def on_in_button_clicked(self):
        if (self.state == mc.mc_global.BreathingState.inactive
        or self.state == mc.mc_global.BreathingState.breathing_out):
            self.update_io_length_lists()
            self.breathing_graphicsscene_l4.clear()
            # self.breathing_graphicsview_l3.centerOn(0, 0)
            # = QtWidgets.QGraphicsView()
            # self.breathing_graphicsview_l3.resetCachedContent()
            self.breathing_in()

    def on_out_button_clicked(self):
        if self.state == mc.mc_global.BreathingState.breathing_in:
            self.breathing_out()

    def on_close_button_clicked(self):
        self.cursor_qtimer.stop()

        if len(self.ob_qgri_list) > 0:
            self.update_io_length_lists()
        self.close_signal.emit(
            self.ib_length_int_list,
            self.ob_length_int_list
        )

        self.close()

    def update_io_length_lists(self):
        if self.state == mc.mc_global.BreathingState.breathing_out and len(self.ob_qgri_list) > 0:
            if len(self.ob_qgri_list) > 0:
                self.ib_length_int_list.append(self.ib_qgri_list[-1].rect().width())
                self.ob_length_int_list.append(self.ob_qgri_list[-1].rect().width())

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
        self.ib_qgri_list.append(t_graphics_rect_item)

    def breathing_in_timer_timeout(self):
        t_graphics_rect_item = self.ib_qgri_list[-1]
        new_rect = t_graphics_rect_item.rect()
        new_rect.setLeft(new_rect.left() - 1)
        t_graphics_rect_item.setRect(new_rect)

        self.ib_cll.fade_in(2)
        # self.breathing_graphicsview_l3.centerOn(t_graphics_rect_item)

        """
        hline_width_int = self.hline_frame.width()
        if hline_width_int < 400:
            self.hline_frame.setFixedWidth(hline_width_int + 2)
        font = self.ib_cll.font()
        point_size_ft = font.pointSizeF()
        font.setPointSizeF(point_size_ft + 0.15)
        self.ib_cll.setFont(font)
        """

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

        self.ob_qgri_list.append(t_graphics_rect_item)

    def stop_breathing_out_timer(self):
        if self.ob_qtimer is None:
            return
        self.ob_qtimer.stop()
        logging.debug("Timer stopped at " + str(time.time()))

    def breathing_out_timer_timeout(self):
        t_graphics_rect_item = self.ob_qgri_list[-1]
        new_rect = t_graphics_rect_item.rect()
        new_rect.setRight(new_rect.right() + 1)
        t_graphics_rect_item.setRect(new_rect)

        self.ob_cll.fade_in(3)

        """
        hline_width_int = self.hline_frame.width()
        if hline_width_int >= 1:
            self.hline_frame.setFixedWidth(hline_width_int - 1)
        font = self.ob_cll.font()
        point_size_ft = font.pointSizeF()
        font.setPointSizeF(point_size_ft + 0.05)
        self.ob_cll.setFont(font)
        """

    def update_gui(self):
        in_str = "-----------------"
        out_str = "-"
        if mc.mc_global.active_phrase_id_it != mc.mc_global.NO_PHRASE_SELECTED_INT:
            breathing_phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)
            in_str = breathing_phrase.ib_str
            out_str = breathing_phrase.ob_str
        self.ib_cll.setText(in_str)
        self.ob_cll.setText(out_str)

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


class CustomButton(QtWidgets.QPushButton):
    entered_signal = QtCore.pyqtSignal()

    def __init__(self, i_title: str):
        super().__init__(i_title)

    # Overridden
    # noinspection PyPep8Naming
    def enterEvent(self, i_QEvent):
        self.entered_signal.emit()
        logging.debug("CustomButton: enterEvent")

