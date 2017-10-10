#!/usr/bin/env python3
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
import mc.matc_main



if __name__ == "__main__":
    mc_global.db_file_exists_at_application_startup_bl = os.path.isfile(mc_global.get_database_filename())
    # -settings this variable before the file has been created

    logging.basicConfig(level=logging.DEBUG)  # -by default only warnings and higher are shown

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


    matc_qapplication = QtWidgets.QApplication(sys.argv)
    matc = mc.matc_main.MatC(matc_qapplication)
    matc.main_window.show()
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
