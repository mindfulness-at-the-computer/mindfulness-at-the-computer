
import logging

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import mc.gui.safe_delete_dlg
from mc import model, mc_global

BREATHING_IN_DEFAULT_PHRASE = "Breathing in"
BREATHING_OUT_DEFAULT_PHRASE = "Breathing out"


class PhraseListCompositeWidget(QtWidgets.QWidget):
    phrases_updated_signal = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)
        self.setMinimumWidth(180)

        self.list_widget = QtWidgets.QListWidget()
        #self.list_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        vbox.addWidget(self.list_widget)
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)

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
        self.add_new_phrase_qpb = QtWidgets.QPushButton("Add")
        self.add_new_phrase_qpb.clicked.connect(self.add_new_phrase_button_clicked)
        hbox.addWidget(self.add_new_phrase_qpb)

        # Details
        details_vbox = QtWidgets.QVBoxLayout()
        self.details_qgb = QtWidgets.QGroupBox("Details")
        vbox.addWidget(self.details_qgb)
        self.details_qgb.setLayout(details_vbox)
        self.details_qgb.setDisabled(True)

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
        logging.debug("the return key has been pressed")

    def on_delete_clicked(self):
        # active_phrase = model.PhrasesM.get(mc_global.active_phrase_id_it)
        conf_result_bool = mc.gui.safe_delete_dlg.SafeDeleteDialog.get_safe_confirmation_dialog(
            "Are you sure that you want to remove this entry?",
        )
        if conf_result_bool:
            if mc_global.active_phrase_id_it == mc_global.NO_PHRASE_SELECTED_INT:
                logging.warning("No phrase selected")
            model.PhrasesM.remove(mc_global.active_phrase_id_it)
            self.list_widget.clearSelection()  # -clearing after entry removed from db
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
        self.phrases_updated_signal.emit(self.details_qgb.isEnabled())

    def details_out_breath_text_changed(self):
        assert mc_global.active_phrase_id_it != mc_global.NO_PHRASE_SELECTED_INT
        model.PhrasesM.update_out_breath(
            mc_global.active_phrase_id_it,
            self.out_breath_phrase_qle.text()
        )
        self.phrases_updated_signal.emit(self.details_qgb.isEnabled())

    def add_new_phrase_button_clicked(self):
        text_sg = self.add_to_list_qle.text().strip()  # strip is needed to remove a newline at the end (why?)
        if not (text_sg and text_sg.strip()):
            return
        model.PhrasesM.add(text_sg, BREATHING_IN_DEFAULT_PHRASE, BREATHING_OUT_DEFAULT_PHRASE)
        self.add_to_list_qle.clear()
        self.update_gui()
        self.list_widget.setCurrentRow(self.list_widget.count() - 1)
        self.in_breath_phrase_qle.setFocus()

    def on_selection_changed(self):
        selected_modelindexlist = self.list_widget.selectedIndexes()
        if len(selected_modelindexlist) >= 1:
            selected_row_int = selected_modelindexlist[0].row()
            self.details_qgb.setDisabled(False)
            current_question_qli = self.list_widget.item(selected_row_int)
            customqlabel_widget = self.list_widget.itemWidget(current_question_qli)
            mc_global.active_phrase_id_it = customqlabel_widget.question_entry_id
        else:
            self.details_qgb.setDisabled(True)
            mc_global.active_phrase_id_it = mc_global.NO_PHRASE_SELECTED_INT

        self.update_gui_details()
        self.phrases_updated_signal.emit(self.details_qgb.isEnabled())

    def on_new_row_selected_from_system_tray(self, i_id_of_selected_item: int):
        mc_global.active_phrase_id_it = i_id_of_selected_item
        for i in range(0, self.list_widget.count()):
            item = self.list_widget.item(i)
            phrase_cqll = self.list_widget.itemWidget(item)
            logging.debug("phrase_cqll.question_entry_id = " + str(phrase_cqll.question_entry_id))
            if phrase_cqll.question_entry_id == mc_global.active_phrase_id_it:
                item.setSelected(True)
                return

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
