
import sys
import logging
import time
import enum

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


BAR_WIDTH_FT = 16.0


class BreathingCompositeWidget(QtWidgets.QWidget):

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


        ##hbox_widget = QtWidgets.QWidget()
        ##self..setCentralWidget(hbox_widget)
        hbox = QtWidgets.QHBoxLayout()
        self.setLayout(hbox)

        vbox = QtWidgets.QVBoxLayout()
        hbox.addLayout(vbox)

        self.ib_qll = QtWidgets.QLabel()
        vbox.addWidget(self.ib_qll)
        self.ob_qll = QtWidgets.QLabel()
        vbox.addWidget(self.ob_qll)


        self.breathing_graphicsview = QtWidgets.QGraphicsView()  # QGraphicsScene
        vbox.addWidget(self.breathing_graphicsview)

        self.breathing_graphicsscene = QtWidgets.QGraphicsScene()
        self.breathing_graphicsview.setScene(self.breathing_graphicsscene)

        #self.breathing_graphicsscene.addText("Breathing in i know i am breathing in, breathing out")
        #self.breathing_graphicsscene.

        self.update_gui()

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
        #self.breath_counter_int += 1

    def stop_breathing_in_timer(self):
        if self.ib_qtimer is None:
            return
        #self.in_breath_length_ft += round(self.ib_qtimer.remainingTime() / 1000, 1)
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

        """
        t_rounded_qgi = RoundedRectGraphicsItem(0, 0, 30, 30)
        self.breathing_graphicsscene.addItem(t_rounded_qgi)
        """

    def stop_breathing_out_timer(self):
        if self.ob_qtimer is None:
            return
        #self.out_breath_length_ft += round(self.ob_qtimer.remainingTime() / 1000, 1)
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
        self.ib_qll.setText(str(self.in_breath_length_ft))
        self.ob_qll.setText(str(self.out_breath_length_ft))


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


