import argparse
import logging
import sys
import os
import sqlite3

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import PyQt5.Qt

from mc import mc_global
from mc.gui import main_win
import mc.model
import mc.db


if __name__ == "__main__":
    mc_global.db_file_exists_at_application_startup_bl = os.path.isfile(mc_global.get_database_filename())
    # -settings this variable before the file has been created

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "--testing", "-t", help="Testing", action="store_true"
    )
    # -for info about "store_true" please search here: https://docs.python.org/3/howto/argparse.html
    args = argument_parser.parse_args()
    if args.testing:
        mc_global.testing_bool = True
    else:
        mc_global.testing_bool = False

    logging.basicConfig(level=logging.DEBUG)  # -by default only warnings and higher are shown
    matc_qapplication = QtWidgets.QApplication(sys.argv)
    matc_qapplication.setQuitOnLastWindowClosed(False)
    main_window = main_win.MbMainWindow()

    # System tray
    # Please note: We cannot move the update code into another function, even here in
    # this file (very strange), if we do we won't see the texts, only the separators,
    # unknown why but it may be because of a bug
    main_window.tray_icon = QtWidgets.QSystemTrayIcon(
        QtGui.QIcon(mc_global.get_app_icon_path()),
        matc_qapplication
    )
    main_window.tray_icon.show()
    # self.update_tray_menu()
    if not main_window.tray_icon.supportsMessages():
        logging.warning("Your system doesn't support notifications. If you are using MacOS please install growl")

    settings = mc.model.SettingsM.get()

    tray_menu = QtWidgets.QMenu(main_window)

    tray_restore_action = QtWidgets.QAction("Restore")
    tray_menu.addAction(tray_restore_action)
    tray_restore_action.triggered.connect(main_window.showNormal)
    tray_maximize_action = QtWidgets.QAction("Maximize")
    tray_menu.addAction(tray_maximize_action)
    tray_maximize_action.triggered.connect(main_window.showMaximized)
    tray_quit_action = QtWidgets.QAction("Quit")
    tray_menu.addAction(tray_quit_action)
    tray_quit_action.triggered.connect(main_window.exit_application)

    tray_menu.addSeparator()
    mc_global.tray_rest_progress_qaction = QtWidgets.QAction("")
    tray_menu.addAction(mc_global.tray_rest_progress_qaction)
    mc_global.tray_rest_progress_qaction.setDisabled(True)
    mc_global.update_tray_rest_progress_bar(0, 1)
    tray_rest_now_qaction = QtWidgets.QAction("Take a Break Now")
    tray_menu.addAction(tray_rest_now_qaction)
    tray_rest_now_qaction.triggered.connect(main_window.show_rest_reminder)
    mc_global.tray_rest_enabled_qaction = QtWidgets.QAction("Enable Rest Reminder")
    tray_menu.addAction(mc_global.tray_rest_enabled_qaction)
    mc_global.tray_rest_enabled_qaction.setCheckable(True)
    mc_global.tray_rest_enabled_qaction.toggled.connect(
        main_window.rest_settings_widget.on_switch_toggled
    )
    mc_global.tray_rest_enabled_qaction.setChecked(settings.rest_reminder_active_bool)

    tray_menu.addSeparator()
    mc_global.tray_breathing_enabled_qaction = QtWidgets.QAction("Enable Breathing Reminder")
    tray_menu.addAction(mc_global.tray_breathing_enabled_qaction)
    mc_global.tray_breathing_enabled_qaction.setCheckable(True)
    mc_global.tray_breathing_enabled_qaction.setChecked(settings.breathing_reminder_active_bool)
    mc_global.tray_breathing_enabled_qaction.toggled.connect(
        main_window.breathing_settings_widget.on_switch_toggled
    )
    mc_global.tray_breathing_enabled_qaction.setDisabled(True)


    main_window.tray_icon.setContextMenu(tray_menu)





    # Application information
    logging.info("===== Starting "
        + mc_global.APPLICATION_TITLE_STR + " - "
        + mc_global.APPLICATION_VERSION_STR + " ====="
    )
    logging.info("Python version: " + str(sys.version))
    logging.info("SQLite version: " + str(sqlite3.sqlite_version))
    logging.info("PySQLite (Python module) version: " + str(sqlite3.version))
    logging.info("Qt version: " + str(QtCore.qVersion()))
    logging.info("PyQt (Python module) version: " + str(PyQt5.Qt.PYQT_VERSION_STR))
    logging.info(mc_global.APPLICATION_TITLE_STR + " Application version: " + str(mc_global.APPLICATION_VERSION_STR))
    db_conn = mc.db.Helper.get_db_connection()
    logging.info(mc_global.APPLICATION_TITLE_STR + " Database schema version: " + str(mc.db.get_schema_version(db_conn)))
    logging.info("=====")

    sys.exit(matc_qapplication.exec_())

