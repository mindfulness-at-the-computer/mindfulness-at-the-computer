import logging
import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtMultimedia
import mc.gui.rest_action_list_wt
import mc.model
import mc.mc_global
import mc.gui.breathing_history_wt
import mc.gui.breathing_settings_wt
import mc.gui.breathing_phrase_list_wt
import mc.gui.rest_settings_wt
import mc.gui.rest_dlg
import mc.gui.breathing_popup
import mc.gui.rest_reminder_popup
import mc.gui.rest_dlg


class MainWin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 900, 600)
        self.setWindowIcon(QtGui.QIcon(mc.mc_global.get_app_icon_path()))

        self.sys_tray = SystemTray()

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

        self.setStyleSheet("selection-background-color:#bfef7f; selection-color:#000000;")

        self.rest_reminder_dialog = None
        self.rest_widget = None
        self.tray_icon = None
        self.rest_reminder_qtimer = None
        self.breathing_qtimer = None

        central_w2 = QtWidgets.QWidget()
        self.setCentralWidget(central_w2)
        hbox_l3 = QtWidgets.QHBoxLayout()
        central_w2.setLayout(hbox_l3)

        vbox_l4 = QtWidgets.QVBoxLayout()
        hbox_l3.addLayout(vbox_l4)

        self.br_phrase_list_wt = mc.gui.breathing_phrase_list_wt.BreathingPhraseListWt()
        vbox_l4.addWidget(self.br_phrase_list_wt)
        self.br_phrase_list_wt.selection_changed_signal.connect(self.on_breathing_list_row_changed)
        self.br_phrase_list_wt.phrase_changed_signal.connect(self.on_breathing_phrase_changed)

        self.br_settings_wt = mc.gui.breathing_settings_wt.BreathingSettingsWt()
        vbox_l4.addWidget(self.br_settings_wt)
        self.br_settings_wt.updated_signal.connect(self.on_breathing_settings_changed)
        self.br_settings_wt.breathe_now_button_clicked_signal.connect(self.show_breathing_dialog)

        vbox_l4 = QtWidgets.QVBoxLayout()
        hbox_l3.addLayout(vbox_l4)

        self.rest_action_list_wt = mc.gui.rest_action_list_wt.RestActionListWt()
        vbox_l4.addWidget(self.rest_action_list_wt)
        self.rest_action_list_wt.update_signal.connect(self.on_rest_action_list_updated)
        self.rest_action_list_wt.selection_changed_signal.connect(self.on_rest_action_list_row_changed)

        self.rest_settings_wt = mc.gui.rest_settings_wt.RestSettingsWt()
        vbox_l4.addWidget(self.rest_settings_wt)
        self.rest_settings_wt.settings_updated_signal.connect(self.on_rest_settings_changed)
        self.rest_settings_wt.rest_now_button_clicked_signal.connect(self.on_rest_rest)
        self.rest_settings_wt.rest_reset_button_clicked_signal.connect(self.on_rest_settings_changed)
        self.rest_settings_wt.rest_slider_value_changed_signal.connect(self.on_rest_slider_value_changed)

        self.breathing_history_wt = mc.gui.breathing_history_wt.BreathingHistoryWt()
        hbox_l3.addWidget(self.breathing_history_wt)

        # Setup of Menu
        self.menu_bar = self.menuBar()
        self.update_menu()

        # Setup of Timers
        self.on_breathing_settings_changed()
        self.on_rest_settings_changed()

        # Setup of Systray
        self.setup_systray()

    # noinspection PyAttributeOutsideInit
    def setup_systray(self):
        """
        System tray
        Please note: We cannot move the update code into another function, even in
        this file (very strange). If we do, we won't see the texts, only the separators,
        don't know why, potential bug.
        """
        self.tray_icon = QtWidgets.QSystemTrayIcon(
            QtGui.QIcon(mc.model.get_app_systray_icon_path()),
            self
        )
        self.tray_icon.activated.connect(self.on_systray_activated)
        self.tray_icon.show()

        logging.info("##### System Information #####")
        systray_available_str = "No"
        if self.tray_icon.isSystemTrayAvailable():
            systray_available_str = "Yes"
        logging.info("System tray available: " + systray_available_str)
        notifications_supported_str = "No"
        if self.tray_icon.supportsMessages():
            notifications_supported_str = "Yes"
        logging.info("System tray notifications supported: " + notifications_supported_str)
        sys_info = QtCore.QSysInfo()
        logging.info("buildCpuArchitecture: " + sys_info.buildCpuArchitecture())
        logging.info("currentCpuArchitecture: " + sys_info.currentCpuArchitecture())
        logging.info("kernel type and version: " + sys_info.kernelType() + " " + sys_info.kernelVersion())
        logging.info("product name and version: " + sys_info.prettyProductName())
        logging.info("#####")

        settings = mc.model.SettingsM.get()

        self.tray_menu = QtWidgets.QMenu(self)

        self.sys_tray.rest_enabled_qaction = QtWidgets.QAction("Enable Rest Reminder")
        self.tray_menu.addAction(self.sys_tray.rest_enabled_qaction)
        self.sys_tray.rest_enabled_qaction.setCheckable(True)
        self.sys_tray.rest_enabled_qaction.toggled.connect(
            self.rest_settings_wt.on_switch_toggled
        )
        self.sys_tray.rest_enabled_qaction.setChecked(settings.rest_reminder_active_bool)
        self.sys_tray.rest_progress_qaction = QtWidgets.QAction("")
        self.tray_menu.addAction(self.sys_tray.rest_progress_qaction)
        self.sys_tray.rest_progress_qaction.setDisabled(True)
        self.sys_tray.update_rest_progress_bar(0, 1)
        self.tray_rest_now_qaction = QtWidgets.QAction("Take a Break Now")
        self.tray_menu.addAction(self.tray_rest_now_qaction)
        self.tray_rest_now_qaction.triggered.connect(self.on_rest_rest)

        self.tray_menu.addSeparator()

        self.sys_tray.breathing_enabled_qaction = QtWidgets.QAction("Enable Breathing Reminder")
        self.tray_menu.addAction(self.sys_tray.breathing_enabled_qaction)
        self.sys_tray.breathing_enabled_qaction.setCheckable(True)
        self.sys_tray.breathing_enabled_qaction.setChecked(settings.breathing_reminder_active_bool)
        self.sys_tray.breathing_enabled_qaction.toggled.connect(
            self.br_settings_wt.on_switch_toggled
        )

        self.tray_open_breathing_dialog_qaction = QtWidgets.QAction("Open Breathing Dialog")
        self.tray_menu.addAction(self.tray_open_breathing_dialog_qaction)
        self.tray_open_breathing_dialog_qaction.triggered.connect(self.show_breathing_dialog)

        """
        self.sys_tray.phrase_qaction_list.clear()
        for (count, l_phrase) in enumerate(mc.model.PhrasesM.get_all()):
            INDENTATION_STR = "  "
            ACTIVE_MARKER_STR = "•"
            INACTIVE_MARKER_STR = " "
            active_or_inactive_str = INACTIVE_MARKER_STR
            if l_phrase.id_int == mc.mc_global.active_phrase_id_it:
                active_or_inactive_str = ACTIVE_MARKER_STR
            tray_phrase_qaction = QtWidgets.QAction(active_or_inactive_str + INDENTATION_STR + l_phrase.title_str)
            tray_phrase_qaction.triggered.connect(
                functools.partial(
                    self.br_phrase_list_wt.on_new_row_selected_from_system_tray,
                    l_phrase.id_int
                )
            )
            self.sys_tray.phrase_qaction_list.append(tray_phrase_qaction)
            # self.tray_phrase_qaction = QtWidgets.QAction(l_phrase.title_str)
            self.tray_menu.addAction(tray_phrase_qaction)
            if count >= 4:
                break
        """

        self.tray_menu.addSeparator()

        self.tray_restore_action = QtWidgets.QAction("Open Settings")
        self.tray_menu.addAction(self.tray_restore_action)
        self.tray_restore_action.triggered.connect(self.restore_window)
        self.tray_quit_action = QtWidgets.QAction("Quit")
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
        self.change_timer_state()
        self.br_settings_wt.setEnabled(i_details_enabled)
        self.sys_tray.breathing_enabled_qaction.setEnabled(i_details_enabled)

        self.update_gui(mc.mc_global.EventSource.breathing_list_selection_changed)

    def on_rest_action_list_row_changed(self):
        self.update_gui(mc.mc_global.EventSource.rest_list_selection_changed)

    def on_breathing_phrase_changed(self, i_details_enabled):
        self.change_timer_state()
        self.br_settings_wt.setEnabled(i_details_enabled)
        self.sys_tray.breathing_enabled_qaction.setEnabled(i_details_enabled)

        self.update_gui(mc.mc_global.EventSource.breathing_list_phrase_updated)

    def on_rest_settings_changed(self):
        settings = mc.model.SettingsM.get()
        if settings.rest_reminder_active_bool:
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
        mc.mc_global.rest_reminder_minutes_passed_int += 1
        if (mc.mc_global.rest_reminder_minutes_passed_int
                >= mc.model.SettingsM.get().rest_reminder_interval_int):
            self.show_rest_reminder()
        self.rest_settings_wt.rest_reminder_qsr.setValue(
            mc.mc_global.rest_reminder_minutes_passed_int
        )

    def on_rest_widget_closed(self):
        mc.mc_global.rest_reminder_minutes_passed_int = 0
        self.update_gui()

    def restore_window(self):
        self.raise_()
        self.showNormal()
        # another alternative (from an SO answer): self.setWindowState(QtCore.Qt.WindowActive)

    def show_rest_reminder(self):
        # self.restore_window()
        # self.main_area_stacked_widget_l4.setCurrentIndex(self.rrcw_sw_id_int)
        # self.rest_actions_dock.raise_()
        self.rest_reminder_dialog = mc.gui.rest_reminder_popup.RestReminderDlg()
        self.rest_reminder_dialog.rest_signal.connect(self.on_rest_rest)
        self.rest_reminder_dialog.skip_signal.connect(self.on_rest_skip)
        self.rest_reminder_dialog.wait_signal.connect(self.on_rest_wait)
        self.update_gui(mc.mc_global.EventSource.rest_opened)

    def on_rest_wait(self):
        mc.mc_global.rest_reminder_minutes_passed_int -= 2  # TODO
        self.update_gui()

    def on_rest_rest(self):
        self.rest_widget = mc.gui.rest_dlg.RestDlg()
        self.rest_widget.closed_signal.connect(self.on_rest_widget_closed)

    def on_rest_skip(self):
        mc.mc_global.rest_reminder_minutes_passed_int = 0
        self.update_gui()

    def on_breathing_settings_changed(self):
        self.change_timer_state()
        self.update_gui(mc.mc_global.EventSource.breathing_settings_changed)

    def change_timer_state(self):
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
        self.breathing_qtimer.timeout.connect(self.show_breathing_dialog_if_conditions)
        # -show_breathing_notification
        self.breathing_qtimer.start(settings.breathing_reminder_interval_int * 60 * 1000)

    def update_menu(self):
        self.menu_bar.clear()

        file_menu = self.menu_bar.addMenu("&File")
        export_action = QtWidgets.QAction("Export data", self)
        file_menu.addAction(export_action)
        export_action.triggered.connect(mc.model.export_all)
        minimize_to_tray_action = QtWidgets.QAction("Minimize to tray", self)
        file_menu.addAction(minimize_to_tray_action)
        minimize_to_tray_action.triggered.connect(self.minimize_to_tray)
        quit_action = QtWidgets.QAction("Quit", self)
        file_menu.addAction(quit_action)
        quit_action.triggered.connect(self.exit_application)

        debug_menu = self.menu_bar.addMenu("&Debug")
        update_gui_action = QtWidgets.QAction("Update GUI", self)
        debug_menu.addAction(update_gui_action)
        update_gui_action.triggered.connect(self.update_gui)
        clear_phrase_selection_action = QtWidgets.QAction("Clear Breathing Phrase", self)
        debug_menu.addAction(clear_phrase_selection_action)
        clear_phrase_selection_action.triggered.connect(self.debug_clear_breathing_phrase_selection)
        breathing_full_screen_action = QtWidgets.QAction("Breathing widget full screen", self)
        debug_menu.addAction(breathing_full_screen_action)
        breathing_full_screen_action.triggered.connect(self.showFullScreen)
        show_exp_notification_action = QtWidgets.QAction("Show breathing dialog", self)
        debug_menu.addAction(show_exp_notification_action)
        show_exp_notification_action.triggered.connect(self.show_breathing_dialog)

        help_menu = self.menu_bar.addMenu("&Help")
        about_action = QtWidgets.QAction("About", self)
        help_menu.addAction(about_action)
        about_action.triggered.connect(self.show_about_box)
        online_help_action = QtWidgets.QAction("Online help", self)
        help_menu.addAction(online_help_action)
        online_help_action.triggered.connect(self.show_online_help)

    def show_breathing_dialog_if_conditions(self):
        if not self.isActiveWindow() and mc.model.breathing_reminder_active():
            self.show_breathing_dialog()

    # noinspection PyAttributeOutsideInit
    def show_breathing_dialog(self):
        notification_type_int = mc.model.SettingsM.get().breathing_reminder_notification_type_int

        if (notification_type_int == mc.mc_global.BreathingNotificationType.Both.value
        or notification_type_int == mc.mc_global.BreathingNotificationType.Visual.value):
            self.breathing_dialog = mc.gui.breathing_popup.BreathingDlg()
            self.breathing_dialog.close_signal.connect(self.on_breathing_dialog_closed)
            self.breathing_dialog.phrase_changed_signal.connect(self.on_breathing_dialog_phrase_changed)
            self.breathing_dialog.show()

        if (notification_type_int == mc.mc_global.BreathingNotificationType.Both.value
        or notification_type_int == mc.mc_global.BreathingNotificationType.Audio.value):
            self.play_audio()  # "390200__ganapataye__03-bells[cc0].wav"

    def play_audio(self) -> None:
        settings = mc.model.SettingsM.get()
        audio_path_str = settings.breathing_reminder_audio_path_str

        volume_int = settings.breathing_reminder_volume_int

        sound_effect = QtMultimedia.QSoundEffect(self)
        # -PLEASE NOTE: A parent has to be given here, otherwise we will not hear anything
        sound_effect.setSource(QtCore.QUrl.fromLocalFile(audio_path_str))
        sound_effect.setVolume(float(volume_int / 100))
        sound_effect.play()

    def on_breathing_dialog_closed(self, i_ib_list, i_ob_list):
        self.breathing_history_wt.add_from_dialog(i_ib_list, i_ob_list)

    def on_breathing_dialog_phrase_changed(self):
        self.update_gui()

    def debug_clear_breathing_phrase_selection(self):
        self.br_phrase_list_wt.list_widget.clearSelection()

    def show_online_help(self):
        url_str = "https://sunyatazero.github.io/mindfulness-at-the-computer/user-guide.html"
        # noinspection PyCallByClass
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url_str))
        # Python: webbrowser.get(url_str) --- doesn't work

    def show_about_box(self):
        # noinspection PyCallByClass
        QtWidgets.QMessageBox.about(
            self,
            "About Mindfulness at the Computer",
            (
                '<html>'
                'Concept and programming by Tord Dellsén'
                '<a href="https://sunyatazero.github.io/"> Github website</a><br>'
                '<a href="https://github.com/SunyataZero/mindfulness-at-the-computer/graphs/contributors">'
                'All contributors</a><br>'
                'Photography for application icon by Torgny Dellsén '
                '<a href="http://torgnydellsen.zenfolio.com">torgnydellsen.zenfolio.com</a><br>'
                'Other icons from Open Iconic - useiconic.com<br>'
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

        if i_event_source != mc.mc_global.EventSource.rest_slider_value_changed:
            self.rest_settings_wt.update_gui()
        self.br_settings_wt.update_gui()

        if (i_event_source != mc.mc_global.EventSource.breathing_list_selection_changed
        and i_event_source != mc.mc_global.EventSource.rest_list_selection_changed):
            self.br_phrase_list_wt.update_gui()
            self.rest_action_list_wt.update_gui()

        self.update_systray()

    def update_systray(self):
        if self.tray_icon is None:
            return
        settings = mc.model.SettingsM.get()

        # Icon
        self.tray_icon.setIcon(QtGui.QIcon(mc.model.get_app_systray_icon_path()))
        # self.tray_icon.show()

        # Menu
        self.sys_tray.update_breathing_checked(settings.breathing_reminder_active_bool)
        self.sys_tray.update_rest_checked(settings.rest_reminder_active_bool)
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
