import logging
import time
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from mc import model, mc_global
import mc.gui.breathing_dialog

BAR_WIDTH_FT = 32.0
LARGE_MARGIN_FT = 10.0
SMALL_MARGIN_FT = 2.0
POINT_SIZE_INT = 16
GRADIENT_IN_FT = 120.0
GRADIENT_OUT_FT = 150.0


class BreathingCompositeWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.show()
        self.setMinimumHeight(270)
        self.setMinimumWidth(400)

        self.ib_qtimer = None
        self.ob_qtimer = None
        self.updating_gui_bool = False
        self.breathing_rest_counter_int = 0
        self.breath_counter_int = 0

        self.in_breath_graphics_qgri_list = []
        self.out_breath_graphics_qgri_list = []

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.help_text_qll = QtWidgets.QLabel("Please select a breathing phrase from the list to the left")
        vbox_l2.addWidget(self.help_text_qll)
        self.help_text_qll.setFont(mc_global.get_font_large(i_italics=True))

        self.bi_text_qll = CustomLabel(mc_global.BreathingState.breathing_in)
        self.bo_text_qll = CustomLabel(mc_global.BreathingState.breathing_out)
        vbox_l2.addWidget(self.bi_text_qll)
        vbox_l2.addWidget(self.bo_text_qll)
        self.bi_text_qll.setFont(mc_global.get_font_xlarge())
        self.bo_text_qll.setFont(mc_global.get_font_xlarge())
        self.bi_text_qll.setWordWrap(True)
        self.bo_text_qll.setWordWrap(True)
        self.bi_text_qll.widget_entered_signal.connect(self.on_io_widget_entered)
        self.bo_text_qll.widget_entered_signal.connect(self.on_io_widget_entered)

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)

        sps_qgb = QtWidgets.QGroupBox()
        hbox_l3.addWidget(sps_qgb)
        vbox_l4 = QtWidgets.QVBoxLayout()
        sps_qgb.setLayout(vbox_l4)
        self.start_pause_qpb = QtWidgets.QPushButton("Start")
        vbox_l4.addWidget(self.start_pause_qpb)
        # TODO: Change font
        self.start_pause_qpb.clicked.connect(self.on_start_pause_clicked)
        self.stop_qpb = QtWidgets.QPushButton("Stop/Clear")
        vbox_l4.addWidget(self.stop_qpb)
        self.stop_qpb.clicked.connect(self.on_stop_button_clicked)

        io_qgb = QtWidgets.QGroupBox()
        hbox_l3.addWidget(io_qgb)
        hbox_l4 = QtWidgets.QHBoxLayout()
        io_qgb.setLayout(hbox_l4)

        vbox_l5 = QtWidgets.QVBoxLayout()
        hbox_l4.addLayout(vbox_l5)
        # self.btn_descr_qll = QtWidgets.QLabel("In")
        self.ib_toggle_qpb = QtWidgets.QPushButton("In")
        vbox_l5.addWidget(self.ib_toggle_qpb)
        self.ib_toggle_qpb.setCheckable(True)
        self.ib_toggle_qpb.toggled.connect(self.on_ib_toggled)
        self.ob_toggle_qpb = QtWidgets.QPushButton("Out")
        vbox_l5.addWidget(self.ob_toggle_qpb)
        self.ob_toggle_qpb.setCheckable(True)
        self.ob_toggle_qpb.toggled.connect(self.on_ob_toggled)

        vbox_l5 = QtWidgets.QVBoxLayout()
        hbox_l4.addLayout(vbox_l5)
        self.ib_icon_cqll = CustomLabel(
            mc_global.BreathingState.breathing_in,
            mc_global.get_icon_path("arrow-circle-top-4x.png")
        )
        vbox_l5.addWidget(self.ib_icon_cqll)
        self.ib_icon_cqll.widget_entered_signal.connect(self.on_io_widget_entered)
        self.ob_icon_cqll = CustomLabel(
            mc_global.BreathingState.breathing_out,
            mc_global.get_icon_path("arrow-circle-bottom-4x.png")
        )
        vbox_l5.addWidget(self.ob_icon_cqll)
        self.ob_icon_cqll.widget_entered_signal.connect(self.on_io_widget_entered)

        """
        start_stop_vbox = QtWidgets.QVBoxLayout()
        hbox.addLayout(start_stop_vbox)
        start_stop_vbox.addWidget(self.start_pause_qpb)
        self.start_stop_shortcut_qll = QtWidgets.QLabel()
        start_stop_vbox.addWidget(self.start_stop_shortcut_qll)
        """

        self.breathing_graphicsview = QtWidgets.QGraphicsView()  # QGraphicsScene
        vbox_l2.addWidget(self.breathing_graphicsview)
        self.breathing_graphicsscene = QtWidgets.QGraphicsScene()
        self.breathing_graphicsview.setScene(self.breathing_graphicsscene)
        # self.breathing_graphicsview.centerOn(QtCore.Qt.AlignRight)
        # alignment can be set with "setAlignment"
        self.breathing_graphicsview.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

        self.update_gui()

    def on_io_widget_entered(self, i_io_as_int: int):
        # -breathing state is used in two different variables in this function
        if mc_global.breathing_state == mc_global.BreathingState.inactive:
            return
        io_enum_state = mc_global.BreathingState(i_io_as_int)
        logging.debug("io_enum_state = " + io_enum_state.name)
        if io_enum_state == mc_global.BreathingState.breathing_in:
            self.ib_toggle_qpb.setChecked(True)
        elif io_enum_state == mc_global.BreathingState.breathing_out:
            self.ob_toggle_qpb.setChecked(True)

    def on_start_pause_clicked(self):
        if mc_global.breathing_state == mc_global.breathing_state.inactive:
            self.breathing_in()
        else:
            self.pause()
        self.update_gui()

    def on_ib_toggled(self, i_checked: bool):
        if self.updating_gui_bool:
            return
        if i_checked:
            self.breathing_in()
        else:
            self.breathing_out()
        self.update_gui()

    def on_ob_toggled(self, i_checked: bool):
        if self.updating_gui_bool:
            return
        if i_checked:
            self.breathing_out()
        else:
            self.breathing_in()
        self.update_gui()

    def breathing_in(self):
        mc_global.breathing_state = mc_global.BreathingState.breathing_in
        self.stop_breathing_out_timer()
        self.start_breathing_in_timer()

    def breathing_out(self):
        mc_global.breathing_state = mc_global.BreathingState.breathing_out
        self.stop_breathing_in_timer()
        self.start_breathing_out_timer()

    def on_stop_button_clicked(self):
        if self.breathing_graphicsscene is None:
            return
        self.pause()
        self.in_breath_graphics_qgri_list.clear()
        self.out_breath_graphics_qgri_list.clear()
        self.breathing_graphicsscene.clear()
        self.breath_counter_int = 0
        self.breathing_rest_counter_int = 0

    def pause(self):
        self.breathing_rest_counter_int += 1
        mc_global.breathing_state = mc_global.BreathingState.inactive
        self.stop_breathing_in_timer()
        self.stop_breathing_out_timer()
        self.update_gui()

    def start_breathing_in_timer(self):
        self.breath_counter_int += 1

        self.ib_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.ib_qtimer.timeout.connect(self.breathing_in_timer_timeout)
        self.ib_qtimer.start(100)
        logging.info("Timer started at " + str(time.time()))

        self.update_gui()

        self.add_new_breathing_rect(mc_global.BreathingState.breathing_in)

        """
        xpos = float(
            (self.breathing_rest_counter_int - 1) * LARGE_MARGIN_FT
            + (self.breath_counter_int - 1) * (BAR_WIDTH_FT + SMALL_MARGIN_FT)
        )
        t_drawrect = QtCore.QRectF(xpos, 0.0, BAR_WIDTH_FT, 1.0)

        t_start_qpointf = QtCore.QPointF(t_drawrect.x(), t_drawrect.y() - GRADIENT_IN_FT)
        t_stop_qpointf = t_drawrect.bottomLeft()  # QtCore.QPointF(0.0, 50.0)
        t_linear_gradient = QtGui.QLinearGradient(t_start_qpointf, t_stop_qpointf)
        t_linear_gradient.setColorAt(0.0, QtGui.QColor(204, 255, 77))
        t_linear_gradient.setColorAt(1.0, QtGui.QColor(164, 230, 0))
        t_brush = QtGui.QBrush(t_linear_gradient)

        t_pen = QtGui.QPen(QtCore.Qt.NoPen)

        t_graphics_rect_item = self.breathing_graphicsscene.addRect(
            t_drawrect,
            pen=t_pen,
            brush=t_brush
        )
        self.in_breath_graphics_qgri_list.append(t_graphics_rect_item)
        """

    def add_new_breathing_rect(
        self,
        i_io: mc_global.BreathingState,
        i_length: int=1,
        i_vis_type: mc_global.BreathingVisType=mc_global.BreathingVisType.mainwindow_widget,
        i_margin: int=SMALL_MARGIN_FT
    ):

        if i_io == mc_global.BreathingState.breathing_in:
            self.breath_counter_int += 1

        # Rectangle
        xpos = 0
        if len(self.in_breath_graphics_qgri_list) > 0:
            last_graphics_rect_item = self.in_breath_graphics_qgri_list[-1]
            xpos = float(last_graphics_rect_item.rect().right() + i_margin)
            if i_io == mc_global.BreathingState.breathing_out:
                xpos = float(last_graphics_rect_item.rect().left())
        width_int = BAR_WIDTH_FT
        if i_vis_type == mc_global.BreathingVisType.popup_dialog:
            width_int = mc.gui.breathing_dialog.BAR_HEIGHT_FT
        ypos = -i_length
        if i_io == mc_global.BreathingState.breathing_out:
            ypos = 0.0
        t_drawrect = QtCore.QRectF(xpos, ypos, width_int, i_length)

        # Gradient
        y_gradient = t_drawrect.y() - GRADIENT_IN_FT
        if i_io == mc_global.BreathingState.breathing_out:
            y_gradient = t_drawrect.y() + GRADIENT_OUT_FT
        t_start_qpointf = QtCore.QPointF(t_drawrect.x(), y_gradient)
        t_stop_qpointf = t_drawrect.bottomLeft()  # QtCore.QPointF(0.0, 50.0)
        t_linear_gradient = QtGui.QLinearGradient(t_start_qpointf, t_stop_qpointf)
        if i_io == mc_global.BreathingState.breathing_in:
            t_linear_gradient.setColorAt(0.0, QtGui.QColor(204, 255, 77))
            t_linear_gradient.setColorAt(1.0, QtGui.QColor(164, 230, 0))
        else:
            t_linear_gradient.setColorAt(0.0, QtGui.QColor(219, 255, 128))
            t_linear_gradient.setColorAt(1.0, QtGui.QColor(183, 255, 0))

        # Adding rectangle with gradient
        t_graphics_rect_item = self.breathing_graphicsscene.addRect(
            t_drawrect,
            pen=QtGui.QPen(QtCore.Qt.NoPen),
            brush=QtGui.QBrush(t_linear_gradient)
        )
        if i_io == mc_global.BreathingState.breathing_in:
            self.in_breath_graphics_qgri_list.append(t_graphics_rect_item)
        elif i_io == mc_global.BreathingState.breathing_out:
            self.out_breath_graphics_qgri_list.append(t_graphics_rect_item)
        # -an alternative to storing this separately might be to use ".items" and check for type
        #  as there is a QGraphicsRectItem

    def stop_breathing_in_timer(self):
        if self.ib_qtimer is None:
            return
        self.ib_qtimer.stop()
        logging.debug("Timer stopped at " + str(time.time()))

        self.update_gui()

    def breathing_in_timer_timeout(self):
        t_graphics_rect_item = self.in_breath_graphics_qgri_list[-1]
        new_rect = t_graphics_rect_item.rect()
        new_rect.setY(new_rect.y() - 1)
        t_graphics_rect_item.setRect(new_rect)

        self.breathing_graphicsview.centerOn(t_graphics_rect_item)

    def start_breathing_out_timer(self):
        self.ob_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.ob_qtimer.timeout.connect(self.breathing_out_timer_timeout)
        self.ob_qtimer.start(100)
        logging.info("Timer started at " + str(time.time()))

        self.update_gui()

        self.add_new_breathing_rect(mc_global.BreathingState.breathing_out)

    def stop_breathing_out_timer(self):
        if self.ob_qtimer is None:
            return
        self.ob_qtimer.stop()
        logging.debug("Timer stopped at " + str(time.time()))

        self.update_gui()

    def breathing_out_timer_timeout(self):
        t_graphics_rect_item = self.out_breath_graphics_qgri_list[-1]
        new_rect = t_graphics_rect_item.rect()
        new_rect.setBottom(new_rect.bottom() + 1)
        t_graphics_rect_item.setRect(new_rect)

    def update_gui(self):
        self.updating_gui_bool = True

        # Buttons and shortcut descriptions
        if mc_global.breathing_state == mc_global.BreathingState.inactive:
            self.ib_toggle_qpb.setEnabled(False)
            self.ob_toggle_qpb.setEnabled(False)
            self.start_pause_qpb.setText("Start")
            self.start_pause_qpb.setFont(mc_global.get_font_medium(i_bold=True))

            # self.start_stop_shortcut_qll.setText("Press and hold shift key to start")
            # self.iob_shortcut_qll.setText("")
        else:
            self.ib_toggle_qpb.setEnabled(True)
            self.ob_toggle_qpb.setEnabled(True)
            self.start_pause_qpb.setText("Pause")
            self.start_pause_qpb.setFont(mc_global.get_font_medium())

            # self.start_stop_shortcut_qll.setText("shortcut")

            if mc_global.breathing_state == mc_global.BreathingState.breathing_in:
                # self.iob_toggle_qpb.setText("Breathing In")
                self.ib_toggle_qpb.setChecked(True)
                self.ob_toggle_qpb.setChecked(False)
                # self.iob_shortcut_qll.setText("Press and hold shift to breathe in")

            elif mc_global.breathing_state == mc_global.BreathingState.breathing_out:
                # self.iob_toggle_qpb.setText("Breathing Out")
                self.ib_toggle_qpb.setChecked(False)
                self.ob_toggle_qpb.setChecked(True)
                # self.iob_shortcut_qll.setText("Release the shift key to breathe out")

        if mc_global.active_phrase_id_it != mc_global.NO_PHRASE_SELECTED_INT:
            self.help_text_qll.hide()

            active_phrase = model.PhrasesM.get(mc_global.active_phrase_id_it)

            ib_formatted_str = active_phrase.ib_str
            ob_formatted_str = active_phrase.ob_str
            if mc_global.breathing_state == mc_global.BreathingState.breathing_in:
                # ib_formatted_str += " ←"
                self.bi_text_qll.setFont(mc_global.get_font_xlarge(i_underscore=True))
                self.bo_text_qll.setFont(mc_global.get_font_xlarge())
            elif mc_global.breathing_state == mc_global.BreathingState.breathing_out:
                # ob_formatted_str += " ←"
                self.bi_text_qll.setFont(mc_global.get_font_xlarge())
                self.bo_text_qll.setFont(mc_global.get_font_xlarge(i_underscore=True))
            elif mc_global.breathing_state == mc_global.BreathingState.inactive:
                self.bi_text_qll.setFont(mc_global.get_font_xlarge())
                self.bo_text_qll.setFont(mc_global.get_font_xlarge())
            self.bi_text_qll.setText(ib_formatted_str)
            self.bo_text_qll.setText(ob_formatted_str)
            if ob_formatted_str:
                self.bo_text_qll.show()
            else:
                self.bo_text_qll.hide()

        self.updating_gui_bool = False

    # overridden
    def keyPressEvent(self, i_qkeyevent):
        if i_qkeyevent.key() == QtCore.Qt.Key_Shift:
            logging.info("shift key pressed")

            if mc_global.breathing_state == mc_global.BreathingState.breathing_out:
                self.ib_toggle_qpb.setChecked(True)

            # self.phrase.update_gui(mb_global.BreathingState.breathing_in)
        elif i_qkeyevent.key() == QtCore.Qt.Key_Return or i_qkeyevent.key() == QtCore.Qt.Key_Enter:
            logging.info("enter or return key pressed")

            if (mc_global.breathing_state == mc_global.BreathingState.breathing_out
                    or mc_global.breathing_state == mc_global.BreathingState.breathing_in):
                self.start_pause_qpb.click()

        elif i_qkeyevent.key() == QtCore.Qt.Key_Backspace or i_qkeyevent.key() == QtCore.Qt.Key_Delete:
            logging.info("backspace or delete key pressed")

            self.stop_qpb.click()

        else:
            pass
            # super().keyPressEvent(self, iQKeyEvent)

    # overridden
    def keyReleaseEvent(self, i_qkeyevent):
        if i_qkeyevent.key() == QtCore.Qt.Key_Shift:
            logging.info("shift key released")
            if mc_global.breathing_state == mc_global.BreathingState.breathing_in:
                self.ob_toggle_qpb.setChecked(True)
        else:
            pass


class CustomLabel(QtWidgets.QLabel):
    widget_entered_signal = QtCore.pyqtSignal(int)  # -using mb_global.BreathingState with value

    def __init__(self, i_io: mc_global.BreathingState, i_icon_image_path: str=None):
        super().__init__()
        self.io_enum = i_io

        if i_icon_image_path:
            self.setPixmap(QtGui.QPixmap(i_icon_image_path))

    # Overridden
    def enterEvent(self, i_qevent):
        self.widget_entered_signal.emit(self.io_enum.value)
        logging.debug("entered " + self.io_enum.name)


"""
        t_rounded_qgi = RoundedRectGraphicsItem(0, 0, 30, 30)
        self.breathing_graphicsscene.addItem(t_rounded_qgi)

class RoundedRectGraphicsItem(QtWidgets.QGraphicsItem):
    def __init__(self, i_x_int, i_y_int, i_width_int, i_height_int):
        super().__init__()
        self.pen_width_int = 2
        self.qrectf = QtCore.QRectF(
            i_x_int - self.pen_width_int / 2,
            i_y_int - self.pen_width_int / 2,
            i_width_int + self.pen_width_int / 2,
            i_height_int + self.pen_width_int / 2
        )
        # -QRectF (with floating point numbers) is used instead of QRect, this is
        #  because the boundingRect function has to return a QRectF

    # overridden
    def boundingRect(self):
        return self.qrectf

    # overridden
    def paint(self, i_QPainter, i_Option, i_QWidget):
        i_QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        i_QPainter.setPen(QtGui.QPen(QtCore.Qt.black, self.pen_width_int))
        i_QPainter.drawRoundedRect(self.qrectf, 4, 4)

"""
