
import os
import logging

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from mc import model, mc_global
import mc.dlg.safe_delete_dialog
import mc.win.toggle_switch


class RestActionsComposite(QtWidgets.QWidget):
    rest_settings_updated_signal = QtCore.pyqtSignal()
    breathing_settings_updated_signal = QtCore.pyqtSignal()
    breathing_test_button_clicked_signal = QtCore.pyqtSignal()
    rest_test_button_clicked_signal = QtCore.pyqtSignal()
    rest_reset_button_clicked_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.updating_gui_bool = False

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        # Rest actions
        vbox.addWidget(QtWidgets.QLabel("Rest actions"))
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
        self.details_qgb = QtWidgets.QGroupBox("Details")
        vbox.addWidget(self.details_qgb)
        self.details_qgb.setDisabled(True)
        details_vbox = QtWidgets.QVBoxLayout()
        self.details_qgb.setLayout(details_vbox)

        details_vbox.addWidget(QtWidgets.QLabel("Title"))
        self.details_name_qle = QtWidgets.QLineEdit()
        details_vbox.addWidget(self.details_name_qle)

        self.details_image_path_qll = QtWidgets.QLabel()
        details_vbox.addWidget(self.details_image_path_qll)
        self.details_image_path_qll.setWordWrap(True)
        self.select_image_qpb = QtWidgets.QPushButton(" Select image")
        # self.select_image_qpb.setIcon(QtGui.QIcon(mc_global.get_icon_path("image-2x.png")))
        details_vbox.addWidget(self.select_image_qpb)
        self.select_image_qpb.clicked.connect(self.on_select_image_clicked)
        hbox = QtWidgets.QHBoxLayout()
        details_vbox.addLayout(hbox)
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
        model.RestActionsM.add(
            self.rest_add_action_qle.text().strip(),
            ""
        )
        self.update_gui()
        self.list_widget.setCurrentRow(self.list_widget.count() - 1)

    def on_delete_clicked(self):
        # active_phrase = model.PhrasesM.get(mc_global.active_phrase_id_it)
        conf_result_bool = mc.dlg.safe_delete_dialog.SafeDeleteDialog.get_safe_confirmation_dialog(
            "Are you sure that you want to remove this entry?"
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
        selected_modelindexlist = self.list_widget.selectedIndexes()
        # current_row_int = self.rest_actions_qlw.currentRow()
        if len(selected_modelindexlist) >= 1:
            selected_row_int = selected_modelindexlist[0].row()
            self.details_qgb.setDisabled(False)
            current_rest_action_qli = self.list_widget.item(selected_row_int)
            customqlabel_widget = self.list_widget.itemWidget(current_rest_action_qli)
            mc_global.active_rest_action_id_it = customqlabel_widget.question_entry_id
        else:
            self.details_qgb.setDisabled(True)
            #### mc_global.act= mc_global.NO_PHRASE_SELECTED_INT

        self.update_gui_details()
        #### self.row_changed_signal.emit()

    def on_select_image_clicked(self):
        image_file_result_tuple = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Please choose an image",
            mc_global.get_user_images_path(),
            "Image files (*.png *.jpg *.bmp)"
        )
        image_file_path_str = image_file_result_tuple[0]
        logging.debug("image_file_path_str = " + image_file_path_str)
        if image_file_path_str:
            model.RestActionsM.update_rest_action_image_path(
                mc_global.active_rest_action_id_it,
                image_file_path_str
            )
            self.update_gui_details()
        else:
            pass

    def update_gui(self):
        self.updating_gui_bool = True

        self.list_widget.clear()
        for rest_action in model.RestActionsM.get_all():
            rest_action_title_cll = RestQLabel(rest_action.title_str, rest_action.id_int)
            list_item = QtWidgets.QListWidgetItem()
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, rest_action_title_cll)

        self.update_gui_details()

        self.updating_gui_bool = False

    def update_gui_details(self):
        if mc_global.active_rest_action_id_it != mc_global.NO_REST_ACTION_SELECTED_INT:
            rest_action = model.RestActionsM.get(mc_global.active_rest_action_id_it)
            self.details_name_qle.setText(rest_action.title_str)
            if rest_action.image_path_str:
                self.details_image_path_qll.setText(os.path.basename(rest_action.image_path_str))
            else:
                self.details_image_path_qll.setText("(no image set)")


class RestQLabel(QtWidgets.QLabel):
    question_entry_id = mc_global.NO_PHRASE_SELECTED_INT  # -"static"
    #mouse_pressed_signal = QtCore.pyqtSignal(QtGui.QMouseEvent, int)

    def __init__(self, i_text: str, i_diary_entry_id: int=mc_global.NO_PHRASE_SELECTED_INT):
        super().__init__(i_text)
        self.question_entry_id = i_diary_entry_id

