import logging
import sys
import webbrowser
import functools

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtTest
from PyQt5 import QtWidgets

import mc.gui.rest_action_list_dock
from mc import model, mc_global
import mc.gui.breathing_widget
import mc.gui.breathing_reminder_settings_dock
import mc.gui.breathing_phrase_list_dock
import mc.gui.rest_reminder_settings_dock
import mc.gui.rest_widget


class MbMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 900, 600)
        self.setCorner(QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomRightCorner, QtCore.Qt.RightDockWidgetArea)
        self.setWindowIcon(QtGui.QIcon(mc_global.get_app_icon_path()))

        if mc_global.testing_bool:
            data_storage_str = "{Testing - data stored in memory}"
        else:
            data_storage_str = "{Live - data stored on hard drive}"
        window_title_str = (
            mc_global.APPLICATION_TITLE_STR
            + " [" + mc_global.APPLICATION_VERSION_STR + "] "
            + data_storage_str
        )
        self.setWindowTitle(window_title_str)

        self.setStyleSheet("selection-background-color:#bfef7f; selection-color:#000000;")  # -#91c856
        # QProgressBar{background-color:#333333;}

        self.rest_reminder_dialog = None
        self.tray_icon = None
        self.rest_reminder_qtimer = None
        self.breathing_qtimer = None

        vbox_widget = QtWidgets.QWidget()
        self.setCentralWidget(vbox_widget)
        vbox = QtWidgets.QVBoxLayout()
        vbox_widget.setLayout(vbox)


        self.main_area_stacked_widget = QtWidgets.QStackedWidget()
        vbox.addWidget(self.main_area_stacked_widget)

        self.breathing_composite_widget = mc.gui.breathing_widget.BreathingCompositeWidget()
        self.bcw_sw_id_int = self.main_area_stacked_widget.addWidget(self.breathing_composite_widget)

        self.rest_reminder_composite = mc.gui.rest_widget.RestReminderComposite()
        self.rrcw_sw_id_int = self.main_area_stacked_widget.addWidget(self.rest_reminder_composite)
        self.rest_reminder_composite.result_signal.connect(self.on_rest_reminder_widget_closed)

        self.main_area_stacked_widget.setCurrentIndex(self.bcw_sw_id_int)


        self.phrase_list_dock = QtWidgets.QDockWidget("List of Phrases")
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.phrase_list_dock)
        self.phrase_list_dock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.phrase_list_widget = mc.gui.breathing_phrase_list_dock.PhraseListCompositeWidget()
        self.phrase_list_dock.setWidget(self.phrase_list_widget)
        self.phrase_list_widget.phrases_updated_signal.connect(self.phrase_row_changed)

        self.breathing_settings_dock = QtWidgets.QDockWidget("Breathing Reminders")
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.breathing_settings_dock)
        # settings_dock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.breathing_settings_widget = mc.gui.breathing_reminder_settings_dock.BreathingSettingsComposite()
        self.breathing_settings_dock.setWidget(self.breathing_settings_widget)
        self.breathing_settings_widget.breathing_settings_updated_signal.connect(self.update_breathing_timer)
        self.breathing_settings_widget.breathing_test_button_clicked_signal.connect(self.show_breathing_notification)

        self.rest_settings_dock = QtWidgets.QDockWidget("Rest Reminders")
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.rest_settings_dock)
        # settings_dock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.rest_settings_widget = mc.gui.rest_reminder_settings_dock.RestSettingsComposite()
        self.rest_settings_dock.setWidget(self.rest_settings_widget)
        self.rest_settings_widget.rest_settings_updated_signal.connect(self.update_rest_timer)
        self.rest_settings_widget.rest_test_button_clicked_signal.connect(self.show_rest_reminder)
        self.rest_settings_widget.rest_reset_button_clicked_signal.connect(self.update_rest_timer)

        self.rest_actions_dock = QtWidgets.QDockWidget("Rest Actions")
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.rest_actions_dock)
        self.rest_actions_dock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.tabifyDockWidget(self.phrase_list_dock, self.rest_actions_dock)  # <------
        self.rest_actions_widget = mc.gui.rest_action_list_dock.RestActionsComposite()
        self.rest_actions_dock.setWidget(self.rest_actions_widget)
        self.rest_actions_widget.update_signal.connect(self.on_rest_actions_updated)
        size_policy = self.rest_actions_dock.sizePolicy()
        size_policy.setVerticalPolicy(QtWidgets.QSizePolicy.Maximum)
        self.rest_actions_dock.setSizePolicy(size_policy)

        """
        self.quotes_dock = QtWidgets.QDockWidget("Quotes")
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.quotes_dock)
        self.quotes_widget = quotes.CompositeQuotesWidget()
        self.quotes_dock.setWidget(self.quotes_widget)
        self.quotes_dock.hide()  # -hiding at the start
        """

        # Menu
        self.menu_bar = self.menuBar()
        self.update_menu()

        # Timers
        self.update_breathing_timer()
        self.update_rest_timer()

        # System tray
        # Please note: We cannot move the update code into another function, even here in
        # this file (very strange), if we do we won't see the texts, only the separators,
        # unknown why but it may be because of a bug
        self.tray_icon = QtWidgets.QSystemTrayIcon(
            QtGui.QIcon(mc_global.get_app_systray_icon_path()),
            self
        )
        logging.debug("connecting with the activated signal")
        self.tray_icon.activated.connect(self.on_systray_activated)
        self.tray_icon.show()
        # self.update_tray_menu()
        if not self.tray_icon.supportsMessages():
            logging.warning("Your system doesn't support notifications. If you are using MacOS please install growl")

        settings = mc.model.SettingsM.get()

        self.tray_menu = QtWidgets.QMenu(self)

        mc_global.tray_rest_enabled_qaction = QtWidgets.QAction("Enable Rest Reminder")
        self.tray_menu.addAction(mc_global.tray_rest_enabled_qaction)
        mc_global.tray_rest_enabled_qaction.setCheckable(True)
        mc_global.tray_rest_enabled_qaction.toggled.connect(
            self.rest_settings_widget.on_switch_toggled
        )
        mc_global.tray_rest_enabled_qaction.setChecked(settings.rest_reminder_active_bool)
        mc_global.tray_rest_progress_qaction = QtWidgets.QAction("")
        self.tray_menu.addAction(mc_global.tray_rest_progress_qaction)
        mc_global.tray_rest_progress_qaction.setDisabled(True)
        mc_global.update_tray_rest_progress_bar(0, 1)
        self.tray_rest_now_qaction = QtWidgets.QAction("Take a Break Now")
        self.tray_menu.addAction(self.tray_rest_now_qaction)
        self.tray_rest_now_qaction.triggered.connect(self.show_rest_reminder)

        self.tray_menu.addSeparator()

        mc_global.tray_breathing_enabled_qaction = QtWidgets.QAction("Enable Breathing Reminder")
        self.tray_menu.addAction(mc_global.tray_breathing_enabled_qaction)
        mc_global.tray_breathing_enabled_qaction.setCheckable(True)
        mc_global.tray_breathing_enabled_qaction.setChecked(settings.breathing_reminder_active_bool)
        mc_global.tray_breathing_enabled_qaction.toggled.connect(
            self.breathing_settings_widget.on_switch_toggled
        )
        mc_global.tray_breathing_enabled_qaction.setDisabled(True)

        count_int = 0
        mc_global.tray_phrase_qaction_list.clear()
        for l_phrase in mc.model.PhrasesM.get_all():
            INDENTATION_STR = "  "
            ACTIVE_MARKER_STR = "•"
            INACTIVE_MARKER_STR = " "
            active_or_inactive_str = INACTIVE_MARKER_STR
            if l_phrase.id_int == mc_global.active_phrase_id_it:
                active_or_inactive_str = ACTIVE_MARKER_STR
            tray_phrase_qaction = QtWidgets.QAction(active_or_inactive_str + INDENTATION_STR + l_phrase.title_str)
            tray_phrase_qaction.triggered.connect(
                functools.partial(
                    self.phrase_list_widget.on_new_row_selected_from_system_tray,
                    l_phrase.id_int
                )
            )
            mc_global.tray_phrase_qaction_list.append(tray_phrase_qaction)
            # self.tray_phrase_qaction = QtWidgets.QAction(l_phrase.title_str)
            self.tray_menu.addAction(tray_phrase_qaction)
            count_int += 1
            if count_int >= 5:
                break

        self.tray_menu.addSeparator()

        self.tray_restore_action = QtWidgets.QAction("Restore")
        self.tray_menu.addAction(self.tray_restore_action)
        self.tray_restore_action.triggered.connect(self.showNormal)
        self.tray_quit_action = QtWidgets.QAction("Quit")
        self.tray_menu.addAction(self.tray_quit_action)
        self.tray_quit_action.triggered.connect(self.exit_application)

        self.tray_icon.setContextMenu(self.tray_menu)

    def on_rest_actions_updated(self):
        self.rest_reminder_composite.update_gui()

    def on_systray_activated(self):
        logging.debug("entered on_systray_activated")

    def phrase_row_changed(self, i_details_enabled: bool):
        self.update_breathing_timer()
        self.update_gui()
        self.breathing_settings_widget.setEnabled(i_details_enabled)
        mc_global.tray_breathing_enabled_qaction.setEnabled(i_details_enabled)

    def update_rest_timer(self):
        settings = model.SettingsM.get()
        if settings.rest_reminder_active_bool:
            self.start_rest_timer()
        else:
            self.stop_rest_timer()
        self.update_gui()

    def stop_rest_timer(self):
        if self.rest_reminder_qtimer is not None and self.rest_reminder_qtimer.isActive():
            self.rest_reminder_qtimer.stop()
        self.rest_settings_widget.update_gui()  # -so that the progressbar is updated

    def start_rest_timer(self):
        mc_global.rest_reminder_minutes_passed_int = 0
        self.stop_rest_timer()
        self.rest_reminder_qtimer = QtCore.QTimer(self)
        self.rest_reminder_qtimer.timeout.connect(self.rest_timer_timeout)
        self.rest_reminder_qtimer.start(60 * 1000)  # -one minute

    def rest_timer_timeout(self):
        mc_global.rest_reminder_minutes_passed_int += 1
        if (mc_global.rest_reminder_minutes_passed_int
                >= model.SettingsM.get().rest_reminder_interval_int):
            self.show_rest_reminder()
        # self.rest_settings_widget.updating_gui_bool = True
        self.rest_settings_widget.rest_reminder_qsr.setValue(
            mc_global.rest_reminder_minutes_passed_int
        )
        # self.rest_settings_widget.updating_gui_bool = False
        # self.update_tray_menu(1, 1)

    def on_rest_reminder_widget_closed(self, i_wait_minutes: int):
        if i_wait_minutes != mc.gui.rest_reminder_cwidget.CLOSED_RESULT_INT:
            if i_wait_minutes != unused_rest_reminder_dlg.CLOSED_RESULT_INT:
                mc_global.rest_reminder_minutes_passed_int = (
                    model.SettingsM.get().rest_reminder_interval_int
                    - i_wait_minutes
                )
        else:
            mc_global.rest_reminder_minutes_passed_int = 0

        self.main_area_stacked_widget.setCurrentIndex(self.bcw_sw_id_int)
        self.update_gui()

    def show_rest_reminder(self):
        #mc_global.rest_reminder_minutes_passed_int = 0
        self.main_area_stacked_widget.setCurrentIndex(self.rrcw_sw_id_int)
        self.update_gui()
        # self.showNormal()
        # self.raise_()
        self.showNormal()
        # self.raise_()
        self.setWindowState(QtCore.Qt.WindowActive)
        # -TODO: Do we want to use this for the systray as well so we are more consistent?
        #  or else

        # self.activateWindow()

    def update_breathing_timer(self):
        settings = model.SettingsM.get()
        if settings.breathing_reminder_active_bool:
            self.start_breathing_timer()
        else:
            self.stop_breathing_timer()
        self.update_gui()

    def stop_breathing_timer(self):
        if self.breathing_qtimer is not None and self.breathing_qtimer.isActive():
            self.breathing_qtimer.stop()

    def start_breathing_timer(self):
        self.stop_breathing_timer()
        settings = model.SettingsM.get()
        self.breathing_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.breathing_qtimer.timeout.connect(self.show_breathing_notification)
        self.breathing_qtimer.start(settings.breathing_reminder_interval_int * 1000)

    def show_breathing_notification(self):
        if mc_global.breathing_state != mc_global.BreathingState.inactive \
                or mc_global.active_phrase_id_it == -1:
            return  # -TODO: Alternatively we can stop and start timers when the state changes
        settings = model.SettingsM.get()
        # TODO: assert mc_global.active_phrase_id_it != mc_global.NO_PHRASE_SELECTED_INT
        active_phrase = model.PhrasesM.get(mc_global.active_phrase_id_it)
        reminder_str = active_phrase.ib_str + "\n" + active_phrase.ob_str
        self.tray_icon.showMessage(
            "Mindful breathing",
            reminder_str.strip(),
            icon=QtWidgets.QSystemTrayIcon.NoIcon,
            msecs=settings.breathing_reminder_length_int * 1000
        )
        # TODO: The title (now "application title string") and the icon
        # could be used to show if the message is a mindfulness of breathing message

    def update_menu(self):
        self.menu_bar.clear()

        file_menu = self.menu_bar.addMenu("&File")
        export_action = QtWidgets.QAction("Export data", self)
        file_menu.addAction(export_action)
        export_action.triggered.connect(model.export_all)
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
        clear_rest_selection_action = QtWidgets.QAction("Clear Rest Action", self)
        debug_menu.addAction(clear_rest_selection_action)
        clear_rest_selection_action.triggered.connect(self.debug_clear_rest_action_selection)
        clear_phrase_selection_action = QtWidgets.QAction("Clear Breathing Phrase", self)
        debug_menu.addAction(clear_phrase_selection_action)
        clear_phrase_selection_action.triggered.connect(self.debug_clear_breathing_phrase_selection)
        breathing_fullscreen_action = QtWidgets.QAction("Breathing widget fullscreen", self)
        debug_menu.addAction(breathing_fullscreen_action)
        breathing_fullscreen_action.triggered.connect(self.showFullScreen)
        # -"Calling this function only affects windows"
        # -showNormal

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

    def debug_clear_rest_action_selection(self):
        self.rest_actions_qlw.clearSelection()

    def debug_clear_breathing_phrase_selection(self):
        self.phrase_list_widget.list_widget.clearSelection()

    def show_online_help(self):
        url_str = "https://sunyatazero.github.io/mindfulness-at-the-computer/user-guide.html"
        # Python: webbrowser.get(url_str) --- doesn't work
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url_str))

    def show_about_box(self):
        message_box = QtWidgets.QMessageBox.about(
            self,
            "About Mindfulness at the Computer",
            (
                '<html>Concept and programming by Tord Dellsén<br>'
                'Photography for application icon by Torgny Dellsén <a href="http://torgnydellsen.zenfolio.com">torgnydellsen.zenfolio.com</a><br>'
                'Other icons from Open Iconic - useiconic.com<br>'
                'Other images (for the rest actions) have been released into the public domain (CC0)<br>'
                'Audio files have been released into the public domain (CC0)<br>'
                'Software License: GPLv3</html>'
            )
        )

        # "Photo license: CC BY-SA 4.0"

    # overridden
    def closeEvent(self, i_QCloseEvent):
        i_QCloseEvent.ignore()
        self.minimize_to_tray()

    def minimize_to_tray(self):
        self.showMinimized()
        self.hide()

    def exit_application(self):
        """
        self.on_move_back_todo_button_clicked()
        self.save_todo_text_file(self.todo_path_str)  # -auto-save on exit
        self.settings.setValue("GEOMETRY", self.saveGeometry())
        self.settings.sync()  # -this has to be called (at least on Ubuntu), otherwise the settings aren't saved
        """
        sys.exit()

    def update_gui(self):
        self.breathing_composite_widget.update_gui()
        self.rest_settings_widget.update_gui()
        self.breathing_settings_widget.update_gui()

        if self.tray_icon is not None:
            logging.debug(
                "mc_global.get_app_systray_icon_path() = "
                + mc_global.get_app_systray_icon_path()
            )
            self.tray_icon.setIcon(
                QtGui.QIcon(mc_global.get_app_systray_icon_path())
            )
            # -TODO: Do this in another place?
            self.tray_icon.show()


