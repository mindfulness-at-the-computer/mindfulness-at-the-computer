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

    mc.mc_global.sys_info_telist.append(("Application name", mc.mc_global.APPLICATION_VERSION_STR))
    mc.mc_global.sys_info_telist.append(("Application version", mc.mc_global.APPLICATION_VERSION_STR))
    db_conn = mc.db.Helper.get_db_connection()
    mc.mc_global.sys_info_telist.append(("Application database schema version", mc.db.get_schema_version(db_conn)))
    mc.mc_global.sys_info_telist.append(("Python version", sys.version))
    mc.mc_global.sys_info_telist.append(("SQLite version", sqlite3.sqlite_version))
    mc.mc_global.sys_info_telist.append(("PySQLite (Python module) version", sqlite3.version))
    mc.mc_global.sys_info_telist.append(("Qt version", QtCore.qVersion()))
    # noinspection PyUnresolvedReferences
    mc.mc_global.sys_info_telist.append(("PyQt (Python module) version", PyQt5.Qt.PYQT_VERSION_STR))

    matc_qapplication = QtWidgets.QApplication(sys.argv)

    translator = QtCore.QTranslator()
    # Warning While removing debug keep the loading call intact
    system_locale = QtCore.QLocale.system().name()
    logging.info('System Localization: ' + system_locale)
    logging.info('Localization Load Status: ' + str(translator.load(system_locale + '.qm', 'translate/' + system_locale))) # name, dir
    matc_qapplication.installTranslator(translator)

    matc_qapplication.setQuitOnLastWindowClosed(False)
    matc_main_window = mc.gui.main_win.MainWin()
    matc_main_window.show()

    if mc.mc_global.db_upgrade_message_str:
        QtWidgets.QMessageBox.warning(matc_main_window, "title", mc.mc_global.db_upgrade_message_str)

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
