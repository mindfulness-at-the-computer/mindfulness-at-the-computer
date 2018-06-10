import os
from mc import model
import mc.gui.toggle_switch_wt
from mc.gui.reusable_components import *
from mc.gui.breathing_phrase_list_wt import BreathingPhraseListWt
from mc.gui.toggle_switch_wt import ToggleSwitchWt

MIN_REST_REMINDER_INT = 1  # -in minutes
NO_AUDIO_SELECTED_STR = "No audio selected"


class BreathingSettings2Wt(QtWidgets.QWidget):
    rest_settings_updated_signal = QtCore.pyqtSignal()
    updated_signal = QtCore.pyqtSignal()
    breathe_now_button_clicked_signal = QtCore.pyqtSignal()
    rest_test_button_clicked_signal = QtCore.pyqtSignal()
    rest_reset_button_clicked_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.updating_gui_bool = False

        self.toggle_switch = ToggleSwitchWt()
        self.both_qrb = RadioButtonLeft(self.tr("Visual + Audio"))
        self.visual_qrb = RadioButtonMiddle(self.tr("Visual"))
        self.audio_qrb = RadioButtonRight(self.tr("Audio"))
        self.notification_interval_qsb = QtWidgets.QSpinBox()
        self.close_on_hover_qcb = QtWidgets.QCheckBox()
        self.same_qrb = RadioButtonLeft(self.tr("Same"))
        self.random_qrb = RadioButtonRight(self.tr("Random"))
        self.show_after_qsb = QtWidgets.QSpinBox()
        self.notif_select_audio_qpb = QtWidgets.QPushButton(self.tr("Select audio"))
        self.notif_volume_qsr = QtWidgets.QSlider()
        self.prep_select_audio_qpb = QtWidgets.QPushButton(self.tr("Select audio"))
        self.prep_volume_qsr = QtWidgets.QSlider()
        self.phrases_qlw = BreathingPhraseListWt()

        self._init_ui()
        self._connect_slots_to_signals()

    def _init_ui(self):
        settings = mc.model.SettingsM.get()

        # initializing the values of the controls
        if settings.breathing_reminder_notification_type == mc_global.NotificationType.Audio:
            self.audio_qrb.setChecked(True)
        if settings.breathing_reminder_notification_type == mc_global.NotificationType.Visual:
            self.visual_qrb.setChecked(True)
        if settings.breathing_reminder_notification_type == mc_global.NotificationType.Both:
            self.both_qrb.setChecked(True)
        if settings.breathing_dialog_phrase_selection == mc_global.PhraseSelection.same:
            self.same_qrb.setChecked(True)
        if settings.breathing_dialog_phrase_selection == mc_global.PhraseSelection.random:
            self.random_qrb.setChecked(True)
        self.toggle_switch.turn_on_off_qcb.setChecked(settings.breathing_reminder_active_bool)
        self.notif_select_audio_qpb.setObjectName("notif_select_audio_qpb")
        self.prep_select_audio_qpb.setObjectName("prep_select_audio_qpb")

        # Notification settings
        notification_type_grid = PageGrid()
        notification_type_grid.setColumnMinimumWidth(0, 120)
        notification_type_grid.setColumnMinimumWidth(1, 120)
        notification_type_grid.setColumnMinimumWidth(2, 125)
        notification_type_grid.setColumnStretch(3, 1)
        notification_type_grid.addWidget(self.both_qrb, 0, 0)
        notification_type_grid.addWidget(self.visual_qrb, 0, 1)
        notification_type_grid.addWidget(self.audio_qrb, 0, 2)
        notification_type_grid.setSpacing(0)
        notification_type_qgb = QtWidgets.QGroupBox()
        notification_type_qgb.setStyleSheet("border: none;")
        notification_type_qgb.setLayout(notification_type_grid)

        notification_interval_qhl = QtWidgets.QHBoxLayout()
        notification_interval_qhl.addWidget(QtWidgets.QLabel(self.tr("Interval every:")))
        notification_interval_qhl.addWidget(self.notification_interval_qsb)
        notification_interval_qhl.addWidget(QtWidgets.QLabel(self.tr("minutes")))
        notification_interval_qhl.addStretch(1)

        # Settings for the breathing dialog
        dialog_qhl = QtWidgets.QHBoxLayout()
        dialog_qhl.addWidget(H2(self.tr("Dialog")))
        dialog_qhl.addStretch(1)
        dialog_qhl.addWidget(QtWidgets.QLabel(self.tr("Close on hover")))
        dialog_qhl.addWidget(self.close_on_hover_qcb)
        dialog_qhl.setSpacing(20)

        dialog_type_grid = PageGrid()
        dialog_type_grid.setColumnMinimumWidth(0, 120)
        dialog_type_grid.setColumnMinimumWidth(1, 125)
        dialog_type_grid.setColumnStretch(2, 1)
        dialog_type_grid.addWidget(self.same_qrb, 0, 0)
        dialog_type_grid.addWidget(self.random_qrb, 0, 1)
        dialog_type_grid.setSpacing(0)
        dialog_type_qgb = QtWidgets.QGroupBox()
        dialog_type_qgb.setStyleSheet("border: none;")
        dialog_type_qgb.setLayout(dialog_type_grid)

        show_after_qhl = QtWidgets.QHBoxLayout()
        show_after_qhl.addWidget(QtWidgets.QLabel(self.tr("Show after:")))
        show_after_qhl.addWidget(self.show_after_qsb)
        show_after_qhl.addWidget(QtWidgets.QLabel(self.tr("notifications")))
        show_after_qhl.addStretch(1)

        # Settings for notification audio
        self.notif_volume_qsr.setOrientation(QtCore.Qt.Horizontal)
        self.notif_volume_qsr.setMinimum(0)
        self.notif_volume_qsr.setMaximum(100)
        notif_audio_qhl = QtWidgets.QHBoxLayout()
        notif_audio_qhl.addWidget(self.notif_select_audio_qpb)
        notif_audio_qhl.addWidget(self.notif_volume_qsr)

        # Settings for prepare audio
        self.prep_volume_qsr.setOrientation(QtCore.Qt.Horizontal)
        self.prep_volume_qsr.setMinimum(0)
        self.prep_volume_qsr.setMaximum(100)
        prep_audio_qhl = QtWidgets.QHBoxLayout()
        prep_audio_qhl.addWidget(self.prep_select_audio_qpb)
        prep_audio_qhl.addWidget(self.prep_volume_qsr)

        # PUT EVERYTHING ON THE PAGE......
        grid = PageGrid()

        # first grid column
        grid.addWidget(self.toggle_switch, 0, 0)
        grid.addWidget(H2(self.tr("Notifications")), 1, 0)
        grid.addWidget(HorizontalLine(), 2, 0)
        grid.addWidget(QtWidgets.QLabel(self.tr("Notification type")), 3, 0)
        grid.addWidget(notification_type_qgb, 4, 0)
        # grid.addLayout(notification_interval_qhl, 5, 0)
        # grid.addWidget(QtWidgets.QLabel(), 5, 0)
        grid.addWidget(QtWidgets.QLabel(self.tr("Notification Audio")), 6, 0)
        grid.addLayout(notif_audio_qhl, 7, 0)
        grid.addWidget(QtWidgets.QLabel(), 8, 0)
        grid.addLayout(dialog_qhl, 9, 0)
        grid.addWidget(HorizontalLine(), 10, 0)
        grid.addWidget(QtWidgets.QLabel(self.tr("Do you always want the same phrase or a random one?")), 11, 0)
        grid.addWidget(dialog_type_qgb, 12, 0)
        # grid.addLayout(show_after_qhl, 13, 0)
        grid.addWidget(QtWidgets.QLabel(self.tr("Dialog Audio")), 13, 0)
        grid.addLayout(prep_audio_qhl, 14, 0)

        # second grid column
        grid.addWidget(self.phrases_qlw, 0, 1, 14, 1)

        vbox_l2 = QtWidgets.QVBoxLayout()
        vbox_l2.addWidget(H1(self.tr("Settings for Breathing")))
        vbox_l2.addWidget(HorizontalLine())
        vbox_l2.addStretch(1)
        vbox_l2.addLayout(grid)
        vbox_l2.addStretch(3)
        self.setLayout(vbox_l2)

        self.update_gui()

    def _connect_slots_to_signals(self):
        self.toggle_switch.toggled_signal.connect(self.on_switch_toggled)
        self.notification_interval_qsb.valueChanged.connect(
            self.on_breathing_interval_value_changed
        )
        self.show_after_qsb.valueChanged.connect(
            self.on_notifications_per_dialog_qsb_changed
        )
        self.close_on_hover_qcb.toggled.connect(self.on_dialog_close_on_hover_toggled)
        self.notif_select_audio_qpb.clicked.connect(self.on_notif_select_audio_clicked)
        self.prep_select_audio_qpb.clicked.connect(self.on_prep_select_audio_clicked)
        self.notif_volume_qsr.valueChanged.connect(self.notif_volume_changed)
        self.prep_volume_qsr.valueChanged.connect(self.prep_volume_changed)
        self.audio_qrb.clicked.connect(self.on_notification_type_audio_activated)
        self.visual_qrb.clicked.connect(self.on_notification_type_visual_activated)
        self.both_qrb.clicked.connect(self.on_notification_type_both_activated)
        self.same_qrb.clicked.connect(self.on_phrase_selection_same_activated)
        self.random_qrb.clicked.connect(self.on_phrase_selection_random_activated)

    def on_phrase_selection_same_activated(self, i_index: int):
        print('on phrase selection same activated works')
        # -activated is only triggered on user action (and not programmatically)
        mc.model.SettingsM.update_breathing_dialog_phrase_selection(0)

    def on_phrase_selection_random_activated(self, i_index: int):
        print('on phrase selection random activated works')
        # -activated is only triggered on user action (and not programmatically)
        mc.model.SettingsM.update_breathing_dialog_phrase_selection(1)

    def on_dialog_close_on_hover_toggled(self, i_checked: bool):
        print('on close on hover toggled works')
        if self.updating_gui_bool:
            return
        mc.model.SettingsM.update_breathing_dialog_close_on_hover(i_checked)

    def on_dialog_audio_toggled(self, i_checked: bool):
        if self.updating_gui_bool:
            return
        mc.model.SettingsM.update_breathing_dialog_audio_active(i_checked)

    def on_phrase_setup_activated(self, i_index: int):
        print('on phrase setup activated works')
        # -activated is only triggered on user action (and not programmatically)
        mc.model.SettingsM.update_breathing_reminder_notification_phrase_setup(i_index)

    def on_notification_type_audio_activated(self):
        print('on notification type audio activated works')
        print(mc_global.NotificationType.Audio.value)
        # -activated is only triggered on user action (and not programmatically)
        mc.model.SettingsM.update_breathing_reminder_notification_type(mc_global.NotificationType.Audio.value)

    def on_notification_type_visual_activated(self):
        print('on notification type audio activated works')
        print(mc_global.NotificationType.Visual.value)
        # -activated is only triggered on user action (and not programmatically)
        mc.model.SettingsM.update_breathing_reminder_notification_type(mc_global.NotificationType.Visual.value)

    def on_notification_type_both_activated(self):
        print('on notification type audio activated works')
        print(mc_global.NotificationType.Both.value)
        # -activated is only triggered on user action (and not programmatically)
        mc.model.SettingsM.update_breathing_reminder_notification_type(mc_global.NotificationType.Both.value)

    def on_notifications_per_dialog_qsb_changed(self, i_new_value: int):
        print('on notificatios per dialog changed works')
        if self.updating_gui_bool:
            return
        mc.model.SettingsM.update_breathing_reminder_nr_per_dialog(i_new_value)

    def prep_volume_changed(self, i_value: int):
        print('prep volume changed')
        if self.updating_gui_bool:
            return
        mc.model.SettingsM.update_prep_reminder_audio_volume(i_value)

    def notif_volume_changed(self, i_value: int):
        print('on notification volume changed works')
        if self.updating_gui_bool:
            return
        mc.model.SettingsM.update_breathing_reminder_volume(i_value)

    def on_prep_select_audio_clicked(self):
        print('prep select audio clicked')
        # noinspection PyCallByClass
        audio_file_result_tuple = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Please choose a wav audio file"),
            mc_global.get_user_audio_path(),
            self.tr("Wav files (*.wav)")
        )
        new_file_path_str = audio_file_result_tuple[0]
        if new_file_path_str:
            new_filename_str = os.path.basename(new_file_path_str)  # -we store the name rather than the path
            mc.model.SettingsM.update_prep_reminder_audio_filename(new_filename_str)
        else:
            pass
        self.prep_update_gui_audio_details()

    def on_notif_select_audio_clicked(self):
        print('notif select audio clicked')
        # noinspection PyCallByClass
        audio_file_result_tuple = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Please choose a wav audio file"),
            mc_global.get_user_audio_path(),
            self.tr("Wav files (*.wav)")
        )
        new_file_path_str = audio_file_result_tuple[0]
        if new_file_path_str:
            new_filename_str = os.path.basename(new_file_path_str)  # -we store the name instead of the path
            mc.model.SettingsM.update_breathing_reminder_audio_filename(new_filename_str)
        else:
            pass
        self.notif_update_gui_audio_details()

    def prep_update_gui_audio_details(self):
        self.updating_gui_bool = True
        settings = mc.model.SettingsM.get()

        audio_path_str = settings.prep_reminder_audio_filename
        audio_file_name_str = os.path.basename(audio_path_str)
        if audio_file_name_str:
            self.prep_select_audio_qpb.setText(audio_file_name_str)
        else:
            self.prep_select_audio_qpb.setText(NO_AUDIO_SELECTED_STR)

        self.close_on_hover_qcb.setChecked(settings.breathing_reminder_dialog_close_on_active_bool)
        self.prep_volume_qsr.setValue(settings.prep_reminder_audio_volume)

        self.updating_gui_bool = False

    def notif_update_gui_audio_details(self):
        self.updating_gui_bool = True
        settings = mc.model.SettingsM.get()

        audio_path_str = settings.breathing_reminder_audio_filename_str
        audio_file_name_str = os.path.basename(audio_path_str)
        if audio_file_name_str:
            self.notif_select_audio_qpb.setText(audio_file_name_str)
        else:
            self.notif_select_audio_qpb.setText(NO_AUDIO_SELECTED_STR)

        self.close_on_hover_qcb.setChecked(settings.breathing_reminder_dialog_close_on_active_bool)
        self.notif_volume_qsr.setValue(settings.breathing_reminder_audio_volume_int)

        self.updating_gui_bool = False

    def on_switch_toggled(self, i_checked_bool):
        print('on switch toggled updates model')
        if self.updating_gui_bool:
            return
        model.SettingsM.update_breathing_reminder_active(i_checked_bool)
        print('updated signal emitted')
        self.updated_signal.emit()

    def on_breathing_interval_value_changed(self, i_new_value: int):
        print('on breathing interval value changed')
        if self.updating_gui_bool:
            return
        model.SettingsM.update_breathing_reminder_interval(i_new_value)
        print('updated signal emitted')
        self.updated_signal.emit()

    def update_gui(self):
        self.updating_gui_bool = True
        settings = mc.model.SettingsM.get()
        if mc_global.active_phrase_id_it != mc_global.NO_PHRASE_SELECTED_INT:
            self.setDisabled(False)
        else:
            self.setDisabled(True)

        self.toggle_switch.update_gui(settings.breathing_reminder_active_bool)
        self.notification_interval_qsb.setValue(settings.breathing_reminder_interval_int)

        # TODO: Decide what to do with the active breathing phrase
        # self.notification_type_qcb.setCurrentText(settings.breathing_reminder_notification_type.name)
        # self.phrase_selection_qcb.setCurrentText(settings.breathing_dialog_phrase_selection.name)
        self.show_after_qsb.setValue(settings.breathing_reminder_nr_before_dialog_int)

        self.prep_update_gui_audio_details()
        self.notif_update_gui_audio_details()

        self.updating_gui_bool = False
