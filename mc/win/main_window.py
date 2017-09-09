import functools
import sys

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from mc import model, mc_global
from mc.win import breathing
from mc.win import insights
from mc.win import phrase_list
from mc.win import quotes
from mc.win import rest_reminder_dialog
from mc.win import rest_reminder_settings
from mc.win import breathing_reminder_settings


class MbMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.show()
        self.setGeometry(100, 100, 900, 600)
        self.setCorner(QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomRightCorner, QtCore.Qt.RightDockWidgetArea)
        self.setWindowIcon(QtGui.QIcon(mc_global.APPLICATION_ICON_PATH_STR))

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
        ### QProgressBar{background-color:#333333;}

        self.tray_icon = None
        self.rest_reminder_qtimer = None
        self.breathing_qtimer = None

        vbox_widget = QtWidgets.QWidget()
        self.setCentralWidget(vbox_widget)
        vbox = QtWidgets.QVBoxLayout()
        vbox_widget.setLayout(vbox)

        self.breathing_composite_widget = breathing.BreathingCompositeWidget()
        vbox.addWidget(self.breathing_composite_widget)

        self.phrase_list_dock = QtWidgets.QDockWidget("List of Phrases")
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.phrase_list_dock)
        self.phrase_list_dock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.phrase_list_widget = phrase_list.PhraseListCompositeWidget()
        self.phrase_list_dock.setWidget(self.phrase_list_widget)
        self.phrase_list_widget.row_changed_signal.connect(self.phrase_row_changed)

        self.rest_settings_dock = QtWidgets.QDockWidget("Rest reminders")
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.rest_settings_dock)
        # settings_dock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.rest_settings_widget = rest_reminder_settings.RestSettingsComposite()
        self.rest_settings_dock.setWidget(self.rest_settings_widget)
        self.rest_settings_widget.rest_settings_updated_signal.connect(self.on_rest_settings_updated)
        self.rest_settings_widget.rest_test_button_clicked_signal.connect(self.show_rest_reminder)
        self.rest_settings_widget.rest_reset_button_clicked_signal.connect(self.start_rest_reminder_timer)

        self.breathing_settings_dock = QtWidgets.QDockWidget("Breathing reminders")
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.breathing_settings_dock)
        # settings_dock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.breathing_settings_widget = breathing_reminder_settings.BreathingSettingsComposite()
        self.breathing_settings_dock.setWidget(self.breathing_settings_widget)
        self.breathing_settings_widget.breathing_settings_updated_signal.connect(self.on_breathing_settings_updated)
        self.breathing_settings_widget.breathing_test_button_clicked_signal.connect(self.show_breathing_notification)


        self.quotes_dock = QtWidgets.QDockWidget("Quotes")
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.quotes_dock)
        self.quotes_widget = quotes.CompositeQuotesWidget()
        self.quotes_dock.setWidget(self.quotes_widget)
        self.quotes_dock.hide()  # -hiding at the start

        self.insights_dock = QtWidgets.QDockWidget("Insights")
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.insights_dock)
        self.insights_widget = insights.CompositeInsightsWidget()
        self.insights_dock.setWidget(self.insights_widget)
        self.insights_dock.hide()  # -hiding at the start

        # Menu
        self.menu_bar = self.menuBar()
        self.update_menu()

        self.start_breathing_notification_timer()

        self.start_rest_reminder_timer()

    def phrase_row_changed(self):
        self.start_breathing_notification_timer()
        self.update_gui()

    def on_rest_settings_updated(self):
        settings = model.SettingsM.get()
        if settings.rest_reminder_active_bool:
            self.start_rest_reminder_timer()
        else:
            self.stop_rest_reminder_timer()

    def stop_rest_reminder_timer(self):
        if self.rest_reminder_qtimer is not None and self.rest_reminder_qtimer.isActive():
            self.rest_reminder_qtimer.stop()
        self.rest_settings_widget.update_gui()  # -so that the progressbar is updated

    def start_rest_reminder_timer(self):
        mc_global.rest_reminder_minutes_passed_int = 0
        self.stop_rest_reminder_timer()
        self.rest_reminder_qtimer = QtCore.QTimer(self)
        self.rest_reminder_qtimer.timeout.connect(self.rest_reminder_timeout)
        self.rest_reminder_qtimer.start(60 * 1000)  # -one minute

    def rest_reminder_timeout(self):
        mc_global.rest_reminder_minutes_passed_int += 1
        rest_reminder_interval_minutes_int = model.SettingsM.get().rest_reminder_interval_int
        if mc_global.rest_reminder_minutes_passed_int >= rest_reminder_interval_minutes_int:
            self.show_rest_reminder()
        self.rest_settings_widget.rest_reminder_qprb.setValue(
            mc_global.rest_reminder_minutes_passed_int
        )

    def show_rest_reminder(self):
        mc_global.rest_reminder_minutes_passed_int = 0
        rest_reminder_dialog.RestReminderDialog.show_dialog(self)
        # TODO: Do we want to set another icon for the system tray?

    def on_breathing_settings_updated(self):
        settings = model.SettingsM.get()
        if settings.breathing_reminder_active_bool:
            self.start_breathing_notification_timer()
        else:
            self.stop_breathing_notification_timer()

    def stop_breathing_notification_timer(self):
        if self.breathing_qtimer is not None and self.breathing_qtimer.isActive():
            self.breathing_qtimer.stop()

    def start_breathing_notification_timer(self):
        self.stop_breathing_notification_timer()
        settings = model.SettingsM.get()
        self.breathing_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.breathing_qtimer.timeout.connect(self.show_breathing_notification)
        self.breathing_qtimer.start(settings.breathing_reminder_interval_int * 1000)

    def show_breathing_notification(self):
        settings = model.SettingsM.get()
        if mc_global.active_phrase_id_it != mc_global.NO_PHRASE_SELECTED_INT:
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
        # or a message for taking a break (or something else)

    def update_menu(self):
        self.menu_bar.clear()

        file_menu = self.menu_bar.addMenu("&File")
        quit_action = QtWidgets.QAction("Quit", self)
        file_menu.addAction(quit_action)
        quit_action.triggered.connect(self.exit_application)
        export_action = QtWidgets.QAction("Export", self)
        file_menu.addAction(export_action)
        export_action.triggered.connect(model.export_all)

        debug_menu = self.menu_bar.addMenu("&Debug")
        update_gui_action = QtWidgets.QAction("Update GUI", self)
        update_gui_action.triggered.connect(self.update_gui)
        debug_menu.addAction(update_gui_action)
        show_rest_dialog_qaction = QtWidgets.QAction("Rest Dialog", self)
        show_rest_dialog_qaction.triggered.connect(
            functools.partial(rest_reminder_dialog.RestReminderDialog.show_dialog, self)
        )
        debug_menu.addAction(show_rest_dialog_qaction)

        window_menu = self.menu_bar.addMenu("&Windows")
        show_breathing_settings_window_action = self.breathing_settings_dock.toggleViewAction()
        window_menu.addAction(show_breathing_settings_window_action)
        show_rest_settings_window_action = self.rest_settings_dock.toggleViewAction()
        window_menu.addAction(show_rest_settings_window_action)
        show_quotes_window_action = self.quotes_dock.toggleViewAction()
        window_menu.addAction(show_quotes_window_action)

        help_menu = self.menu_bar.addMenu("&Help")
        about_action = QtWidgets.QAction("About", self)
        help_menu.addAction(about_action)
        about_action.triggered.connect(self.show_about_box)

    def show_about_box(self):
        message_box = QtWidgets.QMessageBox.about(
            self,
            "About Mindfulness at the Computer",
            ("Concept and programming by Tord\n"
            'Photography (for application icon) by Torgny Dellsén - torgnydellsen.zenfolio.com\n'
            'Other icons from Open Iconic - useiconic.com\n'
            "Software License: GPLv3\n"
            )
        )

        # "Photo license: CC BY-SA 4.0"

    # overridden
    def closeEvent(self, i_QCloseEvent):
        i_QCloseEvent.ignore()

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

