
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from mc import model, mc_global
import mc.dlg.safe_delete_dialog


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
        self.add_to_list_qle = QtWidgets.QLineEdit()
        hbox.addWidget(self.add_to_list_qle)
        # self.add_to_list_qle.setsho
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.Key_Return),
            self.add_to_list_qle,
            member=self.add_new_phrase_button_clicked,
            context=QtCore.Qt.WidgetShortcut
        )
        # QtCore.QObject.connec
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
        self.delete_phrase_qpb = QtWidgets.QPushButton("Delete")
        details_vbox.addWidget(self.delete_phrase_qpb)
        self.delete_phrase_qpb.clicked.connect(self.on_delete_clicked)

        # self.list_widget.selectAll()

        self.update_gui()

    def on_return_shortcut_triggered(self):
        print("the return key has been pressed")

    def on_delete_clicked(self):
        # active_phrase = model.PhrasesM.get(mc_global.active_phrase_id_it)
        conf_result_bool = mc.dlg.safe_delete_dialog.SafeDeleteDialog.get_safe_confirmation_dialog(
            "Are you sure that you want to remove this entry?",
        )
        if conf_result_bool:
            self.list_widget.clearSelection()
            model.PhrasesM.remove(mc_global.active_phrase_id_it)
            mc_global.active_phrase_id_it = mc_global.NO_PHRASE_SELECTED_INT
            self.update_gui()
        else:
            pass

    def details_title_text_changed(self):
        assert mc_global.active_phrase_id_it != mc_global.NO_PHRASE_SELECTED_INT
        model.PhrasesM.update_title(
            mc_global.active_phrase_id_it,
            self.breath_title_qle.text()
        )

    def details_in_breath_text_changed(self):
        assert mc_global.active_phrase_id_it != mc_global.NO_PHRASE_SELECTED_INT
        model.PhrasesM.update_in_breath(
            mc_global.active_phrase_id_it,
            self.in_breath_phrase_qle.text()
        )

    def details_out_breath_text_changed(self):
        assert mc_global.active_phrase_id_it != mc_global.NO_PHRASE_SELECTED_INT
        model.PhrasesM.update_out_breath(
            mc_global.active_phrase_id_it,
            self.out_breath_phrase_qle.text()
        )

    def add_new_phrase_button_clicked(self):
        text_sg = self.add_to_list_qle.text().strip()  # strip is needed to remove a newline at the end (why?)
        if not (text_sg and text_sg.strip()):
            return
        model.PhrasesM.add(text_sg, "Breathing in", "Breathing out")
        self.add_to_list_qle.clear()
        self.update_gui()
        self.list_widget.setCurrentRow(self.list_widget.count() - 1)
        self.in_breath_phrase_qle.setFocus()

    def on_current_row_changed(self):
        current_row_int = self.list_widget.currentRow()
        if current_row_int != -1:
            current_question_qli = self.list_widget.item(current_row_int)
            customqlabel_widget = self.list_widget.itemWidget(current_question_qli)
            mc_global.active_phrase_id_it = customqlabel_widget.question_entry_id
        else:
            raise Exception("We should not be able to deselect")

        self.update_gui_details()
        self.row_changed_signal.emit()



    def update_gui(self):
        # List
        self.list_widget.clear()
        for l_phrase in model.PhrasesM.get_all():
            #self.list_widget.addItem(l_collection.title_str)
            custom_label = CustomQLabel(l_phrase.title_str, l_phrase.id_int)
            list_item = QtWidgets.QListWidgetItem()
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, custom_label)

        # Details
        self.update_gui_details()

    def update_gui_details(self):
        if mc_global.active_phrase_id_it != mc_global.NO_PHRASE_SELECTED_INT:
            active_phrase = model.PhrasesM.get(mc_global.active_phrase_id_it)
            self.breath_title_qle.setText(active_phrase.title_str)
            self.in_breath_phrase_qle.setText(active_phrase.ib_str)
            self.out_breath_phrase_qle.setText(active_phrase.ob_str)


class CustomQLabel(QtWidgets.QLabel):
    question_entry_id = mc_global.NO_PHRASE_SELECTED_INT  # -"static"
    #mouse_pressed_signal = QtCore.pyqtSignal(QtGui.QMouseEvent, int)

    def __init__(self, i_text_sg, i_diary_entry_id=mc_global.NO_PHRASE_SELECTED_INT):
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
