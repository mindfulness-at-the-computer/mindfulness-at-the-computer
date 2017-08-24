import logging
import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import mb_global
import mb_model
import mb_breathing
import mb_phrase_list


class MbMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.show()
        self.setGeometry(100, 100, 900, 600)
        self.setCorner(QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomRightCorner, QtCore.Qt.RightDockWidgetArea)

        self.tray_icon = None

        vbox_widget = QtWidgets.QWidget()
        self.setCentralWidget(vbox_widget)
        vbox = QtWidgets.QVBoxLayout()
        vbox_widget.setLayout(vbox)

        self.breathing_composite_widget = mb_breathing.BreathingCompositeWidget()
        vbox.addWidget(self.breathing_composite_widget)

        self.phrase_list_dock = QtWidgets.QDockWidget("List of Phrases")
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.phrase_list_dock)
        self.phrase_list_widget = mb_phrase_list.PhraseListCompositeWidget()
        self.phrase_list_dock.setWidget(self.phrase_list_widget)
        self.phrase_list_widget.row_changed_signal.connect(self.update_gui)

        # Menu
        self.menu_bar = self.menuBar()
        self.update_menu()

        self.start_background_breathing_notification_timer()

        self.start__timer()

    def start_background_breathing_notification_timer(self):
        self.self_care_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.self_care_qtimer.timeout.connect(self.timer_timeout)
        self.self_care_qtimer.start(30 * 1000)

    def timer_timeout(self):
        if mb_global.active_phrase_id_it != mb_global.NO_PHRASE_SELECTED:
            active_phrase = mb_model.PhrasesM.get(mb_global.active_phrase_id_it)
            self.tray_icon.showMessage(
                mb_global.APPLICATION_TITLE_STR,
                active_phrase.ib_str + "\n" + active_phrase.ob_str,
                icon=QtWidgets.QSystemTrayIcon.NoIcon,
                msecs=10*1000
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

