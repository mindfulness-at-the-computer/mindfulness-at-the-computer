import sys
import logging
import argparse
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import mb_global
import mb_main_window

ICON_FILE_PATH_STR = "icon.png"

if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "--testing", "-p", help="Persistent db storage", action="store_true"
    )
    # -for info about "store_true" please search here: https://docs.python.org/3/howto/argparse.html
    args = argument_parser.parse_args()
    if args.testing:
        mb_global.testing_bool = True
    else:
        mb_global.testing_bool = False

    logging.basicConfig(level=logging.DEBUG)  # -by default only warnings and higher are shown
    app = QtWidgets.QApplication(sys.argv)
    main_window = mb_main_window.MbMainWindow()

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

