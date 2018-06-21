import random

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import mc.mc_global


class CompositeQuotesWidget(QtWidgets.QWidget):

    quote_number_int = 0
    quotes_strlist = []

    def __init__(self):
        super().__init__()

        self.quotes_strlist.append("""
The mind is the basis for everything.
Everything is created by my mind, and is ruled by my mind.
When I speak or act with impure thoughts, suffering follows me
As the wheel of the cart follows the hoof of the ox.""")
        self.quotes_strlist.append("""
The mind is the basis for everything.
Everything is created by my mind, and is ruled by my mind.
When I speak or act with a clear awareness, happiness stays with me.
Like my own shadow, it is unshakable.""")
        self.quotes_strlist.append("""
\"I was wronged! I was hurt! I was defeated! I was robbed!\"
If I cultivate such thought, I will not be free from hatred.""")
        self.quotes_strlist.append("""
\"I was wronged! I was hurt! I was defeated! I was robbed!\"
If I turn away from such thoughts, I may find peace.""")

        vbox_ql2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_ql2)
        self.quotes_label = QtWidgets.QLabel()
        vbox_ql2.addWidget(self.quotes_label)
        self.quotes_label.setWordWrap(True)
        self.quotes_label.setFont(mc.mc_global.get_font_medium())
        #self.quotes_label.setFixedWidth(240)

        hbox_ql3 = QtWidgets.QHBoxLayout()
        vbox_ql2.addLayout(hbox_ql3)

        self.prev_qpb = QtWidgets.QPushButton("Prev")
        self.random_qpb = QtWidgets.QPushButton("Random")
        self.next_qpb = QtWidgets.QPushButton("Next")

        self.prev_qpb.clicked.connect(self.on_prev_button_clicked)
        self.random_qpb.clicked.connect(self.on_random_button_clicked)
        self.next_qpb.clicked.connect(self.on_next_button_clicked)

        hbox_ql3.addWidget(self.prev_qpb)
        hbox_ql3.addWidget(self.random_qpb)
        hbox_ql3.addWidget(self.next_qpb)

        self.update_gui()

    def on_prev_button_clicked(self):
        if self.quote_number_int <= 0:
            return
        self.quote_number_int -= 1
        self.update_gui()

    def on_random_button_clicked(self):
        self.quote_number_int = random.randint(0, len(self.quotes_strlist) - 1)
        self.update_gui()

    def on_next_button_clicked(self):
        if self.quote_number_int >= len(self.quotes_strlist) - 1:
            return
        self.quote_number_int += 1
        self.update_gui()

    def update_gui(self):
        self.quotes_label.setText(self.quotes_strlist[self.quote_number_int])
        ###self.adjustSize()
