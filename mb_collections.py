
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import mb_model
import mb_global


class CollectionsCompositeWidget(QtWidgets.QWidget):
    row_changed_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        self.setMinimumWidth(180)

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        vbox.addWidget(self.list_widget)

        self.list_widget.currentRowChanged.connect(self.on_current_row_changed)

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        self.add_to_list_le = QtWidgets.QLineEdit()
        hbox.addWidget(self.add_to_list_le)
        self.add_to_list_pb = QtWidgets.QPushButton("Add")
        self.add_to_list_pb.clicked.connect(self.add_new_collection_button_clicked)
        hbox.addWidget(self.add_to_list_pb)

        self.update_gui()

    def add_new_collection_button_clicked(self):
        text_sg = self.add_to_list_le.text().strip()  # strip is needed to remove a newline at the end (why?)
        if not (text_sg and text_sg.strip()):
            return
        mb_model.CollectionM.add(9, text_sg)  # -TODO: change 9
        self.add_to_list_le.clear()
        self.update_gui()

    def on_current_row_changed(self):
        current_row_int = self.list_widget.currentRow()
        if current_row_int != -1:
            current_question_qli = self.list_widget.item(current_row_int)
            customqlabel_widget = self.list_widget.itemWidget(current_question_qli)
            mb_global.active_question_id_it = 1  # customqlabel_widget.question_entry_id
            mb_global.active_collection_id_it = customqlabel_widget.question_entry_id

        self.row_changed_signal.emit()

    def update_gui(self):
        self.list_widget.clear()

        for l_collection in mb_model.CollectionM.get_all():
            #self.list_widget.addItem(l_collection.title_str)

            custom_label = CustomQLabel(l_collection.title_str, l_collection.id_int)
            list_item = QtWidgets.QListWidgetItem()
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, custom_label)


class CustomQLabel(QtWidgets.QLabel):
    question_entry_id = mb_global.NO_DIARY_ENTRY_SELECTED  # -"static"
    mouse_pressed_signal = QtCore.pyqtSignal(QtGui.QMouseEvent, int)

    def __init__(self, i_text_sg, i_diary_entry_id=mb_global.NO_DIARY_ENTRY_SELECTED):
        super().__init__(i_text_sg)
        self.question_entry_id = i_diary_entry_id

    # Overridden
    # Please note that this is the event handler (not an event!)
    def mousePressEvent(self, i_qmouseevent):
        super(CustomQLabel, self).mousePressEvent(i_qmouseevent)
        # -self is automatically sent as the 1st argument
        self.mouse_pressed_signal.emit(i_qmouseevent, self.question_entry_id)

