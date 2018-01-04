import logging
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import mc.gui.safe_delete_dlg
import mc.model
import mc.mc_global

BREATHING_IN_DEFAULT_PHRASE = "Breathing in"
BREATHING_OUT_DEFAULT_PHRASE = "Breathing out"


class BreathingPhraseListWt(QtWidgets.QWidget):
    phrase_changed_signal = QtCore.pyqtSignal(bool)
    selection_changed_signal = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)
        # self.setMinimumWidth(180)

        self.updating_gui_bool = False

        self.list_widget = QtWidgets.QListWidget()
        # self.list_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        vbox.addWidget(self.list_widget)
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        self.add_to_list_qle = QtWidgets.QLineEdit()
        hbox.addWidget(self.add_to_list_qle)
        self.add_to_list_qle.setPlaceholderText(self.tr("New item"))
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.Key_Return),
            self.add_to_list_qle,
            member=self.add_new_phrase_button_clicked,
            context=QtCore.Qt.WidgetShortcut
        )

        self.add_new_phrase_qpb = QtWidgets.QPushButton(self.tr("Add"))
        self.add_new_phrase_qpb.clicked.connect(self.add_new_phrase_button_clicked)
        hbox.addWidget(self.add_new_phrase_qpb)

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)

        self.edit_texts_qpb = QtWidgets.QPushButton()
        self.edit_texts_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("pencil-2x.png")))
        self.edit_texts_qpb.setToolTip(self.tr("Edit the selected breathing phrase"))
        self.edit_texts_qpb.clicked.connect(self.on_edit_texts_clicked)
        hbox.addWidget(self.edit_texts_qpb)

        self.move_to_top_qpb = QtWidgets.QPushButton()
        self.move_to_top_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("data-transfer-upload-2x.png")))
        self.move_to_top_qpb.setToolTip(self.tr("Move the selected breathing phrase to top"))
        self.move_to_top_qpb.clicked.connect(self.on_move_to_top_clicked)
        hbox.addWidget(self.move_to_top_qpb)

        self.move_up_qpb = QtWidgets.QPushButton()
        self.move_up_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("arrow-top-2x.png")))
        self.move_up_qpb.setToolTip(self.tr("Move the selected breathing phrase up"))
        self.move_up_qpb.clicked.connect(self.on_move_up_clicked)
        hbox.addWidget(self.move_up_qpb)

        self.move_down_qpb = QtWidgets.QPushButton()
        self.move_down_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("arrow-bottom-2x.png")))
        self.move_down_qpb.setToolTip(self.tr("Move the selected breathing phrase down"))
        self.move_down_qpb.clicked.connect(self.on_move_down_clicked)
        hbox.addWidget(self.move_down_qpb)

        hbox.addStretch(1)

        self.delete_phrase_qpb = QtWidgets.QPushButton()
        self.delete_phrase_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("trash-2x.png")))
        self.delete_phrase_qpb.setToolTip(self.tr("Delete the selected breathing phrase"))
        self.delete_phrase_qpb.clicked.connect(self.on_delete_clicked)
        hbox.addWidget(self.delete_phrase_qpb)

        self.update_gui()

        self.list_widget.setCurrentRow(0)  # -the first row

    def set_button_states(self, status):
        # Disables or enables the buttons depending on breathing phrases list
        self.move_up_qpb.setDisabled(status)
        self.move_down_qpb.setDisabled(status)
        self.move_to_top_qpb.setDisabled(status)
        self.delete_phrase_qpb.setDisabled(status)
        self.edit_texts_qpb.setDisabled(status)

    def on_move_up_clicked(self):
        self.move_up_down(mc.model.MoveDirectionEnum.up)

    def on_move_down_clicked(self):
        self.move_up_down(mc.model.MoveDirectionEnum.down)

    def move_up_down(self, i_up_down: mc.model.MoveDirectionEnum):
        mc.model.PhrasesM._update_sort_order_move_up_down(
            mc.mc_global.active_phrase_id_it,
            i_up_down
        )
        self.update_gui()
        self.update_selected()

    def on_move_to_top_clicked(self):
        while True:
            result_bool = mc.model.PhrasesM._update_sort_order_move_up_down(
                mc.mc_global.active_phrase_id_it,
                mc.model.MoveDirectionEnum.up
            )
            if not result_bool:
                break
        self.update_gui()
        self.update_selected()

    def update_selected(self):
        for i in range(0, self.list_widget.count()):
            item = self.list_widget.item(i)
            phrase_qll = self.list_widget.itemWidget(item)
            logging.debug("custom_qll.entry_id = " + str(phrase_qll.entry_id))
            if phrase_qll.entry_id == mc.mc_global.active_phrase_id_it:
                item.setSelected(True)
                return

    def on_edit_texts_clicked(self):
        EditDialog.launch_edit_dialog()
        self.phrase_changed_signal.emit(True)

    def on_return_shortcut_triggered(self):
        logging.debug("the return key has been pressed")

    def on_delete_clicked(self):
        # active_phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)

        if mc.mc_global.active_phrase_id_it == mc.mc_global.NO_PHRASE_SELECTED_INT:
            # No phrase selected, nothing to delete
            logging.warning("No phrase selected")
            return

        conf_result_bool = mc.gui.safe_delete_dlg.SafeDeleteDlg.get_safe_confirmation_dialog(
            self.tr("Are you sure that you want to remove this entry?"),
        )

        if conf_result_bool:
            mc.model.PhrasesM.remove(mc.mc_global.active_phrase_id_it)
            self.list_widget.clearSelection()   # -clearing after entry removed from db
            mc.mc_global.active_phrase_id_it = mc.mc_global.NO_PHRASE_SELECTED_INT



            self.update_gui()
        else:
            pass

    def add_new_phrase_button_clicked(self):
        text_sg = self.add_to_list_qle.text().strip()  # strip is needed to remove a newline at the end (why?)
        if not (text_sg and text_sg.strip()):
            return
        mc.model.PhrasesM.add(
            text_sg,
            BREATHING_IN_DEFAULT_PHRASE,
            BREATHING_OUT_DEFAULT_PHRASE,
            "", ""
        )
        self.add_to_list_qle.clear()

        self.update_gui()
        self.list_widget.setCurrentRow(self.list_widget.count() - 1)
        # self.in_breath_phrase_qle.setFocus()

        # if dialog_result == QtWidgets.QDialog.Accepted:
        EditDialog.launch_edit_dialog()
        self.phrase_changed_signal.emit(True)

    def on_selection_changed(self):
        if self.updating_gui_bool:
            return
        selected_model_index_list = self.list_widget.selectedIndexes()
        active_selected_bool = len(selected_model_index_list) >= 1
        if active_selected_bool:
            selected_row_int = selected_model_index_list[0].row()
            # self.details_qgb.setDisabled(False)
            # TODO: setDisabled for other
            current_question_qli = self.list_widget.item(selected_row_int)
            customqlabel_widget = self.list_widget.itemWidget(current_question_qli)
            mc.mc_global.active_phrase_id_it = customqlabel_widget.entry_id
        else:
            mc.mc_global.active_phrase_id_it = mc.mc_global.NO_PHRASE_SELECTED_INT

        # self.update_gui_details()
        self.selection_changed_signal.emit(active_selected_bool)

    def on_new_row_selected_from_system_tray(self, i_id_of_selected_item: int):
        mc.mc_global.active_phrase_id_it = i_id_of_selected_item
        for i in range(0, self.list_widget.count()):
            item = self.list_widget.item(i)
            phrase_cqll = self.list_widget.itemWidget(item)
            logging.debug("phrase_cqll.entry_id = " + str(phrase_cqll.entry_id))
            if phrase_cqll.entry_id == mc.mc_global.active_phrase_id_it:
                item.setSelected(True)
                return

    def update_gui(self):
        self.updating_gui_bool = True

        # If the list is now empty, disabling buttons
        # If the list is no longer empty, enable buttons
        self.set_button_states(mc.model.PhrasesM.is_empty())

        # List
        self.list_widget.clear()
        for l_phrase in mc.model.PhrasesM.get_all():
            # self.list_widget.addItem(l_collection.title_str)
            custom_label = CustomQLabel(l_phrase.title, l_phrase.id)
            list_item = QtWidgets.QListWidgetItem()
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, custom_label)

        self.updating_gui_bool = False


class CustomQLabel(QtWidgets.QLabel):
    entry_id = mc.mc_global.NO_PHRASE_SELECTED_INT  # -"static"
    # mouse_pressed_signal = QtCore.pyqtSignal(QtGui.QMouseEvent, int)

    def __init__(self, i_text_sg, i_entry_id=mc.mc_global.NO_PHRASE_SELECTED_INT):
        super().__init__(i_text_sg)
        self.entry_id = i_entry_id

    """
    # Overridden
    # Please note that this is the event handler (not an event!)
    def mousePressEvent(self, i_qmouseevent):
        super(CustomQLabel, self).mousePressEvent(i_qmouseevent)
        # -self is automatically sent as the 1st argument
        #self.mouse_pressed_signal.emit(i_qmouseevent, self.entry_id)
    """


class EditDialog(QtWidgets.QDialog):
    """
    Inspiration: Answer by lou here:
    https://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
    """
    def __init__(self, i_parent=None):
        super(EditDialog, self).__init__(i_parent)

        # If a phrase is not selected, default to phrase with id 1
        if mc.mc_global.active_phrase_id_it == mc.mc_global.NO_PHRASE_SELECTED_INT:
            mc.mc_global.active_phrase_id_it = 1

        active_phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)

        vbox = QtWidgets.QVBoxLayout(self)

        self.breath_title_qle = QtWidgets.QLineEdit(active_phrase.title_str)
        vbox.addWidget(QtWidgets.QLabel(self.tr("Title")))
        vbox.addWidget(self.breath_title_qle)

        self.in_breath_phrase_qle = QtWidgets.QLineEdit(active_phrase.ib_str)
        vbox.addWidget(QtWidgets.QLabel(self.tr("In breath phrase")))
        vbox.addWidget(self.in_breath_phrase_qle)

        self.out_breath_phrase_qle = QtWidgets.QLineEdit(active_phrase.ob_str)
        vbox.addWidget(QtWidgets.QLabel(self.tr("Out breath phrase")))
        vbox.addWidget(self.out_breath_phrase_qle)

        self.short_in_breath_phrase_qle = QtWidgets.QLineEdit(active_phrase.ib_short_str)
        vbox.addWidget(QtWidgets.QLabel(self.tr("Short in breath phrase")))
        vbox.addWidget(self.short_in_breath_phrase_qle)

        self.short_out_breath_phrase_qle = QtWidgets.QLineEdit(active_phrase.ob_short_str)
        vbox.addWidget(QtWidgets.QLabel(self.tr("Short out breath phrase")))
        vbox.addWidget(self.short_out_breath_phrase_qle)

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
    def launch_edit_dialog():
        dialog = EditDialog()
        dialog_result = dialog.exec_()

        if dialog_result == QtWidgets.QDialog.Accepted:
            assert mc.mc_global.active_phrase_id_it != mc.mc_global.NO_PHRASE_SELECTED_INT

            phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)
            phrase.title = dialog.breath_title_qle.text()
            phrase.ib = dialog.in_breath_phrase_qle.text()
            phrase.ob = dialog.out_breath_phrase_qle.text()
            phrase.ib_short = dialog.short_in_breath_phrase_qle.text()
            phrase.ob_short = dialog.short_out_breath_phrase_qle.text()

            """
            mc.model.PhrasesM.update_title(
                mc.mc_global.active_phrase_id_it, dialog.breath_title_qle.text()
            )
            mc.model.PhrasesM.update_in_breath(
                mc.mc_global.active_phrase_id_it, dialog.in_breath_phrase_qle.text()
            )
            mc.model.PhrasesM.update_out_breath(
                mc.mc_global.active_phrase_id_it, dialog.out_breath_phrase_qle.text()
            )
            mc.model.PhrasesM.update_short_ib_phrase(
                mc.mc_global.active_phrase_id_it, dialog.short_in_breath_phrase_qle.text()
            )
            mc.model.PhrasesM.update_short_ob_phrase(
                mc.mc_global.active_phrase_id_it, dialog.short_out_breath_phrase_qle.text()
            )
            """
        else:
            pass

        return dialog_result
