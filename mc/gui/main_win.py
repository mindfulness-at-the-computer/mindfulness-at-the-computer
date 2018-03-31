import logging
import sys
import os
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from mc import db

try:
    # noinspection PyUnresolvedReferences
    from PyQt5 import QtMultimedia
except ImportError:
    logging.debug("ImportError for QtMultimedia - maybe because there's no sound card available")
    # -If the system does not have a sound card (as for example Travis CI)
    # -An alternative to this approach is to use this: http://doc.qt.io/qt-5/qaudiodeviceinfo.html#availableDevices
import mc.gui.rest_action_list_wt
import mc.model
import mc.mc_global
import mc.gui.breathing_history_wt
import mc.gui.breathing_settings_wt
import mc.gui.breathing_phrase_list_wt
import mc.gui.general_settings_wt
import mc.gui.rest_settings_wt
import mc.gui.rest_dlg
import mc.gui.breathing_dlg
import mc.gui.breathing_notification
import mc.gui.rest_notification
import mc.gui.rest_dlg
import mc.gui.intro_dlg
import mc.gui.rest_prepare
import mc.gui.breathing_prepare
import mc.gui.suspend_time_dlg
import mc.gui.sysinfo_dlg
import mc.gui.intention_wt


class MainWin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.sys_tray = SystemTray()
        self.rest_reminder_dialog = None
        self.rest_widget = None
        self.tray_icon = None
        self.rest_reminder_qtimer = None
        self.breathing_qtimer = None
        self.suspend_qtimer = None
        self.rest_prepare_dialog = None
        self.intro_dlg = None
        self.breathing_notification = None
        self.breathing_dialog = None
        self.sound_effect = None
        try:
            self.sound_effect = QtMultimedia.QSoundEffect(self)
            # -PLEASE NOTE: A parent has to be given here, otherwise we will not hear anything
        except NameError:
            logging.debug(
                "NameError - Cannot play audio since QtMultimedia has not been imported"
            )

        self.active_breathing_phrase_qgb = QtWidgets.QGroupBox("Active Breathing Phrase")
        self.br_settings_wt = mc.gui.breathing_settings_wt.BreathingSettingsWt()
        self.br_phrase_list_wt = mc.gui.breathing_phrase_list_wt.BreathingPhraseListWt()
        self.rest_settings_wt = mc.gui.rest_settings_wt.RestSettingsWt()
        self.rest_action_list_wt = mc.gui.rest_action_list_wt.RestActionListWt()
        self.breathing_history_wt = mc.gui.breathing_history_wt.BreathingHistoryWt()

        db.Helper.get_new_db_connection()
        self.intentions_model = mc.model.IntentionsM()
        self.intention_form = mc.gui.intention_wt.IntentionForm(self.intentions_model)
        self.intention_widget = mc.gui.intention_wt.IntentionWidget(self.intentions_model)

        if QtCore.QSysInfo.kernelType() == 'darwin':
            self.run_on_startup_wt = mc.gui.general_settings_wt.RunOnStartupWt()
            self.run_on_startup_wt.run_on_startup_qcb.toggled.connect(self.run_on_startup_wt.on_run_on_startup_toggled)

        self._setup_initialize()

        main_container_hbox_l3 = self._setup_main_container()

        self._setup_add_first_panel_to_main_container(main_container_hbox_l3)
        self._setup_add_breathing_phrase_list_to_main_container(main_container_hbox_l3)
        self._setup_add_rest_action_list_to_main_container(main_container_hbox_l3)

        # Setup of Menu
        self.menu_bar = self.menuBar()
        self.update_menu()

        # Setup of Timers
        self.on_breathing_settings_changed()
        self.update_rest_timer()

        # Startup actions
        if not mc.mc_global.db_file_exists_at_application_startup_bl and not mc.mc_global.testing_bool:
            self.show_intro_dialog()
        self.open_breathing_prepare()

        self.setup_systray()

        self.minimize_to_tray()

    def _setup_initialize(self):
        self.setGeometry(100, 64, 900, 670)
        self.setWindowIcon(QtGui.QIcon(mc.mc_global.get_app_icon_path("icon.png")))
        self._setup_set_window_title()
        self.setStyleSheet(
            "selection-background-color:" + mc.mc_global.MC_LIGHT_GREEN_COLOR_STR + ";"
            "selection-color:#000000;"
        )

    def _setup_main_container(self) -> QtWidgets.QHBoxLayout:
        central_w2 = QtWidgets.QWidget()
        self.setCentralWidget(central_w2)
        main_container_hbox_l3 = QtWidgets.QHBoxLayout()
        central_w2.setLayout(main_container_hbox_l3)
        return main_container_hbox_l3

    def _setup_add_first_panel_to_main_container(self, main_container_hbox_l3):
        first_panel_vbox_l4 = self._setup_new_panel_in_main_window(main_container_hbox_l3)
        self._setup_configure_active_breathing_phrase(first_panel_vbox_l4)
        first_panel_vbox_l4.addWidget(self.breathing_history_wt)

        if hasattr(self, 'run_on_startup_wt'):
            first_panel_vbox_l4.addWidget(self.run_on_startup_wt)

    def _setup_configure_active_breathing_phrase(self, panel_vbox_l4):
        self.title_text_qll = QtWidgets.QLabel(self.tr("title"))
        self.title_text_qll.setWordWrap(True)
        self.in_text_qll = QtWidgets.QLabel(self.tr("in"))
        self.in_text_qll.setWordWrap(True)
        self.out_text_qll = QtWidgets.QLabel(self.tr("out"))
        self.out_text_qll.setWordWrap(True)
        active_breathing_phrase_vbox_l5 = QtWidgets.QVBoxLayout()
        active_breathing_phrase_vbox_l5.addWidget(self.title_text_qll)
        active_breathing_phrase_vbox_l5.addWidget(self.in_text_qll)
        active_breathing_phrase_vbox_l5.addWidget(self.out_text_qll)
        self.active_breathing_phrase_qgb.setLayout(active_breathing_phrase_vbox_l5)
        panel_vbox_l4.addWidget(self.active_breathing_phrase_qgb)

    def _setup_add_breathing_phrase_list_to_main_container(self, main_container_hbox_l3):
        breathing_phrase_list_vbox_l4 = self._setup_new_panel_in_main_window(main_container_hbox_l3)

        title_qll = QtWidgets.QLabel("Breathing")
        breathing_phrase_list_vbox_l4.addWidget(title_qll)
        title_qll.setFont(mc.mc_global.get_font_large(i_bold=True))
        title_qll.setContentsMargins(8, 0, 0, 0)
        # -unknown why we need to set this manually,
        #  we don't have to do this for the widgets below in the visual layout

        breathing_phrase_list_vbox_l4.addWidget(self.br_phrase_list_wt)
        self.br_phrase_list_wt.selection_changed_signal.connect(self.on_breathing_list_row_changed)
        self.br_phrase_list_wt.phrase_changed_signal.connect(self.on_breathing_phrase_changed)
        self._setup_configure_breathing_settings(breathing_phrase_list_vbox_l4)

    def _setup_add_rest_action_list_to_main_container(self, main_container_hbox_l3):
        rest_action_list_vbox_l4 = self._setup_new_panel_in_main_window(main_container_hbox_l3)

        title_qll = QtWidgets.QLabel("Resting")
        rest_action_list_vbox_l4.addWidget(title_qll)
        title_qll.setFont(mc.mc_global.get_font_large(i_bold=True))
        title_qll.setContentsMargins(8, 0, 0, 0)

        rest_action_list_vbox_l4.addWidget(self.rest_action_list_wt)
        self.rest_action_list_wt.update_signal.connect(self.on_rest_action_list_updated)
        self.rest_action_list_wt.selection_changed_signal.connect(self.on_rest_action_list_row_changed)
        self._setup_configure_rest_settings(rest_action_list_vbox_l4)

    @staticmethod
    def _setup_new_panel_in_main_window(main_container_hbox_l3) -> QtWidgets.QVBoxLayout:
        panel_vbox_l4 = QtWidgets.QVBoxLayout()
        main_container_hbox_l3.addLayout(panel_vbox_l4)
        return panel_vbox_l4

    def _setup_configure_rest_settings(self, rest_action_list_vbox_l4):
        rest_action_list_vbox_l4.addWidget(self.rest_settings_wt)
        self.rest_settings_wt.settings_updated_signal.connect(self.update_rest_timer)
        self.rest_settings_wt.rest_now_button_clicked_signal.connect(self.on_rest_rest)
        self.rest_settings_wt.rest_reset_button_clicked_signal.connect(self.update_rest_timer)
        self.rest_settings_wt.rest_slider_value_changed_signal.connect(self.on_rest_slider_value_changed)

    def _setup_configure_breathing_settings(self, breathing_phrase_list_vbox_l4):
        breathing_phrase_list_vbox_l4.addWidget(self.br_settings_wt)
        self.br_settings_wt.updated_signal.connect(self.on_breathing_settings_changed)
        self.br_settings_wt.breathe_now_button_clicked_signal.connect(self.open_breathing_dialog)

    def _setup_set_window_title(self):
        if mc.mc_global.testing_bool:
            data_storage_str = "{Testing - data stored in memory}"
        else:
            data_storage_str = "{Live - data stored on hard drive}"
        window_title_str = (
            mc.mc_global.APPLICATION_TITLE_STR
            + " [" + mc.mc_global.APPLICATION_VERSION_STR + "] "
            + data_storage_str
        )
        self.setWindowTitle(window_title_str)

    # noinspection PyAttributeOutsideInit
    def setup_systray(self):
        """
        System tray
        Please note: We cannot move the update code into another function, even in
        this file (very strange). If we do, we won't see the texts, only the separators,
        don't know why, potential bug.
        """
        self.tray_icon = QtWidgets.QSystemTrayIcon(
            QtGui.QIcon(self.get_app_systray_icon_path()),
            self
        )
        # self.tray_icon.activated.connect(self.on_systray_activated)
        self.tray_icon.show()

        systray_available_str = "No"
        if self.tray_icon.isSystemTrayAvailable():
            systray_available_str = "Yes"
        mc.mc_global.sys_info_telist.append(("System tray available", systray_available_str))
        notifications_supported_str = "No"
        if self.tray_icon.supportsMessages():
            notifications_supported_str = "Yes"
        mc.mc_global.sys_info_telist.append(("System tray notifications supported", notifications_supported_str))
        sys_info = QtCore.QSysInfo()
        mc.mc_global.sys_info_telist.append(("buildCpuArchitecture", sys_info.buildCpuArchitecture()))
        mc.mc_global.sys_info_telist.append(("currentCpuArchitecture", sys_info.currentCpuArchitecture()))
        mc.mc_global.sys_info_telist.append(("kernel type", sys_info.kernelType()))
        mc.mc_global.sys_info_telist.append(("kernel version", sys_info.kernelVersion()))
        mc.mc_global.sys_info_telist.append(("product name and version", sys_info.prettyProductName()))
        logging.info("##### System Information #####")
        for (descr_str, value) in mc.mc_global.sys_info_telist:
            logging.info(descr_str + ": " + str(value))
        logging.info("#####")

        settings = mc.model.SettingsM.get()

        self.tray_menu = QtWidgets.QMenu(self)

        self.sys_tray.rest_enabled_qaction = QtWidgets.QAction(self.tr("Enable Rest Reminder"))
        self.tray_menu.addAction(self.sys_tray.rest_enabled_qaction)
        self.sys_tray.rest_enabled_qaction.setCheckable(True)
        self.sys_tray.rest_enabled_qaction.toggled.connect(
            self.rest_settings_wt.on_switch_toggled
        )
        self.sys_tray.rest_enabled_qaction.setChecked(settings.rest_reminder_active)
        self.sys_tray.rest_progress_qaction = QtWidgets.QAction("")
        self.tray_menu.addAction(self.sys_tray.rest_progress_qaction)
        self.sys_tray.rest_progress_qaction.setDisabled(True)
        self.sys_tray.update_rest_progress_bar(0, 1)
        self.tray_rest_reset_qaction = QtWidgets.QAction(self.tr("Reset Rest Timer (Skip Break)"))
        self.tray_menu.addAction(self.tray_rest_reset_qaction)
        self.tray_rest_reset_qaction.triggered.connect(self.on_rest_skip)
        self.tray_rest_now_qaction = QtWidgets.QAction(self.tr("Take a Break Now"))
        self.tray_menu.addAction(self.tray_rest_now_qaction)
        self.tray_rest_now_qaction.triggered.connect(self.on_rest_rest)

        self.tray_menu.addSeparator()

        self.sys_tray.breathing_enabled_qaction = QtWidgets.QAction(self.tr("Enable Breathing Reminder"))
        self.tray_menu.addAction(self.sys_tray.breathing_enabled_qaction)
        self.sys_tray.breathing_enabled_qaction.setCheckable(True)
        self.sys_tray.breathing_enabled_qaction.setChecked(settings.breathing_reminder_active_bool)
        self.sys_tray.breathing_enabled_qaction.toggled.connect(
            self.br_settings_wt.on_switch_toggled
        )

        self.tray_open_breathing_dialog_qaction = QtWidgets.QAction(self.tr("Open Breathing Dialog"))
        self.tray_menu.addAction(self.tray_open_breathing_dialog_qaction)
        self.tray_open_breathing_dialog_qaction.triggered.connect(self.open_breathing_dialog)

        self.tray_menu.addSeparator()

        self.tray_open_intention_widget_qaction = QtWidgets.QAction(self.tr("Open My intentions"))
        self.tray_open_intention_widget_qaction.triggered.connect(self.open_intention_widget)
        self.tray_menu.addAction(self.tray_open_intention_widget_qaction)

        self.tray_menu.addSeparator()

        self.tray_suspend_action = QtWidgets.QAction(self.tr("Suspend Application"))
        self.tray_menu.addAction(self.tray_suspend_action)
        self.tray_suspend_action.triggered.connect(self.on_suspend_application_clicked)
        self.tray_restore_action = QtWidgets.QAction(self.tr("Open Settings"))
        self.tray_menu.addAction(self.tray_restore_action)
        self.tray_restore_action.triggered.connect(self.restore_window)
        self.tray_quit_action = QtWidgets.QAction(self.tr("Quit"))
        self.tray_menu.addAction(self.tray_quit_action)
        self.tray_quit_action.triggered.connect(self.exit_application)

        self.tray_icon.setContextMenu(self.tray_menu)

    def on_rest_action_list_updated(self):
        self.update_gui(mc.mc_global.EventSource.rest_action_changed)

    def on_systray_activated(self, i_reason):
        # LXDE:
        # XFCE:
        # MacOS:
        logging.debug("===== on_systray_activated entered =====")
        logging.debug("i_reason = " + str(i_reason))
        logging.debug("mouseButtons() = " + str(QtWidgets.QApplication.mouseButtons()))
        self.tray_icon.activated.emit(i_reason)
        """
        if i_reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.restore_window()
        else:
            self.tray_icon.activated.emit(i_reason)
        """
        logging.debug("===== on_systray_activated exited =====")

    def on_breathing_list_row_changed(self, i_details_enabled: bool):
        self.update_breathing_timer()
        self.br_settings_wt.setEnabled(i_details_enabled)
        self.sys_tray.breathing_enabled_qaction.setEnabled(i_details_enabled)

        self.update_gui(mc.mc_global.EventSource.breathing_list_selection_changed)

    def on_rest_action_list_row_changed(self):
        self.update_gui(mc.mc_global.EventSource.rest_list_selection_changed)

    def on_breathing_phrase_changed(self, i_details_enabled):
        self.update_breathing_timer()
        self.br_settings_wt.setEnabled(i_details_enabled)
        self.sys_tray.breathing_enabled_qaction.setEnabled(i_details_enabled)

        self.update_gui(mc.mc_global.EventSource.breathing_list_phrase_updated)

    def stop_suspend_timer(self):
        if self.suspend_qtimer is not None and self.suspend_qtimer.isActive():
            self.suspend_qtimer.stop()

    def start_suspend_timer(self, i_minutes: int):
        if i_minutes == 0:
            logging.debug("Resuming application (after suspending)")
            self.stop_suspend_timer()
        logging.debug("Suspending the application for " + str(i_minutes) + " minutes")

        self.stop_rest_timer()
        self.stop_breathing_timer()

        self.suspend_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.suspend_qtimer.setSingleShot(True)  # <-------
        self.suspend_qtimer.timeout.connect(self.suspend_timer_timeout)
        self.suspend_qtimer.start(i_minutes * 60 * 1000)
        self.update_gui()

    def suspend_timer_timeout(self):
        self.stop_suspend_timer()  # -making sure that this is stopped, just in case

        self.start_rest_timer()
        self.start_breathing_timer()
        self.update_gui()

    def update_rest_timer(self):
        settings = mc.model.SettingsM.get()
        if settings.rest_reminder_active:
            self.start_rest_timer()
        else:
            self.stop_rest_timer()
        self.update_gui(mc.mc_global.EventSource.rest_settings_changed)

    def on_rest_slider_value_changed(self):
        self.update_gui(mc.mc_global.EventSource.rest_slider_value_changed)

    def stop_rest_timer(self):
        if self.rest_reminder_qtimer is not None and self.rest_reminder_qtimer.isActive():
            self.rest_reminder_qtimer.stop()
        self.rest_settings_wt.update_gui()  # -so that the progressbar is updated

    def start_rest_timer(self):
        mc.mc_global.rest_reminder_minutes_passed_int = 0
        self.stop_rest_timer()
        self.rest_reminder_qtimer = QtCore.QTimer(self)
        self.rest_reminder_qtimer.timeout.connect(self.rest_timer_timeout)
        self.rest_reminder_qtimer.start(60 * 1000)  # -one minute

    def rest_timer_timeout(self):
        if mc.mc_global.rest_window_shown_bool:
            return
        mc.mc_global.rest_reminder_minutes_passed_int += 1
        if (mc.mc_global.rest_reminder_minutes_passed_int
        == mc.model.SettingsM.get().rest_reminder_interval_int - 1):
            # self.tray_icon.showMessage("Mindfulness at the Computer", "One minute left until the next rest")
            self.show_rest_prepare()
        if (mc.mc_global.rest_reminder_minutes_passed_int
        == mc.model.SettingsM.get().rest_reminder_interval_int):
            self.start_rest_reminder()
        self.rest_settings_wt.rest_reminder_qsr.setValue(
            mc.mc_global.rest_reminder_minutes_passed_int
        )

    def on_rest_widget_closed(self, i_open_breathing_dialog: bool):
        mc.mc_global.rest_reminder_minutes_passed_int = 0

        if i_open_breathing_dialog:
            self.open_breathing_dialog()
        self.update_rest_timer()
        self.update_breathing_timer()
        self.update_gui()

    def on_rest_widget_closed_and_intention_widget_opened(self):
        self.intention_widget.list_view_buttons.on_add_clicked()

    def restore_window(self):
        self.raise_()
        self.showNormal()
        # another alternative (from an SO answer): self.setWindowState(QtCore.Qt.WindowActive)

    def show_rest_prepare(self):
        self.rest_prepare_dialog = mc.gui.rest_prepare.RestPrepareDlg()

    def start_rest_reminder(self):
        notification_type_int = mc.model.SettingsM.get().rest_reminder_notification_type_int

        if (notification_type_int == mc.mc_global.NotificationType.Both.value
        or notification_type_int == mc.mc_global.NotificationType.Visual.value):
            self.show_rest_reminder()

        if (notification_type_int == mc.mc_global.NotificationType.Both.value
        or notification_type_int == mc.mc_global.NotificationType.Audio.value):
            settings = mc.model.SettingsM.get()
            audio_path_str = settings.rest_reminder_audio_path_str
            volume_int = settings.rest_reminder_volume_int
            self._play_audio(audio_path_str, volume_int)

    def show_rest_reminder(self):
        self.rest_reminder_dialog = mc.gui.rest_notification.RestReminderDlg()
        self.rest_reminder_dialog.rest_signal.connect(self.on_rest_rest)
        self.rest_reminder_dialog.skip_signal.connect(self.on_rest_skip)
        self.rest_reminder_dialog.wait_signal.connect(self.on_rest_wait)
        self.update_gui(mc.mc_global.EventSource.rest_opened)

    def on_rest_wait(self):
        mc.mc_global.rest_reminder_minutes_passed_int -= 2
        self.update_gui()

    def on_rest_rest(self):
        self.rest_widget = mc.gui.rest_dlg.RestDlg()
        self.rest_widget.close_signal.connect(self.on_rest_widget_closed)
        self.rest_widget.intention_signal.connect(self.on_rest_widget_closed_and_intention_widget_opened)

    def on_rest_skip(self):
        mc.mc_global.rest_reminder_minutes_passed_int = 0
        self.update_gui()

    def on_breathing_settings_changed(self):
        self.update_breathing_timer()
        self.update_gui(mc.mc_global.EventSource.breathing_settings_changed)

    def update_breathing_timer(self):
        settings = mc.model.SettingsM.get()
        if settings.breathing_reminder_active_bool:
            self.start_breathing_timer()
        else:
            self.stop_breathing_timer()

    def stop_breathing_timer(self):
        if self.breathing_qtimer is not None and self.breathing_qtimer.isActive():
            self.breathing_qtimer.stop()

    def start_breathing_timer(self):
        self.stop_breathing_timer()
        settings = mc.model.SettingsM.get()
        self.breathing_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.breathing_qtimer.timeout.connect(self.breathing_timer_timeout)
        # -show_breathing_notification
        self.breathing_qtimer.start(settings.breathing_reminder_interval_int * 60 * 1000)

    def update_menu(self):
        self.menu_bar.clear()

        file_menu = self.menu_bar.addMenu(self.tr("&File"))
        export_action = QtWidgets.QAction(self.tr("Export data"), self)
        file_menu.addAction(export_action)
        export_action.triggered.connect(mc.model.export_all)
        minimize_to_tray_action = QtWidgets.QAction(self.tr("Minimize to tray"), self)
        file_menu.addAction(minimize_to_tray_action)
        minimize_to_tray_action.triggered.connect(self.minimize_to_tray)
        """
        choose_file_directory_action = QtWidgets.QAction(self.tr("Choose file directory"), self)
        file_menu.addAction(choose_file_directory_action)
        choose_file_directory_action.triggered.connect(pass)
        """
        quit_action = QtWidgets.QAction(self.tr("Quit"), self)
        file_menu.addAction(quit_action)
        quit_action.triggered.connect(self.exit_application)

        """
        preferences_menu = self.menu_bar.addMenu("&Preferences")
        """

        options_menu = self.menu_bar.addMenu("&Options")
        suspend_application_action = QtWidgets.QAction("Suspend application", self)
        options_menu.addAction(suspend_application_action)
        suspend_application_action.triggered.connect(self.on_suspend_application_clicked)

        debug_menu = self.menu_bar.addMenu("&Debug")
        update_gui_action = QtWidgets.QAction("Update GUI", self)
        debug_menu.addAction(update_gui_action)
        update_gui_action.triggered.connect(self.update_gui)
        breathing_full_screen_action = QtWidgets.QAction(self.tr("Full screen"), self)
        debug_menu.addAction(breathing_full_screen_action)
        breathing_full_screen_action.triggered.connect(self.showFullScreen)
        show_rest_reminder_action = QtWidgets.QAction(self.tr("Show rest reminder"), self)
        debug_menu.addAction(show_rest_reminder_action)
        show_rest_reminder_action.triggered.connect(self.start_rest_reminder)
        show_rest_prepare_action = QtWidgets.QAction("Show rest prepare", self)
        debug_menu.addAction(show_rest_prepare_action)
        show_rest_prepare_action.triggered.connect(self.show_rest_prepare)
        show_breathing_notification_action = QtWidgets.QAction("Show breathing notification", self)
        debug_menu.addAction(show_breathing_notification_action)
        show_breathing_notification_action.triggered.connect(self.breathing_timer_timeout)

        help_menu = self.menu_bar.addMenu(self.tr("&Help"))
        show_intro_dialog_action = QtWidgets.QAction("Show intro wizard", self)
        help_menu.addAction(show_intro_dialog_action)
        show_intro_dialog_action.triggered.connect(self.show_intro_dialog)
        about_action = QtWidgets.QAction(self.tr("About"), self)
        help_menu.addAction(about_action)
        about_action.triggered.connect(self.show_about_box)
        online_help_action = QtWidgets.QAction("Online help", self)
        help_menu.addAction(online_help_action)
        online_help_action.triggered.connect(self.show_online_help)
        sysinfo_action = QtWidgets.QAction(self.tr("System Information"), self)
        help_menu.addAction(sysinfo_action)
        sysinfo_action.triggered.connect(self.show_sysinfo_box)

    def on_suspend_application_clicked(self):

        self._suspend_time_dlg = mc.gui.suspend_time_dlg.SuspendTimeDialog()
        self._suspend_time_dlg.finished.connect(self.on_suspend_time_dlg_finished)
        self._suspend_time_dlg.show()
        """
        minutes_to_suspend_te = QtWidgets.QInputDialog.getInt(
            self, "title", "label", value=0, min=0, max=180
        )
        logging.debug("minutes_to_suspend_te = " + str(minutes_to_suspend_te))
        """

    def on_suspend_time_dlg_finished(self, i_result: int):
        if i_result == QtWidgets.QDialog.Accepted:
            self.start_suspend_timer(self._suspend_time_dlg.suspend_time_qsr.value())
        else:
            pass

    def show_intro_dialog(self):
        self.intro_dlg = mc.gui.intro_dlg.IntroDlg()
        self.intro_dlg.close_signal.connect(self.on_intro_dialog_closed)
        self.intro_dlg.exec()
        self.update_gui()

    def on_intro_dialog_closed(self, i_open_breathing_dialog: bool):
        if i_open_breathing_dialog:
            self.open_breathing_dialog()

    # noinspection PyAttributeOutsideInit
    def breathing_timer_timeout(self):
        if not self.breathing_reminder_active():
            return
        if mc.mc_global.rest_window_shown_bool:
            return

        mc.mc_global.breathing_notification_counter_int += 1
        if (mc.mc_global.breathing_notification_counter_int
        > mc.model.SettingsM.get().breathing_reminder_nr_before_dialog_int):
            mc.mc_global.breathing_notification_counter_int = 0
            self.open_breathing_prepare()
        else:
            self.commence_breathing_notification()

    def commence_breathing_notification(self):
        # Skipping the breathing notification if the breathing dialog is shown
        logging.debug("self.breathing_dialog.isVisible = " + str(self.breathing_dialog.isVisible()))
        if self.breathing_dialog.isVisible():
            return

        notification_type_int = mc.model.SettingsM.get().breathing_reminder_notification_type_int

        if (notification_type_int == mc.mc_global.NotificationType.Both.value
        or notification_type_int == mc.mc_global.NotificationType.Visual.value):
            self.breathing_notification = mc.gui.breathing_notification.BreathingNotification()
            self.breathing_notification.breathe_signal.connect(self.on_breathing_dialog_breathe_clicked)
            self.breathing_notification.show()

        if (notification_type_int == mc.mc_global.NotificationType.Both.value
        or notification_type_int == mc.mc_global.NotificationType.Audio.value):
            settings = mc.model.SettingsM.get()
            audio_path_str = settings.breathing_reminder_audio_path_str
            volume_int = settings.breathing_reminder_volume_int
            self._play_audio(audio_path_str, volume_int)

    def open_breathing_prepare(self):
        self.breathing_prepare = mc.gui.breathing_prepare.BreathingPrepareDlg()
        self.breathing_prepare.closed_signal.connect(self.open_breathing_dialog)

    def open_breathing_dialog(self):
        self.breathing_dialog = mc.gui.breathing_dlg.BreathingDlg()
        self.breathing_dialog.close_signal.connect(self.on_breathing_dialog_closed)
        self.breathing_dialog.phrase_changed_signal.connect(self.on_breathing_dialog_phrase_changed)
        self.breathing_dialog.show()

        settings = mc.model.SettingsM.get()
        if settings.breathing_reminder_dialog_audio_active_bool:
            audio_path_str = settings.breathing_reminder_audio_path_str
            volume_int = settings.breathing_reminder_volume_int
            self._play_audio(audio_path_str, volume_int)

    def open_intention_widget(self):
        self.intention_widget.show()

    def _play_audio(self, i_audio_path: str, i_volume: int) -> None:
        if self.sound_effect is None:
            return
        # noinspection PyCallByClass
        self.sound_effect.setSource(QtCore.QUrl.fromLocalFile(i_audio_path))
        self.sound_effect.setVolume(float(i_volume / 100))
        self.sound_effect.play()

    def on_breathing_dialog_closed(self, i_ib_list, i_ob_list):
        self.breathing_history_wt.add_from_dialog(i_ib_list, i_ob_list)
        self.update_breathing_timer()

    def on_breathing_dialog_phrase_changed(self):
        self.update_gui()

    def on_breathing_dialog_breathe_clicked(self):
        self.breathing_dialog = mc.gui.breathing_dlg.BreathingDlg()
        self.breathing_dialog.close_signal.connect(self.on_breathing_dialog_closed)
        self.breathing_dialog.phrase_changed_signal.connect(self.on_breathing_dialog_phrase_changed)
        self.breathing_dialog.show()

    def debug_clear_breathing_phrase_selection(self):
        self.br_phrase_list_wt.list_widget.clearSelection()

    def show_online_help(self):
        url_str = "https://mindfulness-at-the-computer.github.io/user_guide"
        # noinspection PyCallByClass
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url_str))
        # Python: webbrowser.get(url_str) --- doesn't work

    def show_sysinfo_box(self):
        self._sysinfo_dlg = mc.gui.sysinfo_dlg.SysinfoDialog()
        self._sysinfo_dlg.show()

        """
        info_str = '\n'.join([
            descr_str + ": " + str(value) for (descr_str, value) in mc.mc_global.sys_info_telist
        ])
        # noinspection PyCallByClass
        QtWidgets.QMessageBox.about(
            self,
            "System Information",
            info_str
        )
        """

    def show_about_box(self):
        # noinspection PyCallByClass
        QtWidgets.QMessageBox.about(
            self,
            "About Mindfulness at the Computer",
            (
                '<html>'
                'Originally created by Tord Dellsén'
                '<a href="https://sunyatazero.github.io/"> Github website</a><br>'
                '<a href="https://github.com/SunyataZero/mindfulness-at-the-computer/graphs/contributors">'
                'All contributors</a><br>'
                'Photography for application icon by Torgny Dellsén '
                '<a href="http://torgnydellsen.zenfolio.com">torgnydellsen.zenfolio.com</a><br>'
                'Other icons from Open Iconic - useiconic.com - MIT license<br>'
                'Other images (for the rest actions) have been released into the public domain (CC0)<br>'
                'Audio files have been released into the public domain (CC0)<br>'
                'Software License: GPLv3 (license text available in the install directory)'
                '</html>'
            )
        )

    # overridden
    # noinspection PyPep8Naming
    def closeEvent(self, i_QCloseEvent):
        i_QCloseEvent.ignore()
        self.minimize_to_tray()

    def minimize_to_tray(self):
        self.showMinimized()
        self.hide()

    def exit_application(self):
        sys.exit()

    def update_gui(self, i_event_source=mc.mc_global.EventSource.undefined):
        # self.breathing_widget.update_gui()
        # self.rest_widget.update_gui()

        if mc.mc_global.active_phrase_id_it == mc.mc_global.NO_PHRASE_SELECTED_INT:
            pass
        else:
            breathing_phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)
            self.title_text_qll.setText(breathing_phrase.title)
            self.in_text_qll.setText(breathing_phrase.ib)
            self.out_text_qll.setText(breathing_phrase.ob)

            if i_event_source != mc.mc_global.EventSource.rest_slider_value_changed:
                self.rest_settings_wt.update_gui()
            self.br_settings_wt.update_gui()

            if (i_event_source != mc.mc_global.EventSource.breathing_list_selection_changed
            and i_event_source != mc.mc_global.EventSource.rest_list_selection_changed):
                self.br_phrase_list_wt.update_gui()
                self.rest_action_list_wt.update_gui()

            self.update_systray()

    def get_app_systray_icon_path(self) -> str:
        # TODO: Update the three references to this function
        icon_file_name_str = "icon.png"
        settings = mc.model.SettingsM.get()
        if self.breathing_reminder_active() and settings.rest_reminder_active:
            icon_file_name_str = "icon-br.png"
        elif self.breathing_reminder_active():
            icon_file_name_str = "icon-b.png"
        elif settings.rest_reminder_active:
            icon_file_name_str = "icon-r.png"

        if self.suspend_qtimer is not None and self.suspend_qtimer.isActive():
            icon_file_name_str = "icon-suspend.png"

        ret_icon_path_str = mc.mc_global.get_app_icon_path(icon_file_name_str)
        return ret_icon_path_str

    def breathing_reminder_active(self) -> bool:
        settings = mc.model.SettingsM.get()
        breathing_reminder_active_bl = (
            (mc.mc_global.active_phrase_id_it != mc.mc_global.NO_PHRASE_SELECTED_INT)
            and
            settings.breathing_reminder_active_bool
        )
        return breathing_reminder_active_bl

    def update_systray(self):
        if self.tray_icon is None:
            return
        settings = mc.model.SettingsM.get()

        # Icon
        self.tray_icon.setIcon(QtGui.QIcon(self.get_app_systray_icon_path()))
        # self.tray_icon.show()

        # Menu
        self.sys_tray.update_breathing_checked(settings.breathing_reminder_active_bool)
        self.sys_tray.update_rest_checked(settings.rest_reminder_active)
        self.sys_tray.update_rest_progress_bar(
            mc.mc_global.rest_reminder_minutes_passed_int,
            mc.model.SettingsM.get().rest_reminder_interval_int
        )


class SystemTray:
    def __init__(self):
        self.rest_progress_qaction = None
        self.rest_enabled_qaction = None
        self.breathing_enabled_qaction = None

        self.phrase_qaction_list = []

    def update_rest_progress_bar(self, time_passed_int, interval_minutes_int):
        if self.rest_progress_qaction is None:
            return
        time_passed_str = ""
        parts_of_ten_int = (10 * time_passed_int) // interval_minutes_int
        for i in range(0, 9):
            if i < parts_of_ten_int:
                time_passed_str += "◾"
            else:
                time_passed_str += "◽"
        self.rest_progress_qaction.setText(time_passed_str)

    def update_rest_checked(self, i_active: bool):
        if self.rest_enabled_qaction is not None:
            self.rest_enabled_qaction.setChecked(i_active)

    def update_breathing_checked(self, i_checked: bool):
        if self.breathing_enabled_qaction is not None:
            self.breathing_enabled_qaction.setChecked(i_checked)

    def update_breathing_enabled(self, i_enabled: bool):
        if self.breathing_enabled_qaction is not None:
            self.breathing_enabled_qaction.setEnabled(i_enabled)
