import logging
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import mc.mc_global


class ExpNotificationWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            QtCore.Qt.Window
        )
        # | QtCore.Qt.WindowStaysOnTopHint
        # | QtCore.Qt.X11BypassWindowManagerHint

        # self.setStyleSheet("background-color: rgba(0,0,0,0)")

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)
        # (left, right, top, bottom) = vbox.getContentsMargins()
        # vbox.setContentsMargins(0, 0, 5, 5)

        self.cll_one = CustomLabel("Testing exp notification widget --- 1")
        vbox.addWidget(self.cll_one)
        #self.qll_one.mouse.connect(self.on_mouse_over_one)
        self.qll_two = QtWidgets.QLabel("Testing exp notification widget")
        vbox.addWidget(self.qll_two)

        self.show()  # -done after all the widget have been added so that the right size is set

        # Set position - done after show to get the right size hint
        screen_qrect = QtWidgets.QApplication.desktop().availableGeometry()
        xpos_int = screen_qrect.left() + (screen_qrect.width() - self.sizeHint().width()) // 2
        ypos_int = screen_qrect.bottom() - self.sizeHint().height() - 50
        self.move(xpos_int, ypos_int)

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

