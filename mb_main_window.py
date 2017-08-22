import logging
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import mb_global
import mb_breathing
import mb_phrases
import mb_collections
import mb_details


class MbMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.show()
        self.setGeometry(100, 100, 900, 600)
        self.setCorner(QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomRightCorner, QtCore.Qt.RightDockWidgetArea)

        self.tray_icon = None

        mb_global.active_collection_id_it = 1

        vbox_widget = QtWidgets.QWidget()
        self.setCentralWidget(vbox_widget)
        vbox = QtWidgets.QVBoxLayout()
        vbox_widget.setLayout(vbox)

        self.breathing_dock = QtWidgets.QDockWidget("Breathing Graph")
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.breathing_dock)
        self.breathing_composite_widget = mb_breathing.BreathingCompositeWidget()
        self.breathing_dock.setWidget(self.breathing_composite_widget)

        self.phrases = mb_phrases.PhrasesCompositeWidget()
        vbox.addWidget(self.phrases)

        self.collection_dock = QtWidgets.QDockWidget("Presets")
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.collection_dock)
        self.collection_list_widget = mb_collections.CollectionsCompositeWidget()
        self.collection_dock.setWidget(self.collection_list_widget)
        self.collection_list_widget.row_changed_signal.connect(self.update_gui)

        self.details_dock = QtWidgets.QDockWidget("Details")
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.details_dock)
        self.details_widget = mb_details.DetailsCompositeWidget()

        # Menu
        self.menu_bar = self.menuBar()
        self.update_menu()

        # TODO: reminders
        self.start_timer()

    def start_timer(self):
        self.self_care_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.self_care_qtimer.timeout.connect(self.timer_timeout)
        self.self_care_qtimer.start(30 * 1000)

    def timer_timeout(self):
        APPLICATION_TITLE_STR = "Mindful breathing"

        self.tray_icon.showMessage(
            APPLICATION_TITLE_STR,
            "breathing in i know i am breathing in\nbreathing out i know i am breathing out",
            msecs=10*1000
        )

    def debug_show_reminder(self):
        APPLICATION_TITLE_STR = "Mindful breathing"

        self.tray_icon.showMessage(
            APPLICATION_TITLE_STR,
            "breathing in i know i am breathing in\nbreathing out i know i am breathing out",
            msecs=10*1000
        )
        # QtGui.QIcon(ICON_FILE_PATH_STR),

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
        show_reminder_action = QtWidgets.QAction("Show Reminder", self)
        show_reminder_action.triggered.connect(self.debug_show_reminder)
        debug_menu.addAction(show_reminder_action)

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

    # overridden
    def keyPressEvent(self, iQKeyEvent):
        if iQKeyEvent.key() == QtCore.Qt.Key_Shift:
            logging.info("shift key pressed")
            self.breathing_composite_widget.stop_breathing_out_timer()
            self.breathing_composite_widget.start_breathing_in_timer()

            self.phrases.update_gui(mb_global.BreathingState.breathing_in)
        elif iQKeyEvent.key() == QtCore.Qt.Key_Return or iQKeyEvent.key() == QtCore.Qt.Key_Enter:
            logging.info("enter or return key pressed")
            self.breathing_composite_widget.stop_breathing_in_timer()
            self.breathing_composite_widget.stop_breathing_out_timer()
        elif iQKeyEvent.key() == QtCore.Qt.Key_Backspace or iQKeyEvent.key() == QtCore.Qt.Key_Delete:
            logging.info("backspace or delete key pressed")
            self.breathing_composite_widget.stop_breathing_in_timer()
            self.breathing_composite_widget.stop_breathing_out_timer()
            self.breathing_composite_widget.in_breath_graphics_qgri_list.clear()
            self.breathing_composite_widget.out_breath_graphics_qgri_list.clear()
            self.breathing_composite_widget.breathing_graphicsscene.clear()
        elif iQKeyEvent.key() == QtCore.Qt.Key_N:
            logging.info("N key pressed")
            self.phrases.next_phrase()

    # overridden
    def keyReleaseEvent(self, iQKeyEvent):
        if iQKeyEvent.key() == QtCore.Qt.Key_Shift:
            logging.info("shift key released")
            self.breathing_composite_widget.stop_breathing_in_timer()
            self.breathing_composite_widget.start_breathing_out_timer()

            self.phrases.update_gui(mb_global.BreathingState.breathing_out)

    def update_gui(self):
        self.phrases.update_gui()

