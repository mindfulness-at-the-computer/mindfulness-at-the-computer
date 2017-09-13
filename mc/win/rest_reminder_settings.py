import os
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from mc import model, mc_global
import mc.dlg.safe_delete_dialog
import mc.win.toggle_switch

# Here we place settings for the application, for example the time between notifications,
# as well as if there is audio as well as the notification
# Perhaps we want to hide some of these settings?
# All intervals are in minutes

MIN_REST_REMINDER_INT = 1  # -in minutes
MAX_REST_REMINDER_INT = 99


class RestSettingsComposite(QtWidgets.QWidget):
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

        self.rest_reminder_switch = mc.win.toggle_switch.ToggleSwitchComposite()
        vbox.addWidget(self.rest_reminder_switch)
        self.rest_reminder_switch.toggled_signal.connect(self.on_switch_toggled)

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addWidget(QtWidgets.QLabel("Interval:"))
        self.rest_reminder_interval_qsb = QtWidgets.QSpinBox()
        hbox.addWidget(self.rest_reminder_interval_qsb)
        hbox.addWidget(QtWidgets.QLabel("minutes"))
        hbox.addStretch(1)
        self.rest_reminder_interval_qsb.setMinimum(MIN_REST_REMINDER_INT)
        self.rest_reminder_interval_qsb.setMaximum(MAX_REST_REMINDER_INT)
        self.rest_reminder_interval_qsb.valueChanged.connect(self.on_rest_interval_value_changed)
        vbox.addWidget(QtWidgets.QLabel("Remaining time until next break"))
        self.rest_reminder_qprb = QtWidgets.QProgressBar()
        vbox.addWidget(self.rest_reminder_qprb)
        self.rest_reminder_qprb.setTextVisible(False)
        """
        base_qcolor = QtGui.QColor(41, 163, 41, 0)
        base_qpalette = QtGui.QPalette()
        base_qpalette.setColor(QtGui.QPalette.Base, base_qcolor)
        self.rest_reminder_qprb.setPalette(base_qpalette)
        """
        self.rest_reminder_qprb.setStyleSheet("background-color: #f4fde7;")

        # hbox = QtWidgets.QHBoxLayout()
        # vbox.addLayout(hbox)
        self.rest_reminder_reset_qpb = QtWidgets.QPushButton("Reset timer")
        vbox.addWidget(self.rest_reminder_reset_qpb)
        self.rest_reminder_reset_qpb.clicked.connect(self.on_rest_reset_clicked)


        # Rest actions
        vbox.addWidget(CustomFrame())
        vbox.addWidget(QtWidgets.QLabel("Rest actions"))
        self.rest_actions_qlw = QtWidgets.QListWidget()
        vbox.addWidget(self.rest_actions_qlw)
        self.rest_actions_qlw.currentRowChanged.connect(self.on_current_row_changed)
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
        details_vbox = QtWidgets.QVBoxLayout()
        self.details_qgb.setLayout(details_vbox)

        details_vbox.addWidget(QtWidgets.QLabel("Title"))
        self.details_name_qle = QtWidgets.QLineEdit()
        details_vbox.addWidget(self.details_name_qle)

        self.details_image_path_qll = QtWidgets.QLabel()
        details_vbox.addWidget(self.details_image_path_qll)
        self.details_image_path_qll.setWordWrap(True)
        self.select_image_qpb = QtWidgets.QPushButton("Select image")
        details_vbox.addWidget(self.select_image_qpb)
        self.select_image_qpb.clicked.connect(self.on_select_image_clicked)
        self.delete_qpb = QtWidgets.QPushButton("Delete action")
        details_vbox.addWidget(self.delete_qpb)
        self.delete_qpb.clicked.connect(self.on_delete_clicked)

        # Take break button
        vbox.addWidget(CustomFrame())
        self.rest_reminder_test_qpb = QtWidgets.QPushButton("Take a break now")  # -from the computer
        vbox.addWidget(self.rest_reminder_test_qpb)
        self.rest_reminder_test_qpb.clicked.connect(self.on_rest_test_clicked)

        vbox.addStretch(1)

        # vbox.addWidget(QtWidgets.QLabel("<i>All changes are automatically saved</i>"))

        self.update_gui()

    def on_delete_clicked(self):
        # active_phrase = model.PhrasesM.get(mc_global.active_phrase_id_it)
        conf_result_bool = mc.dlg.safe_delete_dialog.SafeDeleteDialog.get_safe_confirmation_dialog(
            "Are you sure that you want to remove this entry?"
        )
        if conf_result_bool:
            self.rest_actions_qlw.clearSelection()
            model.RestActionsM.remove(mc_global.active_rest_action_id_it)
            mc_global.active_rest_action_id_it = mc_global.NO_REST_ACTION_SELECTED_INT
            self.update_gui()
        else:
            pass

    def on_current_row_changed(self):
        current_row_int = self.rest_actions_qlw.currentRow()
        if current_row_int != -1:
            current_rest_action_qli = self.rest_actions_qlw.item(current_row_int)
            customqlabel_widget = self.rest_actions_qlw.itemWidget(current_rest_action_qli)
            mc_global.active_rest_action_id_it = customqlabel_widget.question_entry_id
        else:
            raise Exception("We should not be able to deselect")

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
        print(image_file_path_str)
        if image_file_path_str:
            model.RestActionsM.update_rest_action_image_path(
                mc_global.active_rest_action_id_it,
                image_file_path_str
            )
            self.update_gui_details()
        else:
            pass

    def add_rest_action_clicked(self):
        model.RestActionsM.add(
            self.rest_add_action_qle.text().strip(),
            ""
        )
        self.update_gui()
        self.rest_actions_qlw.setCurrentRow(self.rest_actions_qlw.count() - 1)

    def on_rest_reset_clicked(self):
        self.rest_reset_button_clicked_signal.emit()

    def on_rest_test_clicked(self):
        self.rest_test_button_clicked_signal.emit()

    def on_switch_toggled(self, i_checked_bool):
        if self.updating_gui_bool:
            return
        model.SettingsM.update_rest_reminder_active(i_checked_bool)
        self.rest_settings_updated_signal.emit()

    def on_rest_interval_value_changed(self, i_new_value: int):
        # -PLEASE NOTE: During debug this event is fired twice, this must be a bug in Qt or PyQt
        # (there is no problem when running normally, that is without debug)
        if self.updating_gui_bool:
            return
        model.SettingsM.update_rest_reminder_interval(i_new_value)
        self.rest_settings_updated_signal.emit()

        rest_reminder_interval_minutes_int = model.SettingsM.get().rest_reminder_interval_int
        self.rest_reminder_qprb.setMinimum(0)
        self.rest_reminder_qprb.setMaximum(rest_reminder_interval_minutes_int)
        self.rest_reminder_qprb.setValue(mc_global.rest_reminder_minutes_passed_int)


    def update_gui(self):
        self.updating_gui_bool = True

        # Rest reminder
        rr_enabled = model.SettingsM.get().rest_reminder_active_bool
        self.rest_reminder_switch.update_gui(rr_enabled)
        rest_reminder_interval_minutes_int = model.SettingsM.get().rest_reminder_interval_int
        self.rest_reminder_interval_qsb.setValue(rest_reminder_interval_minutes_int)
        self.rest_reminder_qprb.setMinimum(0)
        self.rest_reminder_qprb.setMaximum(rest_reminder_interval_minutes_int)
        self.rest_reminder_qprb.setValue(mc_global.rest_reminder_minutes_passed_int)

        self.rest_actions_qlw.clear()
        for rest_action in model.RestActionsM.get_all():
            rest_action_title_cll = CustomQLabel(rest_action.title_str, rest_action.id_int)
            list_item = QtWidgets.QListWidgetItem()
            self.rest_actions_qlw.addItem(list_item)
            self.rest_actions_qlw.setItemWidget(list_item, rest_action_title_cll)

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


class CustomQLabel(QtWidgets.QLabel):
    question_entry_id = mc_global.NO_PHRASE_SELECTED_INT  # -"static"
    #mouse_pressed_signal = QtCore.pyqtSignal(QtGui.QMouseEvent, int)

    def __init__(self, i_text_sg, i_diary_entry_id=mc_global.NO_PHRASE_SELECTED_INT):
        super().__init__(i_text_sg)
        self.question_entry_id = i_diary_entry_id


class CustomFrame(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
