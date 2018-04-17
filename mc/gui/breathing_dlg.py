import logging
import time
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import mc.mc_global
import mc.model

TIME_NOT_SET_FT = 0.0
MIN_SCALE_FT = 0.7
HISTORY_IB_MAX = 4.0
HISTORY_OB_MAX = 7.0


class BreathingDlg(QtWidgets.QFrame):
    close_signal = QtCore.pyqtSignal(list, list)
    phrase_changed_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self._hover_active_bool = False
        self._keyboard_active_bool = True
        self._cursor_qtimer = None
        self._cursor_move_active_bool = False
        self.setWindowFlags(
            QtCore.Qt.Dialog
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
        )
        self.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.setLineWidth(1)
        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)
        self._start_time_ft = TIME_NOT_SET_FT
        settings = mc.model.SettingsM.get()
        self._ib_length_ft_list = []
        self._ob_length_ft_list = []

        self._breathing_graphicsview_l3 = CustomGraphicsView()
        self._breathing_graphicsview_l3.ib_signal.connect(self._start_breathing_in)
        self._breathing_graphicsview_l3.ob_signal.connect(self._start_breathing_out)
        vbox_l2.addWidget(self._breathing_graphicsview_l3)

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)

        self._phrases_qcb = QtWidgets.QComboBox()
        for phrase in mc.model.PhrasesM.get_all():
            self._phrases_qcb.addItem(phrase.title, phrase.id)
        self._phrases_qcb.activated.connect(self._on_phrases_combo_activated)
        hbox_l3.addWidget(self._phrases_qcb)

        self._close_qpb = CustomPushButton(self.tr("Close"))
        self._close_qpb.pressed.connect(self._on_close_button_clicked)
        self._close_qpb.entered_signal.connect(self._on_close_button_entered)
        hbox_l3.addWidget(self._close_qpb)

        self._help_qll = QtWidgets.QLabel(
            self.tr("Hover over the central area breathing in and over the background breathing out")
        )
        font = self._help_qll.font()
        font.setItalic(True)
        self._help_qll.setFont(font)
        self._help_qll.setWordWrap(True)
        vbox_l2.addWidget(self._help_qll, alignment=QtCore.Qt.AlignHCenter)

        self.show()  # -done after all the widget have been added so that the right size is set
        self.raise_()
        self.showNormal()

        # Set position - done after show to get the right size hint
        screen_qrect = QtWidgets.QApplication.desktop().availableGeometry()
        self._xpos_int = screen_qrect.left() + (screen_qrect.width() - self.sizeHint().width()) // 2
        self._ypos_int = screen_qrect.bottom() - self.sizeHint().height() - 50
        self.move(self._xpos_int, self._ypos_int)

        # Animation
        self._ib_qtimeline = QtCore.QTimeLine(duration=8000)
        self._ib_qtimeline.setFrameRange(1, 1000)
        self._ib_qtimeline.setCurveShape(QtCore.QTimeLine.LinearCurve)
        self._ib_qtimeline.frameChanged.connect(
            self._breathing_graphicsview_l3.frame_change_breathing_in
        )
        self._ob_qtimeline = QtCore.QTimeLine(duration=16000)
        self._ob_qtimeline.setFrameRange(1, 2000)
        self._ob_qtimeline.setCurveShape(QtCore.QTimeLine.LinearCurve)
        self._ob_qtimeline.frameChanged.connect(
            self._breathing_graphicsview_l3.frame_change_breathing_out
        )

        self.update_gui()

    def _start_breathing_in(self):
        now = time.time()
        if self._start_time_ft != TIME_NOT_SET_FT:
            diff = now - self._start_time_ft
            if diff > HISTORY_OB_MAX:
                diff = HISTORY_OB_MAX
            self._ob_length_ft_list.append(diff)
        self._start_time_ft = now

        phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)
        self._breathing_graphicsview_l3.text_gi.setHtml(mc.mc_global.get_html(phrase.ib))

        self._ob_qtimeline.stop()
        self._ib_qtimeline.start()

    def _start_breathing_out(self):
        now = time.time()
        diff = now - self._start_time_ft
        if diff > HISTORY_IB_MAX:
            diff = HISTORY_IB_MAX
        self._ib_length_ft_list.append(diff)
        self._start_time_ft = now

        phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)
        self._breathing_graphicsview_l3.text_gi.setHtml(mc.mc_global.get_html(phrase.ob))

        self._ib_qtimeline.stop()
        self._ob_qtimeline.start()

    # overridden
    def keyPressEvent(self, i_qkeyevent):
        if not self._keyboard_active_bool:
            return
        if i_qkeyevent.key() == QtCore.Qt.Key_Shift:
            logging.info("shift key pressed")
            self._start_breathing_in()

    # overridden
    def keyReleaseEvent(self, i_qkeyevent):
        if not self._keyboard_active_bool:
            return
        if i_qkeyevent.key() == QtCore.Qt.Key_Shift:
            logging.info("shift key released")
            self._start_breathing_out()

    def _on_phrases_combo_activated(self, i_index: int):
        logging.debug("on_phrases_combo_activated, index = " + str(i_index))
        # for i in range(0, self.phrases_qcb.count() - 1):
        db_id_int = self._phrases_qcb.itemData(i_index)
        mc.mc_global.active_phrase_id_it = db_id_int
        self.phrase_changed_signal.emit()
        self.update_gui()

    def _on_close_button_entered(self):
        settings = mc.model.SettingsM.get()
        if settings.breathing_reminder_dialog_close_on_active_bool and len(self._ib_length_ft_list) >= 1:
            self._on_close_button_clicked()

    def _on_close_button_clicked(self):
        mc.mc_global.breathing_state = mc.mc_global.BreathingState.inactive

        if len(self._ob_length_ft_list) < len(self._ib_length_ft_list):
            now = time.time()
            diff = now - self._start_time_ft
            if diff > HISTORY_OB_MAX:
                diff = HISTORY_OB_MAX
            self._ob_length_ft_list.append(diff)

        self.close_signal.emit(
            self._ib_length_ft_list,
            self._ob_length_ft_list
        )  # -nice that we are able to send lists with signals!

        self._ib_qtimeline.stop()
        self._ob_qtimeline.stop()

        self.close()

    def update_gui(self):
        for i in range(0, self._phrases_qcb.count()):
            if self._phrases_qcb.itemData(i) == mc.mc_global.active_phrase_id_it:
                self._phrases_qcb.setCurrentIndex(i)
                break


class CustomPushButton(QtWidgets.QPushButton):
    entered_signal = QtCore.pyqtSignal()

    def __init__(self, i_title: str):
        super().__init__(i_title)

    # Overridden
    def enterEvent(self, i_qevent):
        self.entered_signal.emit()


VIEW_WIDTH_INT = 330
VIEW_HEIGHT_INT = 160
BR_WIDTH_FT = 50.0
BR_HEIGHT_FT = 50.0


class CustomGraphicsView(QtWidgets.QGraphicsView):
    ib_signal = QtCore.pyqtSignal()
    ob_signal = QtCore.pyqtSignal()

    # Also contains the graphics scene
    def __init__(self):
        super().__init__()
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFixedWidth(VIEW_WIDTH_INT)
        self.setFixedHeight(VIEW_HEIGHT_INT)
        t_brush = QtGui.QBrush(QtGui.QColor(mc.mc_global.MC_WHITE_COLOR_STR))
        self.setBackgroundBrush(t_brush)
        self.setRenderHints(
            QtGui.QPainter.Antialiasing |
            QtGui.QPainter.SmoothPixmapTransform
        )
        self.setAlignment(QtCore.Qt.AlignCenter)

        self._graphics_scene = QtWidgets.QGraphicsScene()
        self.setScene(self._graphics_scene)

        # Custom dynamic breathing graphic (may be possible to change this in the future)
        self._breathing_gi = BreathingGraphicsObject()
        self._graphics_scene.addItem(self._breathing_gi)
        self._breathing_gi.update_pos_and_origin_point(VIEW_WIDTH_INT, VIEW_HEIGHT_INT)
        self._breathing_gi.hover_signal.connect(self._breathing_gi_hover)
        # -Please note that for breathing in we use a static sized rectangle (instead of the one the user sees),
        # this is the reason for using "hover" instead of "enter above"
        self._breathing_gi.leave_signal.connect(self._breathing_gi_leave)

        # Text
        self.text_gi = TextGraphicsItem()
        self.text_gi.setAcceptHoverEvents(False)  # -so that the underlying item will not be disturbed
        ib_str = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it).ib
        self.text_gi.setHtml(mc.mc_global.get_html(ib_str))
        self.text_gi.setTextWidth(200)
        self.text_gi.update_pos_and_origin_point(VIEW_WIDTH_INT, VIEW_HEIGHT_INT)
        self.text_gi.setDefaultTextColor(QtGui.QColor(mc.mc_global.MC_DARKER_GREEN_COLOR_STR))
        self._graphics_scene.addItem(self.text_gi)

        self._peak_scale_ft = 1

    def _breathing_gi_hover(self):
        if mc.mc_global.breathing_state == mc.mc_global.BreathingState.breathing_in:
            return

        hover_rectangle_qsize = QtCore.QSizeF(BR_WIDTH_FT, BR_HEIGHT_FT)
        # noinspection PyCallByClass
        pos_pointf = QtWidgets.QGraphicsItem.mapFromItem(
            self._breathing_gi,
            self._breathing_gi,
            self._breathing_gi.x() + (self._breathing_gi.boundingRect().width() - hover_rectangle_qsize.width()) / 2,
            self._breathing_gi.y() + (self._breathing_gi.boundingRect().height() - hover_rectangle_qsize.height()) / 2
        )
        # -widget coords
        hover_rectangle_coords_qrect = QtCore.QRectF(pos_pointf, hover_rectangle_qsize)

        cursor = QtGui.QCursor()  # -screen coords
        cursor_pos_widget_coords_qp = self.mapFromGlobal(cursor.pos())  # -widget coords

        logging.debug("cursor.pos() = " + str(cursor.pos()))
        logging.debug("cursor_pos_widget_coords_qp = " + str(cursor_pos_widget_coords_qp))
        logging.debug("hover_rectangle_coords_qrect = " + str(hover_rectangle_coords_qrect))

        if hover_rectangle_coords_qrect.contains(cursor_pos_widget_coords_qp):
            mc.mc_global.breathing_state = mc.mc_global.BreathingState.breathing_in
            self.ib_signal.emit()
            self.text_gi.update_pos_and_origin_point(VIEW_WIDTH_INT, VIEW_HEIGHT_INT)
            self._breathing_gi.update_pos_and_origin_point(VIEW_WIDTH_INT, VIEW_HEIGHT_INT)

    def _breathing_gi_leave(self):
        if mc.mc_global.breathing_state != mc.mc_global.BreathingState.breathing_in:
            return
        mc.mc_global.breathing_state = mc.mc_global.BreathingState.breathing_out

        self._peak_scale_ft = self._breathing_gi.scale()
        self.ob_signal.emit()
        self.text_gi.update_pos_and_origin_point(VIEW_WIDTH_INT, VIEW_HEIGHT_INT)
        self._breathing_gi.update_pos_and_origin_point(VIEW_WIDTH_INT, VIEW_HEIGHT_INT)

    def frame_change_breathing_in(self, i_frame_nr_int):
        phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)
        new_scale_int_ft = 1 + 0.001 * i_frame_nr_int
        if phrase.type == mc.mc_global.BreathingPhraseType.in_out:
            self.text_gi.setScale(new_scale_int_ft)
        self._breathing_gi.setScale(new_scale_int_ft)

    def frame_change_breathing_out(self, i_frame_nr_int):
        phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)
        new_scale_int_ft = self._peak_scale_ft - 0.0005 * i_frame_nr_int
        if new_scale_int_ft < MIN_SCALE_FT:
            new_scale_int_ft = MIN_SCALE_FT
        if phrase.type == mc.mc_global.BreathingPhraseType.in_out:
            self.text_gi.setScale(new_scale_int_ft)
        self._breathing_gi.setScale(new_scale_int_ft)


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
    hover_signal = QtCore.pyqtSignal()
    leave_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.rectf = QtCore.QRectF(0.0, 0.0, BR_WIDTH_FT, BR_HEIGHT_FT)
        self.setAcceptHoverEvents(True)

    # Overridden
    def paint(self, i_qpainter, i_qstyleoptiongraphicsitem, widget=None):
        t_brush = QtGui.QBrush(QtGui.QColor(mc.mc_global.MC_LIGHT_GREEN_COLOR_STR))
        i_qpainter.fillRect(self.rectf, t_brush)

    # Overridden
    def boundingRect(self):
        return self.rectf

    # Overridden
    def hoverMoveEvent(self, i_qgraphicsscenehoverevent):
        self.hover_signal.emit()

    # Overridden
    def hoverLeaveEvent(self, i_qgraphicsscenehoverevent):
        # Please note that this function is entered in case the user hovers over something on top of this graphics item
        logging.debug("hoverLeaveEvent")
        self.leave_signal.emit()

    def update_pos_and_origin_point(self, i_view_width: int, i_view_height: int):
        t_pointf = QtCore.QPointF(
            i_view_width / 2 - self.boundingRect().width() / 2,
            i_view_height / 2 - self.boundingRect().height() / 2
        )
        self.setPos(t_pointf)

        self.setTransformOriginPoint(self.boundingRect().center())
