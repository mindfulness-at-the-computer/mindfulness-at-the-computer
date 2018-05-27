import logging
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import mc.gui.safe_delete_dlg
import mc.gui.warning_dlg
import mc.model
from mc import mc_global
from mc.gui.reusable_components import PushButton, PhrasesList

BREATHING_IN_DEFAULT_PHRASE = "Breathing in"
BREATHING_OUT_DEFAULT_PHRASE = "Breathing out"
BREATHING_IN_DEFAULT_SHORT_PHRASE = "in"
BREATHING_OUT_DEFAULT_SHORT_PHRASE = "out"


class BreathingPhraseListWt(QtWidgets.QWidget):
    phrase_changed_signal = QtCore.pyqtSignal(bool)
    selection_changed_signal = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.updating_gui_bool = False
        self.edit_dialog = None

        self.list_widget = PhrasesList()
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)

        self.add_to_list_qle = QtWidgets.QLineEdit()
        self.add_to_list_qle.setObjectName("add_to_list_qle")
        self.add_to_list_qle.setPlaceholderText(self.tr("New item"))
        self.add_to_list_qle.setFixedWidth(305)
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.Key_Return),
            self.add_to_list_qle,
            member=self.add_new_phrase_button_clicked,
            context=QtCore.Qt.WidgetShortcut
        )

        self.add_new_phrase_qpb = PushButton(self.tr("Add"))
        self.add_new_phrase_qpb.setFixedWidth(75)
        self.add_new_phrase_qpb.clicked.connect(self.add_new_phrase_button_clicked)
        add_new_phrase_qhl = QtWidgets.QHBoxLayout()
        add_new_phrase_qhl.addWidget(self.add_new_phrase_qpb)

        self.edit_texts_qpb = PushButton()
        self.edit_texts_qpb.setFixedWidth(75)
        self.edit_texts_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("pencil-2x.png")))
        self.edit_texts_qpb.setToolTip(self.tr("Edit the selected breathing phrase"))
        self.edit_texts_qpb.clicked.connect(self.on_edit_texts_clicked)

        self.move_to_top_qpb = PushButton()
        self.move_to_top_qpb.setFixedWidth(75)
        self.move_to_top_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("data-transfer-upload-2x.png")))
        self.move_to_top_qpb.setToolTip(self.tr("Move the selected breathing phrase to top"))
        self.move_to_top_qpb.clicked.connect(self.on_move_to_top_clicked)

        self.move_up_qpb = PushButton()
        self.move_up_qpb.setFixedWidth(75)
        self.move_up_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("arrow-top-2x.png")))
        self.move_up_qpb.setToolTip(self.tr("Move the selected breathing phrase up"))
        self.move_up_qpb.clicked.connect(self.on_move_up_clicked)

        self.move_down_qpb = PushButton()
        self.move_down_qpb.setFixedWidth(75)
        self.move_down_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("arrow-bottom-2x.png")))
        self.move_down_qpb.setToolTip(self.tr("Move the selected breathing phrase down"))
        self.move_down_qpb.clicked.connect(self.on_move_down_clicked)

        self.delete_phrase_qpb = PushButton()
        self.delete_phrase_qpb.setFixedWidth(75)
        self.delete_phrase_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("trash-2x.png")))
        self.delete_phrase_qpb.setToolTip(self.tr("Delete the selected breathing phrase"))
        self.delete_phrase_qpb.clicked.connect(self.on_delete_clicked)

        button_bar_grid = QtWidgets.QGridLayout()
        button_bar_grid.addWidget(self.edit_texts_qpb, 0, 0)
        button_bar_grid.addWidget(self.move_to_top_qpb, 0, 1)
        button_bar_grid.addWidget(self.move_up_qpb, 0, 2)
        button_bar_grid.addWidget(self.move_down_qpb, 0, 3)
        button_bar_grid.addWidget(self.delete_phrase_qpb, 0, 5)
        button_bar_grid.setColumnStretch(4, 1)

        # spacing doesn't work the same on different operating systems.
        # on macos the default value of -1 gives the best result
        # on linux it should be 2
        if QtCore.QSysInfo.kernelType() == "linux":
            button_bar_grid.setHorizontalSpacing(2)

        breathing_list_grid = QtWidgets.QGridLayout()
        if QtCore.QSysInfo.kernelType() == "linux":
            breathing_list_grid.setVerticalSpacing(15)
        breathing_list_grid.addWidget(
            QtWidgets.QLabel(self.tr("These are the sentences that appear in the `breathing dialog`")), 0, 0, 1, 3
        )
        breathing_list_grid.addWidget(
            QtWidgets.QLabel(self.tr("They also appear in the `breathing notification`")), 1, 0, 1, 3
        )

        breathing_list_grid.addWidget(self.list_widget, 2, 0, 1, 3)
        breathing_list_grid.addWidget(self.add_to_list_qle, 3, 0)
        breathing_list_grid.setColumnStretch(1, 1)
        breathing_list_grid.addLayout(add_new_phrase_qhl, 3, 2)
        breathing_list_grid.addLayout(button_bar_grid, 4, 0, 1, 3)

        self.setLayout(breathing_list_grid)
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
        self.move_current_row_up_down(mc.model.MoveDirectionEnum.up)

    def on_move_down_clicked(self):
        self.move_current_row_up_down(mc.model.MoveDirectionEnum.down)

    def on_move_to_top_clicked(self):
        current_row_int = self.list_widget.currentRow()
        current_list_widget_item = self.list_widget.item(current_row_int)
        item_widget = self.list_widget.itemWidget(current_list_widget_item)
        self.list_widget.takeItem(current_row_int)
        # -IMPORTANT: item is removed from list only after the item widget has been extracted.
        #  The reason for this is that if we take the item away from the list the associated
        #  widget (in our case a CustomLabel) will not come with us (which makes sense
        #  if the widget is stored in the list somehow)

        self.list_widget.insertItem(0, current_list_widget_item)  # -0 for the topmost position
        self.list_widget.setItemWidget(current_list_widget_item, item_widget)
        self.list_widget.setCurrentRow(0)

        self.update_db_sort_order_for_all_rows()

    def update_db_sort_order_for_all_rows(self):
        logging.debug("update_db_sort_order_for_all_rows")
        count = 0
        while count < self.list_widget.count():
            q_list_item_widget = self.list_widget.item(count)
            custom_label = self.list_widget.itemWidget(q_list_item_widget)
            id_int = custom_label.entry_id
            row_int = self.list_widget.row(q_list_item_widget)
            mc.model.PhrasesM.update_sort_order(
                id_int,
                row_int
            )
            logging.debug("id_int = " + str(id_int) + ", row_int = " + str(row_int))
            count += 1

        self.update_gui()
        self.update_selected()

    def move_current_row_up_down(self, i_move_direction: mc.model.MoveDirectionEnum) -> bool:
        current_row_int = self.list_widget.currentRow()
        current_list_widget_item = self.list_widget.item(current_row_int)
        item_widget = self.list_widget.itemWidget(current_list_widget_item)
        self.list_widget.takeItem(current_row_int)
        # -IMPORTANT: item is removed from list only after the item widget has been extracted.
        #  The reason for this is that if we take the item away from the list the associated
        #  widget (in our case a CustomLabel) will not come with us (which makes sense
        #  if the widget is stored in the list somehow)
        if i_move_direction == mc.model.MoveDirectionEnum.up:
            # if main_sort_order_int == 0 or main_sort_order_int > len(QuestionM.get_all()):
            if current_row_int >= 0:
                self.list_widget.insertItem(current_row_int - 1, current_list_widget_item)
                self.list_widget.setItemWidget(current_list_widget_item, item_widget)
                self.list_widget.setCurrentRow(current_row_int - 1)
            else:
                return False
        elif i_move_direction == mc.model.MoveDirectionEnum.down:
            # if main_sort_order_int < 0 or main_sort_order_int >= len(QuestionM.get_all()):
            if current_row_int < self.list_widget.count():
                self.list_widget.insertItem(current_row_int + 1, current_list_widget_item)
                self.list_widget.setItemWidget(current_list_widget_item, item_widget)
                self.list_widget.setCurrentRow(current_row_int + 1)
            else:
                return False

        self.update_db_sort_order_for_all_rows()
        return True

    def update_selected(self):
        for i in range(0, self.list_widget.count()):
            item = self.list_widget.item(i)
            phrase_qll = self.list_widget.itemWidget(item)
            logging.debug("custom_qll.entry_id = " + str(phrase_qll.entry_id))
            if phrase_qll.entry_id == mc.mc_global.active_phrase_id_it:
                item.setSelected(True)
                self.list_widget.setCurrentItem(item)  # -important that we add this as well
                return

    def on_edit_texts_clicked(self):
        id_int = mc.mc_global.active_phrase_id_it
        if id_int != mc.mc_global.NO_PHRASE_SELECTED_INT:
            self.edit_dialog = EditDialog()
            self.edit_dialog.finished.connect(self.on_edit_dialog_finished)
            self.edit_dialog.show()

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
            conf_result_bool = mc.gui.warning_dlg.WarningDlg.get_safe_confirmation_dialog(
                self.tr("You have to write an item before you press 'Add'.")
            )
            return
        mc.model.PhrasesM.add(
            text_sg,
            BREATHING_IN_DEFAULT_PHRASE,
            BREATHING_OUT_DEFAULT_PHRASE,
            BREATHING_IN_DEFAULT_SHORT_PHRASE,
            BREATHING_OUT_DEFAULT_SHORT_PHRASE,
            mc.mc_global.BreathingPhraseType.in_out
        )
        self.add_to_list_qle.clear()

        self.update_gui()
        self.list_widget.setCurrentRow(self.list_widget.count() - 1)
        # self.in_breath_phrase_qle.setFocus()

        # if dialog_result == QtWidgets.QDialog.Accepted:
        self.edit_dialog = EditDialog()
        self.edit_dialog.finished.connect(self.on_edit_dialog_finished)
        self.edit_dialog.show()

    def on_edit_dialog_finished(self, i_result: int):

        if i_result == QtWidgets.QDialog.Accepted:
            assert mc.mc_global.active_phrase_id_it != mc.mc_global.NO_PHRASE_SELECTED_INT
            phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)
            phrase.title = self.edit_dialog.breath_title_qle.text()
            phrase.ib = self.edit_dialog.in_breath_phrase_qle.text()
            phrase.ob = self.edit_dialog.out_breath_phrase_qle.text()
        else:
            pass

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
            list_item.setSizeHint(QtCore.QSize(list_item.sizeHint().width(), mc_global.LIST_ITEM_HEIGHT_INT))
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, custom_label)

        self.updating_gui_bool = False


class CustomQLabel(QtWidgets.QLabel):
    entry_id = mc.mc_global.NO_PHRASE_SELECTED_INT  # -"static"

    def __init__(self, i_text_sg, i_entry_id=mc.mc_global.NO_PHRASE_SELECTED_INT):
        super().__init__(i_text_sg)
        self.entry_id = i_entry_id


class EditDialog(QtWidgets.QDialog):
    def __init__(self, i_parent=None):
        super(EditDialog, self).__init__(i_parent)

        self.setModal(True)

        self.setMinimumWidth(250)

        self.updating_gui_bool = False

        # If a phrase is not selected, default to phrase with id 1
        if mc.mc_global.active_phrase_id_it == mc.mc_global.NO_PHRASE_SELECTED_INT:
            mc.mc_global.active_phrase_id_it = 1

        active_phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)

        vbox = QtWidgets.QVBoxLayout(self)

        self.breath_title_qle = QtWidgets.QLineEdit(active_phrase.title)
        vbox.addWidget(QtWidgets.QLabel(self.tr("Title")))
        vbox.addWidget(self.breath_title_qle)

        vbox.addWidget(QtWidgets.QLabel("Phrase(s)"))
        self.in_breath_phrase_qle = QtWidgets.QLineEdit(active_phrase.ib)
        vbox.addWidget(self.in_breath_phrase_qle)

        self.out_breath_phrase_qle = QtWidgets.QLineEdit(active_phrase.ob)
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

        self.update_gui()

    def update_gui(self):
        self.updating_gui_bool = True

        self.adjustSize()

        self.updating_gui_bool = False
