
import logging
import os
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import mc.gui.safe_delete_dlg
from mc import model, mc_global


class RestActionsComposite(QtWidgets.QWidget):

    delete_signal = QtCore.pyqtSignal()
    selection_changed_signal = QtCore.pyqtSignal(int)

    """
    update_signal = QtCore.pyqtSignal()
    list_selection_changed_signal = QtCore.pyqtSignal()
    """

    def __init__(self):
        super().__init__()

        self.updating_gui_bool = False

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        # Rest actions
        self.list_widget = QtWidgets.QListWidget()
        vbox.addWidget(self.list_widget)

        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        self.rest_add_action_qle = QtWidgets.QLineEdit()
        hbox.addWidget(self.rest_add_action_qle)
        self.rest_add_action_qpb = QtWidgets.QPushButton("Add")
        hbox.addWidget(self.rest_add_action_qpb)
        self.rest_add_action_qpb.clicked.connect(self.add_rest_action_clicked)

        # Details

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)

        self.edit_texts_qpb = QtWidgets.QPushButton()
        hbox.addWidget(self.edit_texts_qpb)
        self.edit_texts_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("pencil-2x.png")))
        self.edit_texts_qpb.clicked.connect(self.on_edit_texts_clicked)

        self.move_to_top_qpb = QtWidgets.QPushButton()
        hbox.addWidget(self.move_to_top_qpb)
        self.move_to_top_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("data-transfer-upload-2x.png")))
        self.move_to_top_qpb.clicked.connect(self.on_move_to_top_clicked)
        self.move_up_qpb = QtWidgets.QPushButton()
        hbox.addWidget(self.move_up_qpb)
        self.move_up_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("arrow-top-2x.png")))
        self.move_up_qpb.clicked.connect(self.on_move_up_clicked)
        self.move_down_qpb = QtWidgets.QPushButton()
        hbox.addWidget(self.move_down_qpb)
        self.move_down_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("arrow-bottom-2x.png")))
        self.move_down_qpb.clicked.connect(self.on_move_down_clicked)
        hbox.addStretch(1)
        self.delete_qpb = QtWidgets.QPushButton()
        hbox.addWidget(self.delete_qpb)
        self.delete_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("trash-2x.png")))
        self.delete_qpb.clicked.connect(self.on_delete_clicked)

        self.update_gui()

    def on_edit_texts_clicked(self):
        EditDialog.launch_edit_dialog()
        self.update_signal.emit()

    def on_move_up_clicked(self):
        self.move_up_down(model.MoveDirectionEnum.up)

    def on_move_down_clicked(self):
        self.move_up_down(model.MoveDirectionEnum.down)

    def move_up_down(self, i_up_down: model.MoveDirectionEnum):
        id_int = mc_global.active_rest_action_id_it
        model.RestActionsM.update_sort_order_move_up_down(id_int, i_up_down)
        self.update_gui()

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

    def add_rest_action_clicked(self):
        if not(self.rest_add_action_qle.text().strip()):
            return
        model.RestActionsM.add(
            self.rest_add_action_qle.text().strip(),
            ""
        )
        self.update_gui()
        self.list_widget.setCurrentRow(self.list_widget.count() - 1)

    def on_delete_clicked(self):
        conf_result_bool = SafeDeleteDialog.get_safe_confirmation_dialog(
            "Are you sure that you want to remove this entry?"
        )
        if conf_result_bool:
            self.list_widget.clearSelection()
            self.delete_signal.emit()

            """ For the handler method:
            model.RestActionsM.remove(mc_global.active_rest_action_id_it)
            mc_global.active_rest_action_id_it = mc_global.NO_REST_ACTION_SELECTED_INT
            self.update_gui()
            """

    def on_selection_changed(self):
        if self.updating_gui_bool:
            return
        selected_model_index_list = self.list_widget.selectedIndexes()
        if len(selected_model_index_list) >= 1:
            selected_row_model_index_int = selected_model_index_list[0].row()
            selected_rest_action_qli = self.list_widget.item(selected_row_model_index_int)
            row_label_cll = self.list_widget.itemWidget(selected_rest_action_qli)

            self.selection_changed_signal(row_label_cll.question_entry_id)

            """ For the handler method:
            mc_global.active_rest_action_id_it = row_label_cll.question_entry_id
            """
        else:
            # mc_global.act= mc_global.NO_PHRASE_SELECTED_INT
            self.selection_changed_signal(mc_global.NOTHING_SELECTED_INT)

        """ For the handler method:
        self.list_selection_changed_signal.emit()
        """

    def update_gui(self):
        self.updating_gui_bool = True

        self.list_widget.clear()
        for rest_action in model.RestActionsM.get_all():
            rest_action_title_cll = CustomQLabel(rest_action.title, rest_action.id)
            list_item = QtWidgets.QListWidgetItem()
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, rest_action_title_cll)

        for i in range(0, self.list_widget.count()):
            item = self.list_widget.item(i)
            rest_qll = self.list_widget.itemWidget(item)
            logging.debug("custom_qll.question_entry_id = " + str(rest_qll.question_entry_id))
            if rest_qll.question_entry_id == mc_global.active_rest_action_id_it:
                item.setSelected(True)
                return

        self.updating_gui_bool = False


class CustomQLabel(QtWidgets.QLabel):
    entry_id = mc.mc_global.NO_PHRASE_SELECTED_INT  # -"static"

    def __init__(self, i_text_sg, i_entry_id):
        super().__init__(i_text_sg)
        self.entry_id = i_entry_id




class SafeDeleteDialog(QtWidgets.QDialog):
    """
    Inspiration: Answer by lou here:
    https://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
    """
    def __init__(self, i_description_str, i_parent = None):
        super(SafeDeleteDialog, self).__init__(i_parent)

        vbox = QtWidgets.QVBoxLayout(self)

        self.description_qll = QtWidgets.QLabel(i_description_str)
        vbox.addWidget(self.description_qll)

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
    def get_safe_confirmation_dialog(i_description_str):
        dialog = SafeDeleteDialog(i_description_str)
        dialog_result = dialog.exec_()
        confirmation_result_bool = False
        if dialog_result == QtWidgets.QDialog.Accepted:
            confirmation_result_bool = True
        return confirmation_result_bool


