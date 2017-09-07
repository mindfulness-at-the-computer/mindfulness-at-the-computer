import argparse
import logging
import sys
import os

from PyQt5 import QtGui
from PyQt5 import QtWidgets

from mc import mc_global
from mc.win import main_window

ICON_FILE_PATH_STR = "icon.png"

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
    app = QtWidgets.QApplication(sys.argv)
    main_window = main_window.MbMainWindow()

    # System tray
    main_window.tray_icon = QtWidgets.QSystemTrayIcon(QtGui.QIcon(ICON_FILE_PATH_STR), app)
    main_window.tray_icon.show()

    tray_menu = QtWidgets.QMenu(main_window)
    tray_restore_action = QtWidgets.QAction("Restore")
    tray_restore_action.triggered.connect(main_window.showNormal)
    tray_menu.addAction(tray_restore_action)
    tray_maximize_action = QtWidgets.QAction("Maximize")
    tray_maximize_action.triggered.connect(main_window.showMaximized)
    tray_menu.addAction(tray_maximize_action)
    tray_quit_action = QtWidgets.QAction("Quit")
    tray_quit_action.triggered.connect(main_window.exit_application)
    tray_menu.addAction(tray_quit_action)

    main_window.tray_icon.setContextMenu(tray_menu)
    if not main_window.tray_icon.supportsMessages():
        logging.warning("Your system doesn't support notifications. If you are using MacOS please install growl")

    sys.exit(app.exec_())

