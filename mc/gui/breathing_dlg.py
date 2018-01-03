import logging
import time
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import mc.mc_global
import mc.model

TIME_NOT_SET_FT = 0.0
BR_WIDTH_FT = 50.0
BR_HEIGHT_FT = 50.0


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
            QtCore.Qt.Dialog
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

        self.breath_phrase_id_list = []

        self.start_time_ft = TIME_NOT_SET_FT
        settings = mc.model.SettingsM.get()

        self.breathing_graphicsview_l3 = GraphicsView()
        vbox_l2.addWidget(self.breathing_graphicsview_l3)
        self.breathing_graphicsview_l3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.breathing_graphicsview_l3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.breathing_graphicsview_l3.ib_signal.connect(self.start_breathing_in)
        self.breathing_graphicsview_l3.ob_signal.connect(self.start_breathing_out)

        buttons_hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(buttons_hbox_l3)

        self.phrases_qcb = QtWidgets.QComboBox()
        buttons_hbox_l3.addWidget(self.phrases_qcb)
        for phrase in mc.model.PhrasesM.get_all():
            self.phrases_qcb.addItem(phrase.title, phrase.id)
        self.phrases_qcb.activated.connect(self.on_phrases_combo_activated)

        self.close_qpb = CustomPushButton(self.tr("Close"))
        buttons_hbox_l3.addWidget(self.close_qpb)
        self.close_qpb.pressed.connect(self.on_close_button_clicked)
        self.close_qpb.entered_signal.connect(self.on_close_button_entered)

        self.help_qll = QtWidgets.QLabel(
            self.tr("Hover over the central area breathing in and over the background breathing out")
        )
        vbox_l2.addWidget(self.help_qll, alignment=QtCore.Qt.AlignHCenter)
        font = self.help_qll.font()
        font.setItalic(True)
        self.help_qll.setFont(font)
        self.help_qll.setWordWrap(True)

        self.shortened_phrase_qcb = QtWidgets.QCheckBox(self.tr("Use shortened"))
        vbox_l2.addWidget(self.shortened_phrase_qcb)
        self.shortened_phrase_qcb.toggled.connect(self.on_shortened_phrase_toggled)
        using_shortened_phrase_bool = False
        if settings.breathing_reminder_phrase_setup_int == mc.mc_global.PhraseSetup.Short.value:
            using_shortened_phrase_bool = True
        self.shortened_phrase_qcb.setChecked(using_shortened_phrase_bool)
        self.shortened_phrase_qcb.hide()

        self.show()  # -done after all the widget have been added so that the right size is set
        self.raise_()
        self.showNormal()

        # Set position - done after show to get the right size hint
        screen_qrect = QtWidgets.QApplication.desktop().availableGeometry()
        self.xpos_int = screen_qrect.left() + (screen_qrect.width() - self.sizeHint().width()) // 2
        self.ypos_int = screen_qrect.bottom() - self.sizeHint().height() - 50
        self.move(self.xpos_int, self.ypos_int)

        self.ib_length_ft_list = []
        self.ob_length_ft_list = []

        # Animation
        self.ib_qtimeline = QtCore.QTimeLine(duration=10000)
        self.ib_qtimeline.setFrameRange(1, 1000)
        self.ib_qtimeline.setCurveShape(QtCore.QTimeLine.LinearCurve)
        self.ib_qtimeline.frameChanged.connect(
            self.breathing_graphicsview_l3.frame_change_breathing_in
        )
        self.ob_qtimeline = QtCore.QTimeLine(duration=20000)
        self.ob_qtimeline.setFrameRange(1, 2000)
        self.ob_qtimeline.setCurveShape(QtCore.QTimeLine.LinearCurve)
        self.ob_qtimeline.frameChanged.connect(
            self.breathing_graphicsview_l3.frame_change_breathing_out
        )

        self.start_cursor_timer()

        self.update_gui()

    def start_breathing_in(self):
        phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)
        settings = mc.model.SettingsM.get()
        self.breath_phrase_id_list.append(phrase.id)
        self.ob_qtimeline.stop()

        now = time.time()
        if self.start_time_ft != TIME_NOT_SET_FT:
            self.ob_length_ft_list.append(now - self.start_time_ft)
        self.start_time_ft = now

        are_switching_bool = settings.breathing_reminder_phrase_setup_int == mc.mc_global.PhraseSetup.Switch.value
        if are_switching_bool:
            if (
                len(self.breath_phrase_id_list) >= 2 and
                self.breath_phrase_id_list[-1] == self.breath_phrase_id_list[-2]
            ):
                self.shortened_phrase_qcb.setChecked(True)
            else:
                self.shortened_phrase_qcb.setChecked(False)
        else:
            pass

        if self.shortened_phrase_qcb.isChecked():
            breathing_str = phrase.ib_short
        else:
            breathing_str = phrase.ib
        self.breathing_graphicsview_l3.text_gi.setHtml(mc.mc_global.get_html(breathing_str))

        self.ib_qtimeline.start()

    def start_breathing_out(self):
        phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)
        self.ib_qtimeline.stop()

        now = time.time()
        self.ib_length_ft_list.append(now - self.start_time_ft)
        self.start_time_ft = now

        if self.shortened_phrase_qcb.isChecked():
            breathing_str = phrase.ob_short
        else:
            breathing_str = phrase.ob
        self.breathing_graphicsview_l3.text_gi.setHtml(mc.mc_global.get_html(breathing_str))

        self.ob_qtimeline.start()

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

    def on_close_button_entered(self):
        if len(self.breath_phrase_id_list) >= 1:
            self.on_close_button_clicked()

    def on_close_button_clicked(self):
        mc.mc_global.breathing_state = mc.mc_global.BreathingState.inactive

        if len(self.ob_length_ft_list) < len(self.ib_length_ft_list):
            now = time.time()
            self.ob_length_ft_list.append(now - self.start_time_ft)

        self.cursor_qtimer.stop()
        self.close_signal.emit(
            self.ib_length_ft_list,
            self.ob_length_ft_list
        )
        self.close()

    def update_gui(self):
        # phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)
        # in_str = phrase.ib_str
        # out_str = phrase.ob_str

        for i in range(0, self.phrases_qcb.count()):
            if self.phrases_qcb.itemData(i) == mc.mc_global.active_phrase_id_it:
                self.phrases_qcb.setCurrentIndex(i)
                break


class CustomPushButton(QtWidgets.QPushButton):
    entered_signal = QtCore.pyqtSignal()

    def __init__(self, i_title: str):
        super().__init__(i_title)

    # Overridden
    def enterEvent(self, i_qevent):
        self.entered_signal.emit()


class GraphicsView(QtWidgets.QGraphicsView):
    ib_signal = QtCore.pyqtSignal()
    ob_signal = QtCore.pyqtSignal()

    # Also contains the graphics scene
    def __init__(self):
        super().__init__()

        self.view_width_int = 330
        self.view_height_int = 160
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
        self.custom_gi = BreathingGraphicsObject()
        self.graphics_scene.addItem(self.custom_gi)
        self.custom_gi.update_pos_and_origin_point(self.view_width_int, self.view_height_int)
        self.custom_gi.enter_signal.connect(self.ib_start)
        self.custom_gi.leave_signal.connect(self.ob_start)

        # Text
        self.text_gi = TextGraphicsItem()
        self.graphics_scene.addItem(self.text_gi)
        self.text_gi.setAcceptHoverEvents(False)
        # -so that the underlying item will not be disturbed
        ib_str = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it).ib
        # self.text_gi.setPlainText(ib_str)
        self.text_gi.setHtml(mc.mc_global.get_html(ib_str))
        self.text_gi.setTextWidth(200)
        self.text_gi.update_pos_and_origin_point(self.view_width_int, self.view_height_int)
        self.text_gi.setDefaultTextColor(QtGui.QColor(200, 190, 10))

        self.peak_scale_ft = 1

    def ib_start(self):
        if mc.mc_global.breathing_state == mc.mc_global.BreathingState.breathing_in:
            return

        small_qsize = QtCore.QSizeF(BR_WIDTH_FT, BR_HEIGHT_FT)
        pos_pointf = QtWidgets.QGraphicsItem.mapFromItem(
            self.custom_gi, self.custom_gi,
            self.custom_gi.x() + (self.custom_gi.boundingRect().width() - small_qsize.width()) / 2,
            self.custom_gi.y() + (self.custom_gi.boundingRect().height() - small_qsize.height()) / 2
        )
        # -widget coords
        small_widget_coords_qrect = QtCore.QRectF(pos_pointf, small_qsize)
        # QtWidgets.QGraphicsItem

        cursor = QtGui.QCursor()  # -screen coords
        cursor_pos_widget_coords_qp = self.mapFromGlobal(cursor.pos())  # -widget coords

        logging.debug("cursor.pos() = " + str(cursor.pos()))
        logging.debug("cursor_pos_widget_coords_qp = " + str(cursor_pos_widget_coords_qp))
        logging.debug("small_widget_coords_qrect = " + str(small_widget_coords_qrect))

        if small_widget_coords_qrect.contains(cursor_pos_widget_coords_qp):
            mc.mc_global.breathing_state = mc.mc_global.BreathingState.breathing_in
            self.ib_signal.emit()
            self.text_gi.update_pos_and_origin_point(self.view_width_int, self.view_height_int)
            self.custom_gi.update_pos_and_origin_point(self.view_width_int, self.view_height_int)

    def ob_start(self):
        if mc.mc_global.breathing_state != mc.mc_global.BreathingState.breathing_in:
            return
        mc.mc_global.breathing_state = mc.mc_global.BreathingState.breathing_out

        self.peak_scale_ft = self.text_gi.scale()
        self.ob_signal.emit()
        self.text_gi.update_pos_and_origin_point(self.view_width_int, self.view_height_int)
        self.custom_gi.update_pos_and_origin_point(self.view_width_int, self.view_height_int)

    def frame_change_breathing_in(self, i_frame_nr_int):
        self.text_gi.setScale(1 + 0.001 * i_frame_nr_int)
        self.custom_gi.setScale(1 + 0.001 * i_frame_nr_int)
        # self.setTextWidth(self.textWidth() + 1)

    def frame_change_breathing_out(self, i_frame_nr_int):
        self.text_gi.setScale(self.peak_scale_ft - 0.0005 * i_frame_nr_int)
        self.custom_gi.setScale(self.peak_scale_ft - 0.0005 * i_frame_nr_int)
        # self.setTextWidth(self.textWidth() + 1)


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

    def __init__(self):
        super().__init__()
        self.rectf = QtCore.QRectF(0.0, 0.0, BR_WIDTH_FT, BR_HEIGHT_FT)
        self.setAcceptHoverEvents(True)

    # Overridden
    def paint(self, i_QPainter, QStyleOptionGraphicsItem, widget=None):
        t_brush = QtGui.QBrush(QtGui.QColor(200, 10, 100))
        i_QPainter.fillRect(self.rectf, t_brush)

    # Overridden
    def boundingRect(self):
        return self.rectf

    # Overridden
    def hoverMoveEvent(self, QGraphicsSceneHoverEvent):
        # logging.debug("hoverMoveEvent")
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

