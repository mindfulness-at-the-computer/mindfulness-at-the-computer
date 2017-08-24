import logging
import time
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import mb_model
import mb_global

BAR_WIDTH_FT = 16.0


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

        self.breath_counter_int = 0
        self.in_breath_graphics_qgri_list = []
        self.out_breath_graphics_qgri_list = []

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        breathing_qfont = QtGui.QFont()
        breathing_qfont.setPointSize(17)
        self.bi_text_qll = QtWidgets.QLabel()
        self.bo_text_qll = QtWidgets.QLabel()
        vbox_l2.addWidget(self.bi_text_qll)
        vbox_l2.addWidget(self.bo_text_qll)
        self.bi_text_qll.setFont(breathing_qfont)
        self.bo_text_qll.setFont(breathing_qfont)

        hbox = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox)
        self.start_stop_toggle_qpb = QtWidgets.QPushButton()
        # https://ux.stackexchange.com/questions/1318/should-a-toggle-button-show-its-current-state-or-the-state-to-which-it-will-chan
        self.start_stop_toggle_qpb.setCheckable(True)
        self.start_stop_toggle_qpb.toggled.connect(self.on_start_stop_toggled)
        self.iob_toggle_qpb = QtWidgets.QPushButton()
        self.iob_toggle_qpb.setCheckable(True)
        self.iob_toggle_qpb.toggled.connect(self.on_iob_toggled)

        start_stop_vbox = QtWidgets.QVBoxLayout()
        hbox.addLayout(start_stop_vbox)
        start_stop_vbox.addWidget(self.start_stop_toggle_qpb)
        self.start_stop_shortcut_qll = QtWidgets.QLabel()
        start_stop_vbox.addWidget(self.start_stop_shortcut_qll)

        iob_vbox = QtWidgets.QVBoxLayout()
        hbox.addLayout(iob_vbox)
        iob_vbox.addWidget(self.iob_toggle_qpb)
        self.iob_shortcut_qll = QtWidgets.QLabel()
        iob_vbox.addWidget(self.iob_shortcut_qll)

        self.ib_length_qll = QtWidgets.QLabel()
        vbox_l2.addWidget(self.ib_length_qll)
        self.ob_length_qll = QtWidgets.QLabel()
        vbox_l2.addWidget(self.ob_length_qll)

        self.breathing_graphicsview = QtWidgets.QGraphicsView()  # QGraphicsScene
        vbox_l2.addWidget(self.breathing_graphicsview)

        self.breathing_graphicsscene = QtWidgets.QGraphicsScene()
        self.breathing_graphicsview.setScene(self.breathing_graphicsscene)

        self.update_gui()

    def on_start_stop_toggled(self, i_checked: bool):
        if i_checked:
            self.iob_toggle_qpb.toggle()
            # TODO
        else:
            self.stop()

    def on_iob_toggled(self, i_checked: bool):
        if i_checked:
            mb_global.breathing_state = mb_global.BreathingState.breathing_in
            self.stop_breathing_out_timer()
            self.start_breathing_in_timer()
        else:
            mb_global.breathing_state = mb_global.BreathingState.breathing_out
            self.stop_breathing_in_timer()
            self.start_breathing_out_timer()

    def stop_and_clear(self):
        self.stop()
        self.in_breath_graphics_qgri_list.clear()
        self.out_breath_graphics_qgri_list.clear()
        self.breathing_graphicsscene.clear()

    def stop(self):
        mb_global.breathing_state = mb_global.BreathingState.inactive
        self.stop_breathing_in_timer()
        self.stop_breathing_out_timer()

    def start_breathing_in_timer(self):
        self.in_breath_length_ft = 0.0

        self.ib_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.ib_qtimer.timeout.connect(self.breathing_in_timer_timeout)
        self.ib_qtimer.start(100)
        logging.info("Timer started at " + str(time.time()))

        self.update_gui()

        t_graphics_rect_item = self.breathing_graphicsscene.addRect(QtCore.QRectF(
            float(self.breath_counter_int * (BAR_WIDTH_FT + 2.0)), 0.0, BAR_WIDTH_FT, 1.0
        ))
        self.in_breath_graphics_qgri_list.append(t_graphics_rect_item)

    def stop_breathing_in_timer(self):
        if self.ib_qtimer is None:
            return
        self.ib_qtimer.stop()
        print("Timer stopped at " + str(time.time()))

        self.update_gui()

    def breathing_in_timer_timeout(self):
        self.in_breath_length_ft = round(self.in_breath_length_ft + 0.1, 1)
        self.update_gui()

        t_graphics_rect_item = self.in_breath_graphics_qgri_list[-1]
        new_rect = t_graphics_rect_item.rect()
        #new_rect.setHeight(new_rect.height() + 1)
        new_rect.setY(new_rect.y() - 1)
        t_graphics_rect_item.setRect(new_rect)

    def start_breathing_out_timer(self):
        self.out_breath_length_ft = 0.0

        self.ob_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.ob_qtimer.timeout.connect(self.breathing_out_timer_timeout)
        self.ob_qtimer.start(100)
        logging.info("Timer started at " + str(time.time()))

        self.update_gui()

        t_graphics_rect_item = self.breathing_graphicsscene.addRect(QtCore.QRectF(
            float(self.breath_counter_int * (BAR_WIDTH_FT + 2.0)), 1.0, BAR_WIDTH_FT, 1.0
        ))

        self.out_breath_graphics_qgri_list.append(t_graphics_rect_item)
        self.breath_counter_int += 1

    def stop_breathing_out_timer(self):
        if self.ob_qtimer is None:
            return
        self.ob_qtimer.stop()
        print("Timer stopped at " + str(time.time()))

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

        # Buttons and shortcut descriptions
        if mb_global.breathing_state == mb_global.BreathingState.inactive:
            self.iob_toggle_qpb.setEnabled(False)
            self.iob_toggle_qpb.setText("In / Out")
            self.start_stop_toggle_qpb.setText("Stopped")

            self.start_stop_shortcut_qll.setText("Press and hold shift key to start")
            self.iob_shortcut_qll.setText("")
        else:
            self.iob_toggle_qpb.setEnabled(True)
            self.start_stop_toggle_qpb.setText("Started")

            self.start_stop_shortcut_qll.setText("shortcut")

            if mb_global.breathing_state == mb_global.BreathingState.breathing_in:
                self.iob_toggle_qpb.setText("Breathing In")

                self.iob_shortcut_qll.setText("Press and hold shift to breathe in")

            elif mb_global.breathing_state == mb_global.BreathingState.breathing_out:
                self.iob_toggle_qpb.setText("Breathing Out")

                self.iob_shortcut_qll.setText("Release the shift key to breathe out")

        self.ib_length_qll.setText(str(self.in_breath_length_ft))
        self.ob_length_qll.setText(str(self.out_breath_length_ft))

        if mb_global.active_phrase_id_it != mb_global.NO_PHRASE_SELECTED:
            active_phrase = mb_model.PhrasesM.get(mb_global.active_phrase_id_it)

            ib_formatted_str = active_phrase.ib_str
            ob_formatted_str = active_phrase.ob_str
            if mb_global.breathing_state == mb_global.BreathingState.breathing_in:
                ib_formatted_str += " ←"
            elif mb_global.breathing_state == mb_global.BreathingState.breathing_out:
                ob_formatted_str += " ←"
            self.bi_text_qll.setText(ib_formatted_str)
            self.bo_text_qll.setText(ob_formatted_str)

    # overridden
    def keyPressEvent(self, iQKeyEvent):
        if iQKeyEvent.key() == QtCore.Qt.Key_Shift:
            logging.info("shift key pressed")

            self.iob_toggle_qpb.setChecked(True)

            # self.phrase.update_gui(mb_global.BreathingState.breathing_in)
        elif iQKeyEvent.key() == QtCore.Qt.Key_Return or iQKeyEvent.key() == QtCore.Qt.Key_Enter:
            logging.info("enter or return key pressed")
            self.stop()
            # TODO: Fix this using toggle/setChecked

        elif iQKeyEvent.key() == QtCore.Qt.Key_Backspace or iQKeyEvent.key() == QtCore.Qt.Key_Delete:
            logging.info("backspace or delete key pressed")
            self.stop_and_clear()
            # TODO: Fix this using toggle/setChecked

        else:
            pass
            # super().keyPressEvent(self, iQKeyEvent)

    # overridden
    def keyReleaseEvent(self, iQKeyEvent):
        if iQKeyEvent.key() == QtCore.Qt.Key_Shift:
            logging.info("shift key released")
            # self.breathing_out()

            self.iob_toggle_qpb.setChecked(False)

            #self.breathing_composite_widget.update_gui(mb_global.BreathingState.breathing_out)
        else:
            pass
            # QtWidgets.QMainWindow
            # super().keyPressEvent(self, iQKeyEvent)


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
