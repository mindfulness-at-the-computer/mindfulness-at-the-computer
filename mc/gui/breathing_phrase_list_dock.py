
import logging

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import mc.gui.safe_delete_dialog
import mc.model
import mc.mc_global

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
        # self.list_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
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

        """
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
        """


        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)

        """
        self.add_new_texts_qpb = QtWidgets.QPushButton()
        hbox.addWidget(self.add_new_texts_qpb)
        self.add_new_texts_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("plus-2x.png")))
        self.add_new_texts_qpb.clicked.connect(self.on_edit_texts_clicked)
        """
        self.edit_texts_qpb = QtWidgets.QPushButton()
        hbox.addWidget(self.edit_texts_qpb)
        self.edit_texts_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("pencil-2x.png")))
        self.edit_texts_qpb.clicked.connect(self.on_edit_texts_clicked)
        self.move_to_top_qpb = QtWidgets.QPushButton()
        hbox.addWidget(self.move_to_top_qpb)
        self.move_to_top_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("data-transfer-upload-2x.png")))
        self.move_to_top_qpb.clicked.connect(self.on_move_to_top_clicked)
        self.move_up_qpb = QtWidgets.QPushButton()
        hbox.addWidget(self.move_up_qpb)
        self.move_up_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("arrow-top-2x.png")))
        self.move_up_qpb.clicked.connect(self.on_move_up_clicked)
        self.move_down_qpb = QtWidgets.QPushButton()
        hbox.addWidget(self.move_down_qpb)
        self.move_down_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("arrow-bottom-2x.png")))
        self.move_down_qpb.clicked.connect(self.on_move_down_clicked)


        hbox.addStretch(1)

        self.delete_phrase_qpb = QtWidgets.QPushButton()
        hbox.addWidget(self.delete_phrase_qpb)
        self.delete_phrase_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("trash-2x.png")))
        self.delete_phrase_qpb.clicked.connect(self.on_delete_clicked)


        # self.list_widget.selectAll()

        self.update_gui()

    def on_move_up_clicked(self):
        self.move_up_down(model.MoveDirectionEnum.up)

    def on_move_down_clicked(self):
        self.move_up_down(model.MoveDirectionEnum.down)

    def move_up_down(self, i_up_down: mc.model.MoveDirectionEnum):
        id_int = mc_global.active_rest_action_id_it
        model.RestActionsM.update_sort_order_move_up_down(id_int, i_up_down)
        self.update_gui()
        self.update_selected()

    def on_move_to_top_clicked(self):
        id_int = mc_global.active_rest_action_id_it
        while True:
            result_bool = model.RestActionsM.update_sort_order_move_up_down(
                id_int,
                model.MoveDirectionEnum.up
            )
            if not result_bool:
                break
        self.update_gui()
        self.update_selected()

    def on_edit_texts_clicked(self):
        edit_dialog_result_tuple = EditDialog.get_edit_dialog()
        if edit_dialog_result_tuple[0]:
            assert mc_global.active_phrase_id_it != mc_global.NO_PHRASE_SELECTED_INT
            model.PhrasesM.update_title(
                mc_global.active_phrase_id_it,
                self.breath_title_qle.text()
            )
            model.PhrasesM.update_in_breath(
                mc_global.active_phrase_id_it,
                self.in_breath_phrase_qle.text()
            )
            model.PhrasesM.update_out_breath(
                mc_global.active_phrase_id_it,
                self.out_breath_phrase_qle.text()
            )
            self.phrases_updated_signal.emit(True)
        else:
            pass
        """
        text_str = QtWidgets.QInputDialog.getText(
            self,
            "title",
            "label"
        )
        """

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
        active_selected_bool = len(selected_modelindexlist) >= 1
        if active_selected_bool:
            selected_row_int = selected_modelindexlist[0].row()
            # self.details_qgb.setDisabled(False)
            # TODO: setDisabled for other
            current_question_qli = self.list_widget.item(selected_row_int)
            customqlabel_widget = self.list_widget.itemWidget(current_question_qli)
            mc.mc_global.active_phrase_id_it = customqlabel_widget.question_entry_id
        else:
            mc.mc_global.active_phrase_id_it = mc.mc_global.NO_PHRASE_SELECTED_INT

        # self.update_gui_details()
        self.phrases_updated_signal.emit(active_selected_bool)
        # TODO:

    def on_new_row_selected_from_system_tray(self, i_id_of_selected_item: int):
        mc.mc_global.active_phrase_id_it = i_id_of_selected_item
        for i in range(0, self.list_widget.count()):
            item = self.list_widget.item(i)
            phrase_cqll = self.list_widget.itemWidget(item)
            logging.debug("phrase_cqll.question_entry_id = " + str(phrase_cqll.question_entry_id))
            if phrase_cqll.question_entry_id == mc.mc_global.active_phrase_id_it:
                item.setSelected(True)
                return

    def update_gui(self):
        # List
        self.list_widget.clear()
        for l_phrase in mc.model.PhrasesM.get_all():
            # self.list_widget.addItem(l_collection.title_str)
            custom_label = CustomQLabel(l_phrase.title_str, l_phrase.id_int)
            list_item = QtWidgets.QListWidgetItem()
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, custom_label)


class CustomQLabel(QtWidgets.QLabel):
    question_entry_id = mc.mc_global.NO_PHRASE_SELECTED_INT  # -"static"
    # mouse_pressed_signal = QtCore.pyqtSignal(QtGui.QMouseEvent, int)

    def __init__(self, i_text_sg, i_diary_entry_id=mc.mc_global.NO_PHRASE_SELECTED_INT):
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


class EditDialog(QtWidgets.QDialog):
    """
    Inspiration: Answer by lou here:
    https://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
    """
    def __init__(self, i_parent = None):
        super(EditDialog, self).__init__(i_parent)

        assert mc.mc_global.active_phrase_id_it != mc.mc_global.NO_PHRASE_SELECTED_INT
        active_phrase = model.PhrasesM.get(mc.mc_global.active_phrase_id_it)

        vbox = QtWidgets.QVBoxLayout(self)

        self.breath_title_qle = QtWidgets.QLineEdit(active_phrase.title_str)
        vbox.addWidget(QtWidgets.QLabel("Title"))
        vbox.addWidget(self.breath_title_qle)
        self.in_breath_phrase_qle = QtWidgets.QLineEdit(active_phrase.ib_str)
        vbox.addWidget(QtWidgets.QLabel("In breath phrase"))
        vbox.addWidget(self.in_breath_phrase_qle)
        self.out_breath_phrase_qle = QtWidgets.QLineEdit(active_phrase.ob_str)
        vbox.addWidget(QtWidgets.QLabel("Out breath phrase"))
        vbox.addWidget(self.out_breath_phrase_qle)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )
        vbox.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        # -accept and reject are "slots" built into Qt

    @staticmethod
    def get_edit_dialog():
        dialog = EditDialog()
        dialog_result = dialog.exec_()

        confirmation_result_bool = False
        if dialog_result == QtWidgets.QDialog.Accepted:
            confirmation_result_bool = True
        edit_tuple = (
            dialog.breath_title_qle.text(),
            dialog.in_breath_phrase_qle.text(),
            dialog.out_breath_phrase_qle.text()
        )

        ret_tuple = (confirmation_result_bool, edit_tuple)
        return ret_tuple

