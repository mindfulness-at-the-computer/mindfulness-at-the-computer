
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import mb_global
import mb_model

POINT_SIZE_INT = 11


class PhrasesCompositeWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumHeight(180)
        self.setMinimumWidth(580)

        self.practice_phrases_counter_int = 0

        self.vbox_l2 = QtWidgets.QVBoxLayout()
        self.scroll_area_w3 = QtWidgets.QScrollArea()
        self.scroll_area_w3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area_w3.setWidgetResizable(True)
        self.scroll_list_widget_w4 = QtWidgets.QWidget()
        ## self.scroll_list_widget_w4.setObjectName(MY_WIDGET_NAME_STR)
        self.scroll_list_vbox_l5 = QtWidgets.QVBoxLayout()

        self.scroll_list_widget_w4.setLayout(self.scroll_list_vbox_l5)
        self.scroll_area_w3.setWidget(self.scroll_list_widget_w4)

        self.vbox_l2.addWidget(self.scroll_area_w3)
        self.setLayout(self.vbox_l2)

        new_font = QtGui.QFont()
        new_font.setPointSize(POINT_SIZE_INT)
        hbox_l3 = QtWidgets.QHBoxLayout()
        self.vbox_l2.addLayout(hbox_l3)
        self.add_new_in_breath_text_le = QtWidgets.QLineEdit()
        self.add_new_in_breath_text_le.setFont(new_font)
        hbox_l3.addWidget(self.add_new_in_breath_text_le)
        self.add_new_out_breath_text_le = QtWidgets.QLineEdit()
        self.add_new_out_breath_text_le.setFont(new_font)
        hbox_l3.addWidget(self.add_new_out_breath_text_le)
        self.add_new_button_pb = QtWidgets.QPushButton("Add new")
        hbox_l3.addWidget(self.add_new_button_pb)
        self.add_new_button_pb.clicked.connect(self.on_add_new_button_clicked)

        self.update_gui()

    def on_add_new_button_clicked(self):
        ib_text_sg = self.add_new_in_breath_text_le.text().strip()  # strip is needed to remove a newline at the end (why?)
        if not (ib_text_sg and ib_text_sg.strip()):
            return
        ob_text_sg = self.add_new_out_breath_text_le.text().strip()  # strip is needed to remove a newline at the end (why?)
        if not (ob_text_sg and ob_text_sg.strip()):
            return

        mb_model.PhrasesM.add(mb_global.active_collection_id_it,
            9, ib_text_sg, ob_text_sg)  # -TODO: Change order

        self.add_new_in_breath_text_le.clear()
        self.add_new_out_breath_text_le.clear()
        self.update_gui()


    def update_gui(self, i_breathing_state=mb_global.BreathingState.inactive, i_update_scroll_bool=False):
        """
        :param i_breathing_state:
        :param i_update_scroll_bool: This parameter had to be added to avoid using sendPostedEvents
        in the normal case where the scroll is not changed. (Otherwise we will get flickering)
        :return:
        """
        clear_widget_and_layout_children(self.scroll_list_vbox_l5)

        scroll_to_widget = []
        phrase_list = []
        phrase_list = ["breathing in list row 1", "breathing in list row 2"]
        counter_int = 0
        scroll_to_upper_edge_int = 0
        scroll_to_lower_edge_int = 0
        frame_list = []
        for l_phrase_item in mb_model.PhrasesM.get_all_for_collection(
                mb_global.active_collection_id_it):
            frame_l6 = QtWidgets.QFrame()
            self.scroll_list_vbox_l5.addWidget(frame_l6)

            vbox_l7 = QtWidgets.QVBoxLayout()
            frame_l6.setLayout(vbox_l7)

            # frame_l6.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)

            in_breath_str = l_phrase_item.ib_str
            out_breath_str = l_phrase_item.ob_str

            new_font = QtGui.QFont()
            new_font.setPointSize(POINT_SIZE_INT)

            if self.practice_phrases_counter_int == counter_int:
                if i_breathing_state == mb_global.BreathingState.breathing_in:
                    in_breath_str = in_breath_str + " ←"
                    # -" <" doesn't work, probably because it interferes with the bold tags
                elif i_breathing_state == mb_global.BreathingState.breathing_out:
                    out_breath_str = out_breath_str + " ←"
                else:
                    pass
                new_font.setBold(True)
                #in_breath_str = "<b>" + in_breath_str + "</b>"
                #out_breath_str = "<b>" + out_breath_str + "</b>"

            ib_phrase_qll = QtWidgets.QLabel(in_breath_str)
            vbox_l7.addWidget(ib_phrase_qll)
            ob_phrase_qll = QtWidgets.QLabel(out_breath_str)
            vbox_l7.addWidget(ob_phrase_qll)

            if i_update_scroll_bool:
                if counter_int <= self.practice_phrases_counter_int:
                    QtCore.QCoreApplication.sendPostedEvents(frame_l6)
                    #frame_l6.adjustSize()
                    if counter_int < self.practice_phrases_counter_int:
                        scroll_to_upper_edge_int += frame_l6.height()
                    scroll_to_lower_edge_int += frame_l6.height()

            ib_phrase_qll.setFont(new_font)
            ob_phrase_qll.setFont(new_font)

            counter_int += 1

        if i_update_scroll_bool:
            ###self.scroll_area_w3.ensureVisible(0, scroll_to_upper_edge_int)
            self.scroll_area_w3.ensureVisible(0, scroll_to_lower_edge_int)
            # -Please note: ensureWidgetVisible does not work since there are levels between
            #  the scrollarea and the scroll vbox

        self.scroll_list_vbox_l5.addStretch()

    def next_phrase(self):
        self.practice_phrases_counter_int += 1
        self.update_gui(i_update_scroll_bool=True)


def clear_widget_and_layout_children(qlayout_or_qwidget):
    if qlayout_or_qwidget.widget():
        qlayout_or_qwidget.widget().deleteLater()
    elif qlayout_or_qwidget.layout():
        while qlayout_or_qwidget.layout().count():
            child_qlayoutitem = qlayout_or_qwidget.takeAt(0)
            clear_widget_and_layout_children(child_qlayoutitem)  # Recursive call


"""
class CustomQLabel(QtWidgets.QLabel):
    NO_DIARY_ENTRY_SELECTED = -1
    diary_entry_id = NO_DIARY_ENTRY_SELECTED
    mouse_pressed_signal = QtCore.pyqtSignal(QtGui.QMouseEvent, int)

    def __init__(self, i_text_sg, i_diary_entry_id=NO_DIARY_ENTRY_SELECTED):
        super().__init__(i_text_sg)
        self.diary_entry_id = i_diary_entry_id

    # Overridden
    # Please note that this is the event handler (not an event!)
    def mousePressEvent(self, i_qmouseevent):
        ### super(CustomQLabel, self).mousePressEvent(i_qmouseevent)
        self.mouse_pressed_signal.emit(i_qmouseevent, self.diary_entry_id)
"""
