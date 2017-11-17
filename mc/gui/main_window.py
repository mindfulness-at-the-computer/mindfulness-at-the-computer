import logging
import sys
import functools
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import mc.gui.rest_action_list_dock
import mc.model
import mc.mc_global
import mc.gui.breathing_widget
import mc.gui.breathing_reminder_settings_dock
import mc.gui.breathing_phrase_list_dock
import mc.gui.rest_reminder_settings_dock
import mc.gui.rest_widget
import mc.gui.breathing_dialog


class MbMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 900, 600)
        self.setCorner(QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomRightCorner, QtCore.Qt.RightDockWidgetArea)
        self.setWindowIcon(QtGui.QIcon(mc.mc_global.get_app_icon_path()))

        self.system_tray = SystemTray()

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
        self.tray_icon = None
        self.rest_reminder_qtimer = None
        self.breathing_qtimer = None

        central_widget_l2 = QtWidgets.QWidget()
        self.setCentralWidget(central_widget_l2)
        vbox_l3 = QtWidgets.QVBoxLayout()
        central_widget_l2.setLayout(vbox_l3)

        self.main_area_stacked_widget_l4 = QtWidgets.QStackedWidget()
        vbox_l3.addWidget(self.main_area_stacked_widget_l4)

        self.breathing_widget = mc.gui.breathing_widget.BreathingCompositeWidget()
        self.bcw_sw_id_int = self.main_area_stacked_widget_l4.addWidget(self.breathing_widget)

        self.rest_widget = mc.gui.rest_widget.RestComposite()
        self.rrcw_sw_id_int = self.main_area_stacked_widget_l4.addWidget(self.rest_widget)
        self.rest_widget.result_signal.connect(self.on_rest_widget_closed)

        self.main_area_stacked_widget_l4.setCurrentIndex(self.bcw_sw_id_int)

        self.breathing_phrase_dock = QtWidgets.QDockWidget("Breathing Phrases")
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.breathing_phrase_dock)
        self.breathing_phrase_dock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.phrase_list_widget = mc.gui.breathing_phrase_list_dock.PhraseListCompositeWidget()
        self.breathing_phrase_dock.setWidget(self.phrase_list_widget)
        self.breathing_phrase_dock.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        self.phrase_list_widget.list_selection_changed_signal.connect(self.on_breathing_list_row_changed)
        self.phrase_list_widget.phrase_updated_signal.connect(self.on_breathing_phrase_changed)

        self.breathing_settings_dock = QtWidgets.QDockWidget("Breathing Reminders")
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.breathing_settings_dock)
        # settings_dock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.breathing_settings_dw = mc.gui.breathing_reminder_settings_dock.BreathingSettingsComposite()
        self.breathing_settings_dock.setWidget(self.breathing_settings_dw)
        self.breathing_settings_dw.breathing_settings_updated_signal.connect(self.on_breathing_settings_changed)
        self.breathing_settings_dw.breathing_test_button_clicked_signal.connect(self.show_breathing_dialog)
        self.breathing_settings_dock.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

        self.rest_settings_dock = QtWidgets.QDockWidget("Rest Reminders")
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.rest_settings_dock)
        # settings_dock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.rest_settings_dw = mc.gui.rest_reminder_settings_dock.RestSettingsComposite()
        self.rest_settings_dock.setWidget(self.rest_settings_dw)
        self.rest_settings_dw.rest_settings_updated_signal.connect(self.on_rest_settings_changed)
        self.rest_settings_dw.rest_test_button_clicked_signal.connect(self.show_rest_reminder)
        self.rest_settings_dw.rest_reset_button_clicked_signal.connect(self.on_rest_settings_changed)
        self.rest_settings_dw.rest_slider_value_changed_signal.connect(self.on_rest_slider_value_changed)
        self.rest_settings_dock.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

        self.rest_actions_dock = QtWidgets.QDockWidget("Rest Actions")
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.rest_actions_dock)
        self.rest_actions_dock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.tabifyDockWidget(self.breathing_phrase_dock, self.rest_actions_dock)  # <------
        self.rest_actions_widget = mc.gui.rest_action_list_dock.RestActionsComposite()
        self.rest_actions_dock.setWidget(self.rest_actions_widget)
        self.rest_actions_widget.update_signal.connect(self.on_rest_actions_updated)
        self.rest_actions_widget.list_selection_changed_signal.connect(self.on_rest_action_list_row_changed)
        self.rest_actions_dock.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)

        self.breathing_phrase_dock.raise_()

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
        sysinfo = QtCore.QSysInfo()
        logging.info("buildCpuArchitecture: " + sysinfo.buildCpuArchitecture())
        logging.info("currentCpuArchitecture: " + sysinfo.currentCpuArchitecture())
        logging.info("kernel type and version: " + sysinfo.kernelType() + " " + sysinfo.kernelVersion())
        logging.info("product name and version: " + sysinfo.prettyProductName())
        logging.info("#####")

        settings = mc.model.SettingsM.get()

        self.tray_menu = QtWidgets.QMenu(self)

        self.system_tray.tray_rest_enabled_qaction = QtWidgets.QAction("Enable Rest Reminder")
        self.tray_menu.addAction(self.system_tray.tray_rest_enabled_qaction)
        self.system_tray.tray_rest_enabled_qaction.setCheckable(True)
        self.system_tray.tray_rest_enabled_qaction.toggled.connect(
            self.rest_settings_dw.on_switch_toggled
        )
        self.system_tray.tray_rest_enabled_qaction.setChecked(settings.rest_reminder_active_bool)
        self.system_tray.tray_rest_progress_qaction = QtWidgets.QAction("")
        self.tray_menu.addAction(self.system_tray.tray_rest_progress_qaction)
        self.system_tray.tray_rest_progress_qaction.setDisabled(True)
        self.system_tray.update_tray_rest_progress_bar(0, 1)
        self.tray_rest_now_qaction = QtWidgets.QAction("Take a Break Now")
        self.tray_menu.addAction(self.tray_rest_now_qaction)
        self.tray_rest_now_qaction.triggered.connect(self.show_rest_reminder)

        self.tray_menu.addSeparator()

        self.system_tray.tray_breathing_enabled_qaction = QtWidgets.QAction("Enable Breathing Reminder")
        self.tray_menu.addAction(self.system_tray.tray_breathing_enabled_qaction)
        self.system_tray.tray_breathing_enabled_qaction.setCheckable(True)
        self.system_tray.tray_breathing_enabled_qaction.setChecked(settings.breathing_reminder_active_bool)
        self.system_tray.tray_breathing_enabled_qaction.toggled.connect(
            self.breathing_settings_dw.on_switch_toggled
        )
        self.system_tray.tray_breathing_enabled_qaction.setDisabled(True)

        self.system_tray.tray_phrase_qaction_list.clear()
        for count in enumerate(range(5)):
            for l_phrase in mc.model.PhrasesM.get_all():
                INDENTATION_STR = "  "
                ACTIVE_MARKER_STR = "•"
                INACTIVE_MARKER_STR = " "
                active_or_inactive_str = INACTIVE_MARKER_STR
                if l_phrase.id_int == mc.mc_global.active_phrase_id_it:
                    active_or_inactive_str = ACTIVE_MARKER_STR
                tray_phrase_qaction = QtWidgets.QAction(active_or_inactive_str + INDENTATION_STR + l_phrase.title_str)
                tray_phrase_qaction.triggered.connect(
                    functools.partial(
                        self.phrase_list_widget.on_new_row_selected_from_system_tray,
                        l_phrase.id_int
                    )
                )
                self.system_tray.tray_phrase_qaction_list.append(tray_phrase_qaction)
                # self.tray_phrase_qaction = QtWidgets.QAction(l_phrase.title_str)
                self.tray_menu.addAction(tray_phrase_qaction)

        self.tray_menu.addSeparator()

        self.tray_restore_action = QtWidgets.QAction("Restore")
        self.tray_menu.addAction(self.tray_restore_action)
        self.tray_restore_action.triggered.connect(self.restore_window)
        self.tray_quit_action = QtWidgets.QAction("Quit")
        self.tray_menu.addAction(self.tray_quit_action)
        self.tray_quit_action.triggered.connect(self.exit_application)

        self.tray_icon.setContextMenu(self.tray_menu)

    def on_rest_actions_updated(self):
        self.update_gui(mc.mc_global.EventSource.rest_action_changed)

    def on_systray_activated(self, i_reason):
        logging.debug("entered on_systray_activated. i_reason = " + str(i_reason))
        self.restore_window()

    def on_breathing_list_row_changed(self, i_details_enabled: bool):
        self.change_timer_state()
        self.breathing_settings_dw.setEnabled(i_details_enabled)
        self.system_tray.tray_breathing_enabled_qaction.setEnabled(i_details_enabled)

        self.update_gui(mc.mc_global.EventSource.breathing_list_selection_changed)

    def on_rest_action_list_row_changed(self):
        self.update_gui(mc.mc_global.EventSource.rest_list_selection_changed)

    def on_breathing_phrase_changed(self, i_details_enabled):
        self.change_timer_state()
        self.breathing_settings_dw.setEnabled(i_details_enabled)
        self.system_tray.tray_breathing_enabled_qaction.setEnabled(i_details_enabled)

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
        self.rest_settings_dw.update_gui()  # -so that the progressbar is updated

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
        self.rest_settings_dw.rest_reminder_qsr.setValue(
            mc.mc_global.rest_reminder_minutes_passed_int
        )

    def on_rest_widget_closed(self, i_wait_minutes: int):
        if i_wait_minutes >= 0:  # mc.gui.rest_widget.CLOSED_RESULT_INT
            mc.mc_global.rest_reminder_minutes_passed_int = (
                mc.model.SettingsM.get().rest_reminder_interval_int
                - i_wait_minutes
            )
            self.minimize_to_tray()
        else:
            mc.mc_global.rest_reminder_minutes_passed_int = 0
            if i_wait_minutes == mc.gui.rest_widget.CLOSED_RESULT_INT:
                settings = mc.model.SettingsM.get()
                settings.update_rest_reminder_active(False)
                self.minimize_to_tray()

        self.main_area_stacked_widget_l4.setCurrentIndex(self.bcw_sw_id_int)
        if i_wait_minutes == mc.gui.rest_widget.CLOSED_WITH_BREATHING_RESULT_INT:
            self.breathing_widget.on_start_pause_clicked()
        self.breathing_phrase_dock.raise_()
        # -this may not work, info here:
        # http://www.qtcentre.org/threads/21362-Setting-the-active-tab-with-tabified-docking-windows
        self.update_gui(mc.mc_global.EventSource.rest_closed)

    def restore_window(self):
        self.raise_()
        self.showNormal()
        # another alternative (from an SO answer): self.setWindowState(QtCore.Qt.WindowActive)

    def show_rest_reminder(self):
        self.restore_window()
        self.main_area_stacked_widget_l4.setCurrentIndex(self.rrcw_sw_id_int)
        self.rest_actions_dock.raise_()
        self.update_gui(mc.mc_global.EventSource.rest_opened)

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
        self.breathing_qtimer.timeout.connect(self.show_breathing_dialog)
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
        show_exp_notification_action.triggered.connect(self.show_exp_notification)

        window_menu = self.menu_bar.addMenu("&Windows")
        show_breathing_settings_window_action = self.breathing_settings_dock.toggleViewAction()
        window_menu.addAction(show_breathing_settings_window_action)
        show_rest_settings_window_action = self.rest_settings_dock.toggleViewAction()
        window_menu.addAction(show_rest_settings_window_action)
        # show_quotes_window_action = self.quotes_dock.toggleViewAction()
        # window_menu.addAction(show_quotes_window_action)
        show_rest_actions_window_action = self.rest_actions_dock.toggleViewAction()
        window_menu.addAction(show_rest_actions_window_action)

        help_menu = self.menu_bar.addMenu("&Help")
        about_action = QtWidgets.QAction("About", self)
        help_menu.addAction(about_action)
        about_action.triggered.connect(self.show_about_box)
        online_help_action = QtWidgets.QAction("Online help", self)
        help_menu.addAction(online_help_action)
        online_help_action.triggered.connect(self.show_online_help)

    def show_breathing_dialog(self):
        if not self.isActiveWindow() and mc.model.breathing_reminder_active():
            self.show_exp_notification()

    # noinspection PyAttributeOutsideInit
    def show_exp_notification(self):
        logging.debug("show_exp_notification")
        self.exp_notification = mc.gui.breathing_dialog.ExpNotificationWidget()
        self.exp_notification.close_signal.connect(
            self.on_breathing_dialog_closed)
        self.exp_notification.show()

    def on_breathing_dialog_closed(self, i_ib_list, i_ob_list):
        self.breathing_widget.add_from_dialog(i_ib_list, i_ob_list)

    def debug_clear_breathing_phrase_selection(self):
        self.phrase_list_widget.list_widget.clearSelection()

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
        self.breathing_widget.update_gui()
        self.rest_widget.update_gui()

        if i_event_source != mc.mc_global.EventSource.rest_slider_value_changed:
            self.rest_settings_dw.update_gui()
        self.breathing_settings_dw.update_gui()

        if (i_event_source != mc.mc_global.EventSource.breathing_list_selection_changed
        and i_event_source != mc.mc_global.EventSource.rest_list_selection_changed):
            self.phrase_list_widget.update_gui()
            self.rest_actions_widget.update_gui()

        self.update_systray()

    def update_systray(self):
        if self.tray_icon is None:
            return
        settings = mc.model.SettingsM.get()

        # Icon
        self.tray_icon.setIcon(QtGui.QIcon(mc.model.get_app_systray_icon_path()))
        # self.tray_icon.show()

        # Menu
        self.system_tray.update_tray_breathing_checked(settings.breathing_reminder_active_bool)
        self.system_tray.update_tray_rest_checked(settings.rest_reminder_active_bool)
        self.system_tray.update_tray_rest_progress_bar(
            mc.mc_global.rest_reminder_minutes_passed_int,
            mc.model.SettingsM.get().rest_reminder_interval_int
        )


class SystemTray:
    def __init__(self):
        self.tray_rest_progress_qaction = None
        self.tray_rest_enabled_qaction = None
        self.tray_breathing_enabled_qaction = None
        self.tray_phrase_qaction_list = []

    def update_tray_rest_progress_bar(self, time_passed_int, interval_minutes_int):
        if self.tray_rest_progress_qaction is None:
            return
        time_passed_str = ""
        parts_of_ten_int = (10 * time_passed_int) // interval_minutes_int
        for i in range(0, 9):
            if i < parts_of_ten_int:
                time_passed_str += "◾"
            else:
                time_passed_str += "◽"
        self.tray_rest_progress_qaction.setText(time_passed_str)

    def update_tray_rest_checked(self, i_active: bool):
        if self.tray_rest_enabled_qaction is not None:
            self.tray_rest_enabled_qaction.setChecked(i_active)

    def update_tray_breathing_checked(self, i_checked: bool):
        if self.tray_breathing_enabled_qaction is not None:
            self.tray_breathing_enabled_qaction.setChecked(i_checked)

    def update_tray_breathing_enabled(self, i_enabled: bool):
        if self.tray_breathing_enabled_qaction is not None:
            self.tray_breathing_enabled_qaction.setEnabled(i_enabled)
