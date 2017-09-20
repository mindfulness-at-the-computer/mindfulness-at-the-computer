import logging
import time

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from mc import model, mc_global

BAR_WIDTH_FT = 32.0
POINT_SIZE_INT = 16


class BreathingCompositeWidget(QtWidgets.QWidget):
    """
    The central window for the application
    """
    def __init__(self):
        super().__init__()
        self.show()
        ###self.setGeometry(100, 100, -1, -1)
        self.setMinimumHeight(270)
        self.setMinimumWidth(400)

        self.in_breath_length_ft = 0.0
        self.out_breath_length_ft = 0.0
        self.ib_qtimer = None
        self.ob_qtimer = None
        self.updating_gui_bool = False
        self.breath_counter_int = 0
        self.in_breath_graphics_qgri_list = []
        self.out_breath_graphics_qgri_list = []

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.help_text_qll = QtWidgets.QLabel("Please select a row from the list to the left")
        vbox_l2.addWidget(self.help_text_qll)
        help_font = QtGui.QFont()
        help_font.setItalic(True)
        self.help_text_qll.setFont(help_font)

        self.breathing_in_qfont = QtGui.QFont()
        self.breathing_in_qfont.setPointSize(POINT_SIZE_INT)
        self.breathing_out_qfont = QtGui.QFont()
        self.breathing_out_qfont.setPointSize(POINT_SIZE_INT)
        self.bi_text_qll = QtWidgets.QLabel()
        self.bo_text_qll = QtWidgets.QLabel()
        vbox_l2.addWidget(self.bi_text_qll)
        vbox_l2.addWidget(self.bo_text_qll)
        self.bi_text_qll.setFont(self.breathing_in_qfont)
        self.bo_text_qll.setFont(self.breathing_out_qfont)
        self.bi_text_qll.setWordWrap(True)
        self.bo_text_qll.setWordWrap(True)


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
        self.ib_icon_cqll = CustomIconLabel(
            mc_global.BreathingState.breathing_in,
            mc_global.get_icon_path("arrow-circle-top-4x.png")
        )
        vbox_l5.addWidget(self.ib_icon_cqll)
        self.ib_icon_cqll.widget_entered_signal.connect(self.on_icon_widget_entered)
        self.ob_icon_cqll = CustomIconLabel(
            mc_global.BreathingState.breathing_out,
            mc_global.get_icon_path("arrow-circle-bottom-4x.png")
        )
        vbox_l5.addWidget(self.ob_icon_cqll)
        self.ob_icon_cqll.widget_entered_signal.connect(self.on_icon_widget_entered)

        vbox_l5 = QtWidgets.QVBoxLayout()
        hbox_l4.addLayout(vbox_l5)
        self.ib_length_qll = QtWidgets.QLabel()
        vbox_l5.addWidget(self.ib_length_qll)
        self.ob_length_qll = QtWidgets.QLabel()
        vbox_l5.addWidget(self.ob_length_qll)







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
        ##self.breathing_graphicsview.centerOn(QtCore.Qt.AlignRight)


        self.breath_counter_qll = QtWidgets.QLabel()
        vbox_l2.addWidget(self.breath_counter_qll)


        self.update_gui()

    def on_icon_widget_entered(self, i_io_as_int: int):
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

    def pause(self):
        mc_global.breathing_state = mc_global.BreathingState.inactive
        self.stop_breathing_in_timer()
        self.stop_breathing_out_timer()
        self.breathing_in_qfont.setUnderline(False)
        self.breathing_out_qfont.setUnderline(False)

    def start_breathing_in_timer(self):
        self.breath_counter_int += 1

        self.in_breath_length_ft = 0.0

        self.ib_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.ib_qtimer.timeout.connect(self.breathing_in_timer_timeout)
        self.ib_qtimer.start(100)
        logging.info("Timer started at " + str(time.time()))

        self.update_gui()

        t_drawrect = QtCore.QRectF(
            float((self.breath_counter_int - 1) * (BAR_WIDTH_FT + 2.0)),
            0.0,
            BAR_WIDTH_FT,
            1.0
        )

        t_start_qpointf = QtCore.QPointF(t_drawrect.x(), t_drawrect.y() - 120.0)
        t_stop_qpointf = t_drawrect.bottomLeft()  # QtCore.QPointF(0.0, 50.0)
        t_linear_gradient = QtGui.QLinearGradient(t_start_qpointf, t_stop_qpointf)
        # t_linear_gradient.setColorAt(0.0, QtGui.QColor(220, 220, 220))
        # t_linear_gradient.setColorAt(1.0, QtGui.QColor(120, 120, 120))
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

    def stop_breathing_in_timer(self):
        if self.ib_qtimer is None:
            return
        self.ib_qtimer.stop()
        logging.debug("Timer stopped at " + str(time.time()))

        self.update_gui()

    def breathing_in_timer_timeout(self):
        self.in_breath_length_ft = round(self.in_breath_length_ft + 0.1, 1)
        self.update_gui()

        t_graphics_rect_item = self.in_breath_graphics_qgri_list[-1]
        new_rect = t_graphics_rect_item.rect()
        #new_rect.setHeight(new_rect.height() + 1)
        new_rect.setY(new_rect.y() - 1)
        t_graphics_rect_item.setRect(new_rect)

        self.breathing_graphicsview.centerOn(t_graphics_rect_item)

    def start_breathing_out_timer(self):
        self.out_breath_length_ft = 0.0

        self.ob_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.ob_qtimer.timeout.connect(self.breathing_out_timer_timeout)
        self.ob_qtimer.start(100)
        logging.info("Timer started at " + str(time.time()))

        self.update_gui()




        t_drawrect = QtCore.QRectF(
            float((self.breath_counter_int - 1) * (BAR_WIDTH_FT + 2.0)),
            1.0,
            BAR_WIDTH_FT,
            1.0
        )

        t_start_qpointf = QtCore.QPointF(t_drawrect.x(), t_drawrect.y() + 150.0)
        t_stop_qpointf = t_drawrect.bottomLeft()  # QtCore.QPointF(0.0, 50.0)
        t_linear_gradient = QtGui.QLinearGradient(t_start_qpointf, t_stop_qpointf)
        # t_linear_gradient.setColorAt(0.0, QtGui.QColor(230, 230, 230))
        # t_linear_gradient.setColorAt(1.0, QtGui.QColor(190, 190, 190))
        t_linear_gradient.setColorAt(0.0, QtGui.QColor(219, 255, 128))
        t_linear_gradient.setColorAt(1.0, QtGui.QColor(183, 255, 0))
        t_brush = QtGui.QBrush(t_linear_gradient)

        t_pen = QtGui.QPen(QtCore.Qt.NoPen)

        t_graphics_rect_item = self.breathing_graphicsscene.addRect(
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

        self.update_gui()

    def breathing_out_timer_timeout(self):
        self.out_breath_length_ft = round(self.out_breath_length_ft + 0.1, 1)
        self.update_gui()

        t_graphics_rect_item = self.out_breath_graphics_qgri_list[-1]
        new_rect = t_graphics_rect_item.rect()
        #new_rect.setHeight(new_rect.height() + 1)
        new_rect.setBottom(new_rect.bottom() + 1)
        t_graphics_rect_item.setRect(new_rect)

    def update_gui(self):
        self.updating_gui_bool = True

        # Buttons and shortcut descriptions
        if mc_global.breathing_state == mc_global.BreathingState.inactive:
            self.ib_toggle_qpb.setEnabled(False)
            self.ob_toggle_qpb.setEnabled(False)
            start_font = QtGui.QFont()
            start_font.setBold(True)
            self.start_pause_qpb.setText("Start")
            self.start_pause_qpb.setFont(start_font)

            # self.start_stop_shortcut_qll.setText("Press and hold shift key to start")
            # self.iob_shortcut_qll.setText("")
        else:
            self.ib_toggle_qpb.setEnabled(True)
            self.ob_toggle_qpb.setEnabled(True)
            pause_font = QtGui.QFont()
            pause_font.setBold(False)
            self.start_pause_qpb.setText("Pause")
            self.start_pause_qpb.setFont(pause_font)

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

        self.ib_length_qll.setText(str(self.in_breath_length_ft))
        self.ob_length_qll.setText(str(self.out_breath_length_ft))

        if mc_global.active_phrase_id_it != mc_global.NO_PHRASE_SELECTED_INT:
            self.help_text_qll.hide()

            active_phrase = model.PhrasesM.get(mc_global.active_phrase_id_it)

            ib_formatted_str = active_phrase.ib_str
            ob_formatted_str = active_phrase.ob_str
            if mc_global.breathing_state == mc_global.BreathingState.breathing_in:
                # ib_formatted_str += " ←"
                self.breathing_in_qfont.setUnderline(True)
                self.breathing_out_qfont.setUnderline(False)
            elif mc_global.breathing_state == mc_global.BreathingState.breathing_out:
                # ob_formatted_str += " ←"
                self.breathing_in_qfont.setUnderline(False)
                self.breathing_out_qfont.setUnderline(True)
            self.bi_text_qll.setText(ib_formatted_str)
            self.bi_text_qll.setFont(self.breathing_in_qfont)
            self.bo_text_qll.setText(ob_formatted_str)
            self.bo_text_qll.setFont(self.breathing_out_qfont)
            if ob_formatted_str:
                self.bo_text_qll.show()
            else:
                self.bo_text_qll.hide()

        self.breath_counter_qll.setText(
            "Breathing counter = " + str(self.breath_counter_int)
        )

        self.updating_gui_bool = False

    # overridden
    def keyPressEvent(self, iQKeyEvent):
        if iQKeyEvent.key() == QtCore.Qt.Key_Shift:
            logging.info("shift key pressed")

            if mc_global.breathing_state == mc_global.BreathingState.breathing_out:
                self.ib_toggle_qpb.setChecked(True)

            # self.phrase.update_gui(mb_global.BreathingState.breathing_in)
        elif iQKeyEvent.key() == QtCore.Qt.Key_Return or iQKeyEvent.key() == QtCore.Qt.Key_Enter:
            logging.info("enter or return key pressed")

            if (mc_global.breathing_state == mc_global.BreathingState.breathing_out
                    or mc_global.breathing_state == mc_global.BreathingState.breathing_in):
                self.start_pause_qpb.click()

        elif iQKeyEvent.key() == QtCore.Qt.Key_Backspace or iQKeyEvent.key() == QtCore.Qt.Key_Delete:
            logging.info("backspace or delete key pressed")

            self.stop_qpb.click()

        else:
            pass
            # super().keyPressEvent(self, iQKeyEvent)

    # overridden
    def keyReleaseEvent(self, iQKeyEvent):
        if iQKeyEvent.key() == QtCore.Qt.Key_Shift:
            logging.info("shift key released")
            if mc_global.breathing_state == mc_global.BreathingState.breathing_in:
                self.ob_toggle_qpb.setChecked(True)
        else:
            pass


class CustomIconLabel(QtWidgets.QLabel):
    widget_entered_signal = QtCore.pyqtSignal(int)  # -using mb_global.BreathingState with value

    def __init__(self, i_io: mc_global.BreathingState, i_icon_image_path: str):
        super().__init__()
        self.io_enum = i_io

        self.setPixmap(QtGui.QPixmap(i_icon_image_path))

    # Overridden
    def enterEvent(self, i_QEvent):
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
