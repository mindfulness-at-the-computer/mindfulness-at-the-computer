import logging
import sys
import functools
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import mb_global
import mb_model
import mb_breathing
import mb_phrase_list
import mb_settings


class MbMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.show()
        self.setGeometry(100, 100, 900, 600)
        # self.setCorner(QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        # self.setCorner(QtCore.Qt.BottomRightCorner, QtCore.Qt.RightDockWidgetArea)
        self.setWindowIcon(QtGui.QIcon("icon.png"))

        self.tray_icon = None
        self.rest_reminder_qtimer = None
        self.breathing_qtimer = None

        vbox_widget = QtWidgets.QWidget()
        self.setCentralWidget(vbox_widget)
        vbox = QtWidgets.QVBoxLayout()
        vbox_widget.setLayout(vbox)

        self.breathing_composite_widget = mb_breathing.BreathingCompositeWidget()
        vbox.addWidget(self.breathing_composite_widget)

        self.phrase_list_dock = QtWidgets.QDockWidget("List of Phrases")
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.phrase_list_dock)
        self.phrase_list_dock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.phrase_list_widget = mb_phrase_list.PhraseListCompositeWidget()
        self.phrase_list_dock.setWidget(self.phrase_list_widget)
        self.phrase_list_widget.row_changed_signal.connect(self.phrase_row_changed)

        self.settings_dock = QtWidgets.QDockWidget("Settings")
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.settings_dock)
        # settings_dock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.settings_widget = mb_settings.SettingsComposite()
        self.settings_dock.setWidget(self.settings_widget)
        self.settings_widget.rest_settings_updated_signal.connect(self.on_rest_settings_updated)
        self.settings_widget.breathing_settings_updated_signal.connect(self.on_breathing_settings_updated)
        self.settings_widget.breathing_test_button_clicked_signal.connect(self.show_breathing_notification)
        self.settings_widget.rest_test_button_clicked_signal.connect(self.show_rest_reminder)

        # Menu
        self.menu_bar = self.menuBar()
        self.update_menu()

        self.start_breathing_notification_timer()

        self.start_rest_reminder_timer()

    def phrase_row_changed(self):
        self.start_breathing_notification_timer()
        self.update_gui()

    def on_rest_settings_updated(self):
        settings = mb_model.SettingsM.get()
        if settings.rest_reminder_active_bool:
            self.start_rest_reminder_timer()
        else:
            self.stop_rest_reminder_timer()

    def stop_rest_reminder_timer(self):
        if self.rest_reminder_qtimer is not None and self.rest_reminder_qtimer.isActive():
            self.rest_reminder_qtimer.stop()

    def start_rest_reminder_timer(self):
        self.stop_rest_reminder_timer()
        rest_reminder_interval_minutes_int = mb_model.SettingsM.get().rest_reminder_interval_int
        self.rest_reminder_qtimer = QtCore.QTimer(self)
        self.rest_reminder_qtimer.timeout.connect(self.show_rest_reminder)
        self.rest_reminder_qtimer.start(rest_reminder_interval_minutes_int * 60 * 1000)

    def show_rest_reminder(self):
        RestReminderDialog.show_dialog(self)
        # TODO: Do we want to set another icon for the system tray?

    def on_breathing_settings_updated(self):
        settings = mb_model.SettingsM.get()
        if settings.breathing_reminder_active_bool:
            self.start_breathing_notification_timer()
        else:
            self.stop_breathing_notification_timer()

    def stop_breathing_notification_timer(self):
        if self.breathing_qtimer is not None and self.breathing_qtimer.isActive():
            self.breathing_qtimer.stop()

    def start_breathing_notification_timer(self):
        self.stop_breathing_notification_timer()
        settings = mb_model.SettingsM.get()
        self.breathing_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.breathing_qtimer.timeout.connect(self.show_breathing_notification)
        self.breathing_qtimer.start(settings.breathing_reminder_interval_int * 1000)

    def show_breathing_notification(self):
        settings = mb_model.SettingsM.get()
        if mb_global.active_phrase_id_it != mb_global.NO_PHRASE_SELECTED:
            active_phrase = mb_model.PhrasesM.get(mb_global.active_phrase_id_it)
            reminder_str = active_phrase.ib_str + "\n" + active_phrase.ob_str
            self.tray_icon.showMessage(
                mb_global.APPLICATION_TITLE_STR,
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

        debug_menu = self.menu_bar.addMenu("&Debug")
        update_gui_action = QtWidgets.QAction("Update GUI", self)
        update_gui_action.triggered.connect(self.update_gui)
        debug_menu.addAction(update_gui_action)
        show_rest_dialog_qaction = QtWidgets.QAction("Rest Dialog", self)
        show_rest_dialog_qaction.triggered.connect(
            functools.partial(RestReminderDialog.show_dialog, self)
        )
        debug_menu.addAction(show_rest_dialog_qaction)

        window_menu = self.menu_bar.addMenu("&Windows")
        show_settings_window_action = self.settings_dock.toggleViewAction()
        window_menu.addAction(show_settings_window_action)

        help_menu = self.menu_bar.addMenu("&Help")
        about_action = QtWidgets.QAction("About", self)
        help_menu.addAction(about_action)

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


class RestReminderDialog(QtWidgets.QDialog):
    def __init__(self, i_parent):
        super(RestReminderDialog, self).__init__(i_parent)
        self.setWindowTitle("Please take care of yourself")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        vbox = QtWidgets.QVBoxLayout(self)
        # -please note: If we don't send "self" to the QVBoxLayout we won't see the main window
        #  in the background of the dialog. Also we don't need to use self.setLayout(vbox)

        rest_kindness_alternatives_qbb = QtWidgets.QDialogButtonBox()
        vbox.addWidget(rest_kindness_alternatives_qbb)

        rest_kindness_alternatives_qbb.setOrientation(QtCore.Qt.Vertical)

        movement_qpb = QtWidgets.QPushButton("Movement exercise")
        rest_kindness_alternatives_qbb.addButton(movement_qpb, QtWidgets.QDialogButtonBox.YesRole)
        walk_qpb = QtWidgets.QPushButton("Taking a walk")
        rest_kindness_alternatives_qbb.addButton(walk_qpb, QtWidgets.QDialogButtonBox.YesRole)

        wait_qpb = QtWidgets.QPushButton("Wait (snooze) for 5 minutes")
        rest_kindness_alternatives_qbb.addButton(wait_qpb, QtWidgets.QDialogButtonBox.NoRole)

        close_qpb = QtWidgets.QPushButton("Close")
        rest_kindness_alternatives_qbb.addButton(close_qpb, QtWidgets.QDialogButtonBox.NoRole)
        close_qpb.clicked.connect(self.on_close_button_clicked)

        # Roles: http://doc.qt.io/qt-5/qdialogbuttonbox.html#ButtonRole-enum

        """
        tension in body, releasing tension, mindful movements
        mindfulness of walking
        making tea, drinking tea
        
        **if skipping break: arms over head**
        stretching arms
        """

        # TODO: Idea: For each action have a small image that the user can set

    def on_close_button_clicked(self):
        ##self.parent().show()
        self.accept()

    @staticmethod
    def show_dialog(i_parent):
        i_parent.show()
        # -PLEASE NOTE: We have to make sure the window is visible if using a modal dialog,
        #  otherwise when the dialog is closed the whole application will close as well
        #  (unknown why)
        rest_reminder_dialog = RestReminderDialog(i_parent)
        rest_reminder_dialog.exec()

