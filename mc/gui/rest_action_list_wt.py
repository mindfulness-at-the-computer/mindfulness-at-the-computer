
import logging
import os
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import mc.gui.safe_delete_dlg
import mc.gui.warning_dlg
import mc.mc_global
from mc import model, mc_global
from mc.gui.reusable_components import PhrasesList, PushButton


class RestActionListWt(QtWidgets.QWidget):
    update_signal = QtCore.pyqtSignal()
    selection_changed_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.updating_gui_bool = False

        # Rest actions
        self.list_widget = PhrasesList()
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)

        self.rest_add_action_qle = QtWidgets.QLineEdit()
        self.rest_add_action_qle.setObjectName("add_to_list_qle")
        self.rest_add_action_qle.setPlaceholderText(self.tr("New item"))
        self.rest_add_action_qle.setFixedWidth(305)
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.Key_Return),
            self.rest_add_action_qle,
            member=self.add_rest_action_clicked,
            context=QtCore.Qt.WidgetShortcut
        )

        self.add_new_phrase_qpb = PushButton(self.tr("Add"))
        self.add_new_phrase_qpb.setFixedWidth(75)
        self.add_new_phrase_qpb.clicked.connect(self.add_rest_action_clicked)
        add_new_phrase_qhl = QtWidgets.QHBoxLayout()
        add_new_phrase_qhl.addWidget(self.add_new_phrase_qpb)

        # Details
        self.edit_texts_qpb = PushButton()
        self.edit_texts_qpb.setFixedWidth(75)
        self.edit_texts_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("pencil-2x.png")))
        self.edit_texts_qpb.setToolTip(self.tr("Edit the selected rest action"))
        self.edit_texts_qpb.clicked.connect(self.on_edit_texts_clicked)

        self.move_to_top_qpb = PushButton()
        self.move_to_top_qpb.setFixedWidth(75)
        self.move_to_top_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("data-transfer-upload-2x.png")))
        self.move_to_top_qpb.setToolTip(self.tr("Move the selected rest action to top"))
        self.move_to_top_qpb.clicked.connect(self.on_move_to_top_clicked)

        self.move_up_qpb = PushButton()
        self.move_up_qpb.setFixedWidth(75)
        self.move_up_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("arrow-top-2x.png")))
        self.move_up_qpb.setToolTip(self.tr("Move the selected rest action up"))
        self.move_up_qpb.clicked.connect(self.on_move_up_clicked)

        self.move_down_qpb = PushButton()
        self.move_down_qpb.setFixedWidth(75)
        self.move_down_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("arrow-bottom-2x.png")))
        self.move_down_qpb.setToolTip(self.tr("Move the selected rest action down"))
        self.move_down_qpb.clicked.connect(self.on_move_down_clicked)

        self.delete_qpb = PushButton()
        self.delete_qpb.setFixedWidth(75)
        self.delete_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("trash-2x.png")))
        self.delete_qpb.setToolTip(self.tr("Delete the selected rest action"))
        self.delete_qpb.clicked.connect(self.on_delete_clicked)

        button_bar_grid = QtWidgets.QGridLayout()
        button_bar_grid.addWidget(self.edit_texts_qpb, 0, 0)
        button_bar_grid.addWidget(self.move_to_top_qpb, 0, 1)
        button_bar_grid.addWidget(self.move_up_qpb, 0, 2)
        button_bar_grid.addWidget(self.move_down_qpb, 0, 3)
        button_bar_grid.addWidget(self.delete_qpb, 0, 5)
        button_bar_grid.setColumnStretch(4, 1)

        # spacing doesn't work the same on different operating systems.
        # on macos the default value of -1 gives the best result
        # on linux it should be 2
        if QtCore.QSysInfo.kernelType() == "linux":
            button_bar_grid.setHorizontalSpacing(2)

        rest_action_list_grid = QtWidgets.QGridLayout()
        rest_action_list_grid.addWidget(
            QtWidgets.QLabel(self.tr("These are the actions that appear in the `rest dialog`")), 0, 0, 1, 3
        )

        rest_action_list_grid.addWidget(self.list_widget, 1, 0, 1, 3)
        rest_action_list_grid.addWidget(self.rest_add_action_qle, 2, 0)
        rest_action_list_grid.setColumnStretch(1, 1)
        rest_action_list_grid.addLayout(add_new_phrase_qhl, 2, 2)
        rest_action_list_grid.addLayout(button_bar_grid, 3, 0, 1, 3)

        self.setLayout(rest_action_list_grid)
        self.update_gui()

    def on_edit_texts_clicked(self):
        id_int = mc.mc_global.active_rest_action_id_it
        if id_int != mc.mc_global.NO_REST_ACTION_SELECTED_INT:
            EditDialog.launch_edit_dialog()
            self.update_signal.emit()

    def on_move_up_clicked(self):
        self.move_up_down(model.MoveDirectionEnum.up)

    def on_move_down_clicked(self):
        self.move_up_down(model.MoveDirectionEnum.down)

    def move_up_down(self, i_up_down: model.MoveDirectionEnum):
        id_int = mc.mc_global.active_rest_action_id_it
        if id_int != mc.mc_global.NO_REST_ACTION_SELECTED_INT:
            model.RestActionsM.update_sort_order_move_up_down(id_int, i_up_down)
            self.update_gui()
            self.update_selected()

    def on_move_to_top_clicked(self):
        while True:
            result_bool = model.RestActionsM.update_sort_order_move_up_down(
                mc.mc_global.active_rest_action_id_it,
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
            conf_result_bool = mc.gui.warning_dlg.WarningDlg.get_safe_confirmation_dialog(
                self.tr("You have to write an item before you press 'Add'.")
            )
            return
        model.RestActionsM.add(
            self.rest_add_action_qle.text().strip()
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
            list_item.setSizeHint(QtCore.QSize(list_item.sizeHint().width(), mc.mc_global.LIST_ITEM_HEIGHT_INT))
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
