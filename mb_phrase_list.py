
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import mb_model
import mb_global


class PhraseListCompositeWidget(QtWidgets.QWidget):
    row_changed_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)
        self.setMinimumWidth(180)

        self.list_widget = QtWidgets.QListWidget()
        #self.list_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        vbox.addWidget(self.list_widget)
        self.list_widget.currentRowChanged.connect(self.on_current_row_changed)

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        self.add_to_list_le = QtWidgets.QLineEdit()
        hbox.addWidget(self.add_to_list_le)
        self.add_new_phrase = QtWidgets.QPushButton("Add")
        self.add_new_phrase.clicked.connect(self.add_new_phrase_button_clicked)
        hbox.addWidget(self.add_new_phrase)

        # Details
        details_vbox = QtWidgets.QVBoxLayout()
        details_qgb = QtWidgets.QGroupBox("Details")
        vbox.addWidget(details_qgb)
        details_qgb.setLayout(details_vbox)

        self.breath_title_qle = QtWidgets.QLineEdit()
        details_vbox.addWidget(QtWidgets.QLabel("Title"))
        details_vbox.addWidget(self.breath_title_qle)
        self.breath_title_qle.textChanged.connect(self.details_title_text_changed)
        self.in_breath_phrase_qle = QtWidgets.QLineEdit()
        details_vbox.addWidget(QtWidgets.QLabel("In breath phrase"))
        details_vbox.addWidget(self.in_breath_phrase_qle)
        self.in_breath_phrase_qle.textChanged.connect(self.details_in_breath_text_changed)
        self.out_breath_phrase_qle = QtWidgets.QLineEdit()
        details_vbox.addWidget(QtWidgets.QLabel("Out breath phrase"))
        details_vbox.addWidget(self.out_breath_phrase_qle)
        self.out_breath_phrase_qle.textChanged.connect(self.details_out_breath_text_changed)

        self.update_gui()

    def details_title_text_changed(self):
        assert mb_global.active_phrase_id_it != mb_global.NO_PHRASE_SELECTED
        mb_model.PhrasesM.update_title(
            mb_global.active_phrase_id_it,
            self.breath_title_qle.text()
        )

    def details_in_breath_text_changed(self):
        assert mb_global.active_phrase_id_it != mb_global.NO_PHRASE_SELECTED
        mb_model.PhrasesM.update_in_breath(
            mb_global.active_phrase_id_it,
            self.in_breath_phrase_qle.text()
        )

    def details_out_breath_text_changed(self):
        assert mb_global.active_phrase_id_it != mb_global.NO_PHRASE_SELECTED
        mb_model.PhrasesM.update_out_breath(
            mb_global.active_phrase_id_it,
            self.out_breath_phrase_qle.text()
        )

    def add_new_phrase_button_clicked(self):
        text_sg = self.add_to_list_le.text().strip()  # strip is needed to remove a newline at the end (why?)
        if not (text_sg and text_sg.strip()):
            return
        mb_model.PhrasesM.add(text_sg, "Breathing in", "Breathing out")
        self.add_to_list_le.clear()
        self.update_gui()

    def on_current_row_changed(self):
        current_row_int = self.list_widget.currentRow()
        if current_row_int != -1:
            current_question_qli = self.list_widget.item(current_row_int)
            customqlabel_widget = self.list_widget.itemWidget(current_question_qli)
            mb_global.active_phrase_id_it = customqlabel_widget.question_entry_id

        self.update_gui_details()
        self.row_changed_signal.emit()

    def update_gui(self):
        # List
        self.list_widget.clear()
        for l_phrase in mb_model.PhrasesM.get_all():
            #self.list_widget.addItem(l_collection.title_str)
            custom_label = CustomQLabel(l_phrase.title_str, l_phrase.id_int)
            list_item = QtWidgets.QListWidgetItem()
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, custom_label)

        # Details
        self.update_gui_details()

    def update_gui_details(self):
        if mb_global.active_phrase_id_it != mb_global.NO_PHRASE_SELECTED:
            active_phrase = mb_model.PhrasesM.get(mb_global.active_phrase_id_it)
            self.breath_title_qle.setText(active_phrase.title_str)
            self.in_breath_phrase_qle.setText(active_phrase.ib_str)
            self.out_breath_phrase_qle.setText(active_phrase.ob_str)


class CustomQLabel(QtWidgets.QLabel):
    question_entry_id = mb_global.NO_PHRASE_SELECTED  # -"static"
    #mouse_pressed_signal = QtCore.pyqtSignal(QtGui.QMouseEvent, int)

    def __init__(self, i_text_sg, i_diary_entry_id=mb_global.NO_PHRASE_SELECTED):
        super().__init__(i_text_sg)
        self.question_entry_id = i_diary_entry_id

    """
    # Overridden
    # Please note that this is the event handler (not an event!)
    def mousePressEvent(self, i_qmouseevent):
        super(CustomQLabel, self).mousePressEvent(i_qmouseevent)
        # -self is automatically sent as the 1st argument
        #self.mouse_pressed_signal.emit(i_qmouseevent, self.question_entry_id)
    """
