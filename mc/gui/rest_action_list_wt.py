
import logging
import os
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import mc.gui.safe_delete_dlg
from mc import model, mc_global


class RestActionListWt(QtWidgets.QWidget):
    update_signal = QtCore.pyqtSignal()
    selection_changed_signal = QtCore.pyqtSignal()

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
        self.rest_add_action_qpb = QtWidgets.QPushButton(self.tr("Add"))
        hbox.addWidget(self.rest_add_action_qpb)
        self.rest_add_action_qpb.clicked.connect(self.add_rest_action_clicked)

        # Details

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)

        self.edit_texts_qpb = QtWidgets.QPushButton()
        self.edit_texts_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("pencil-2x.png")))
        self.edit_texts_qpb.setToolTip(self.tr("Edit the selected rest action"))
        self.edit_texts_qpb.clicked.connect(self.on_edit_texts_clicked)
        hbox.addWidget(self.edit_texts_qpb)

        self.move_to_top_qpb = QtWidgets.QPushButton()
        self.move_to_top_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("data-transfer-upload-2x.png")))
        self.move_to_top_qpb.setToolTip(self.tr("Move the selected rest action to top"))
        self.move_to_top_qpb.clicked.connect(self.on_move_to_top_clicked)
        hbox.addWidget(self.move_to_top_qpb)

        self.move_up_qpb = QtWidgets.QPushButton()
        self.move_up_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("arrow-top-2x.png")))
        self.move_up_qpb.setToolTip(self.tr("Move the selected rest action up"))
        self.move_up_qpb.clicked.connect(self.on_move_up_clicked)
        hbox.addWidget(self.move_up_qpb)

        self.move_down_qpb = QtWidgets.QPushButton()
        self.move_down_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("arrow-bottom-2x.png")))
        self.move_down_qpb.setToolTip(self.tr("Move the selected rest action down"))
        self.move_down_qpb.clicked.connect(self.on_move_down_clicked)
        hbox.addWidget(self.move_down_qpb)

        hbox.addStretch(1)

        self.delete_qpb = QtWidgets.QPushButton()
        self.delete_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("trash-2x.png")))
        self.delete_qpb.setToolTip(self.tr("Delete the selected rest action"))
        self.delete_qpb.clicked.connect(self.on_delete_clicked)
        hbox.addWidget(self.delete_qpb)

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

    def update_selected(self):
        for i in range(0, self.list_widget.count()):
            item = self.list_widget.item(i)
            rest_qll = self.list_widget.itemWidget(item)
            logging.debug("custom_qll.question_entry_id = " + str(rest_qll.question_entry_id))
            if rest_qll.question_entry_id == mc_global.active_rest_action_id_it:
                item.setSelected(True)
                return

    def add_rest_action_clicked(self):
        if not(self.rest_add_action_qle.text().strip()):
            return
        model.RestActionsM.add(
            self.rest_add_action_qle.text().strip(),
            ""
        )
        self.update_gui()
        self.list_widget.setCurrentRow(self.list_widget.count() - 1)
        self.rest_add_action_qle.clear()

    def on_delete_clicked(self):
        # active_phrase = model.PhrasesM.get(mc_global.active_phrase_id_it)
        conf_result_bool = mc.gui.safe_delete_dlg.SafeDeleteDlg.get_safe_confirmation_dialog(
            self.tr("Are you sure that you want to remove this entry?")
        )
        if conf_result_bool:
            self.list_widget.clearSelection()
            model.RestActionsM.remove(mc_global.active_rest_action_id_it)
            mc_global.active_rest_action_id_it = mc_global.NO_REST_ACTION_SELECTED_INT
            self.update_gui()
        else:
            pass

    def on_selection_changed(self):
        if self.updating_gui_bool:
            return
        selected_model_index_list = self.list_widget.selectedIndexes()
        if len(selected_model_index_list) >= 1:
            selected_row_int = selected_model_index_list[0].row()
            selected_rest_action_qli = self.list_widget.item(selected_row_int)
            row_label_cll = self.list_widget.itemWidget(selected_rest_action_qli)
            mc_global.active_rest_action_id_it = row_label_cll.question_entry_id
        else:
            pass
            # mc_global.act= mc_global.NO_PHRASE_SELECTED_INT

        self.selection_changed_signal.emit()

    def update_gui(self):
        self.updating_gui_bool = True

        self.list_widget.clear()
        for rest_action in model.RestActionsM.get_all():
            rest_action_title_cll = RestQLabel(rest_action.title, rest_action.id)
            list_item = QtWidgets.QListWidgetItem()
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, rest_action_title_cll)

        # self.update_gui_details()

        self.updating_gui_bool = False


class RestQLabel(QtWidgets.QLabel):
    question_entry_id = mc_global.NO_PHRASE_SELECTED_INT  # -"static"

    def __init__(self, i_text: str, i_diary_entry_id: int=mc_global.NO_PHRASE_SELECTED_INT):
        super().__init__(i_text)
        self.question_entry_id = i_diary_entry_id


class EditDialog(QtWidgets.QDialog):
    """
    Inspiration: Answer by lou here:
    https://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
    """
    def __init__(self, i_parent=None):
        super(EditDialog, self).__init__(i_parent)

        rest_action = model.RestActionsM.get(mc_global.active_rest_action_id_it)
        self.temporary_image_file_path_str = rest_action.image_path

        assert mc_global.active_rest_action_id_it != mc_global.NO_REST_ACTION_SELECTED_INT
        active_rest_action = model.RestActionsM.get(mc_global.active_rest_action_id_it)

        vbox = QtWidgets.QVBoxLayout(self)

        # Title
        title_qgb = QtWidgets.QGroupBox(self.tr("Title"))
        vbox.addWidget(title_qgb)
        title_vbox = QtWidgets.QVBoxLayout()
        title_qgb.setLayout(title_vbox)
        self.rest_action_title_qle = QtWidgets.QLineEdit(active_rest_action.title)
        title_vbox.addWidget(self.rest_action_title_qle)

        # Image
        image_qgb = QtWidgets.QGroupBox(self.tr("Image"))
        vbox.addWidget(image_qgb)
        image_vbox = QtWidgets.QVBoxLayout()
        image_qgb.setLayout(image_vbox)
        self.select_image_qpb = QtWidgets.QPushButton(self.tr(" Select image"))
        image_vbox.addWidget(self.select_image_qpb)
        self.select_image_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("image-2x.png")))
        self.select_image_qpb.clicked.connect(self.on_select_image_clicked)
        self.details_image_path_qll = QtWidgets.QLabel()
        image_vbox.addWidget(self.details_image_path_qll)
        self.details_image_path_qll.setWordWrap(True)

        self.remove_image_qpb = QtWidgets.QPushButton()
        image_vbox.addWidget(self.remove_image_qpb)
        self.remove_image_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("x-2x.png")))
        self.remove_image_qpb.clicked.connect(self.on_remove_image_clicked)

        self.update_gui_details()

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )
        vbox.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        # -accept and reject are "slots" built into Qt

    def update_gui_details(self):
        assert mc_global.active_rest_action_id_it != mc_global.NO_REST_ACTION_SELECTED_INT

        if self.temporary_image_file_path_str:
            if os.path.isfile(self.temporary_image_file_path_str):
                self.details_image_path_qll.setText(os.path.basename(
                    self.temporary_image_file_path_str)
                )
            else:
                self.details_image_path_qll.setText(self.tr("image does not exist"))
        else:
            self.details_image_path_qll.setText(self.tr("(no image set)"))

    @staticmethod
    def launch_edit_dialog():
        dialog = EditDialog()
        dialog_result = dialog.exec_()

        if dialog_result == QtWidgets.QDialog.Accepted:
            rest_action = model.RestActionsM.get(mc_global.active_rest_action_id_it)
            rest_action.title = dialog.rest_action_title_qle.text()
            rest_action.image_path = dialog.temporary_image_file_path_str
            """
            model.RestActionsM.update_title(
                mc_global.active_rest_action_id_it,
                dialog.rest_action_title_qle.text()
            )
            model.RestActionsM.update_rest_action_image_path(
                mc_global.active_rest_action_id_it,
                dialog.temporary_image_file_path_str
            )
            """
        else:
            pass

        return dialog_result

    def on_select_image_clicked(self):
        # noinspection PyCallByClass
        image_file_result_tuple = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Please choose an image"),
            mc_global.get_user_images_path(),
            "Image files (*.png *.jpg *.bmp)"
        )
        new_file_path_str = image_file_result_tuple[0]
        logging.debug("new_file_path_str = " + new_file_path_str)
        if new_file_path_str:
            self.temporary_image_file_path_str = new_file_path_str
            self.update_gui_details()
        else:
            pass

    def on_remove_image_clicked(self):
        self.temporary_image_file_path_str = ""
        self.update_gui_details()
