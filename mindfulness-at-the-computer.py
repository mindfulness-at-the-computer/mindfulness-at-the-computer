#!/usr/bin/env python3
import logging
import os
import sqlite3
import sys
import PyQt5.Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import mc.gui.main_win
from mc import mc_global
import mc.db

if __name__ == "__main__":
    mc_global.db_file_exists_at_application_startup_bl = os.path.isfile(mc_global.get_database_filename())
    # -settings this variable before the file has been created

    logging.basicConfig(level=logging.DEBUG)  # -by default only warnings and higher are shown

    # Application information
    logging.info(
        "===== Starting "
        + mc_global.APPLICATION_TITLE_STR + " - "
        + mc_global.APPLICATION_VERSION_STR + " ====="
    )
    logging.info("Python version: " + str(sys.version))
    logging.info("SQLite version: " + str(sqlite3.sqlite_version))
    logging.info("PySQLite (Python module) version: " + str(sqlite3.version))
    logging.info("Qt version: " + str(QtCore.qVersion()))
    # noinspection PyUnresolvedReferences
    logging.info("PyQt (Python module) version: " + str(PyQt5.Qt.PYQT_VERSION_STR))
    logging.info(
        mc_global.APPLICATION_TITLE_STR
        + " - Application version: " + str(mc_global.APPLICATION_VERSION_STR)
    )
    db_conn = mc.db.Helper.get_db_connection()
    logging.info(
        mc_global.APPLICATION_TITLE_STR
        + " - Database schema version: " + str(mc.db.get_schema_version(db_conn))
    )
    logging.info("=====")

    matc_qapplication = QtWidgets.QApplication(sys.argv)
    matc_qapplication.setQuitOnLastWindowClosed(False)
    matc_main_window = mc.gui.main_win.MainWin()
    matc_main_window.show()
    sys.exit(matc_qapplication.exec_())

    """
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
    """
