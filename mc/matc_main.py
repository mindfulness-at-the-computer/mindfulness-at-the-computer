import logging
import functools

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import PyQt5.Qt

from mc import mc_global
from mc.gui import main_win
import mc.model
import mc.db


class MatC:

    def __init__(self, i_matc_qapplication):

        self.main_window = main_win.MbMainWindow()
        self.matc_qapplication = i_matc_qapplication
        self.matc_qapplication.setQuitOnLastWindowClosed(False)


        # System tray
        # Please note: We cannot move the update code into another function, even here in
        # this file (very strange), if we do we won't see the texts, only the separators,
        # unknown why but it may be because of a bug
        self.main_window.tray_icon = QtWidgets.QSystemTrayIcon(
            QtGui.QIcon(mc_global.get_app_icon_path()),
            self.matc_qapplication
        )
        self.main_window.tray_icon.show()
        # self.update_tray_menu()
        if not self.main_window.tray_icon.supportsMessages():
            logging.warning("Your system doesn't support notifications. If you are using MacOS please install growl")

        settings = mc.model.SettingsM.get()

        self.tray_menu = QtWidgets.QMenu(self.main_window)

        mc_global.tray_rest_enabled_qaction = QtWidgets.QAction("Enable Rest Reminder")
        self.tray_menu.addAction(mc_global.tray_rest_enabled_qaction)
        mc_global.tray_rest_enabled_qaction.setCheckable(True)
        mc_global.tray_rest_enabled_qaction.toggled.connect(
            self.main_window.rest_settings_widget.on_switch_toggled
        )
        mc_global.tray_rest_enabled_qaction.setChecked(settings.rest_reminder_active_bool)
        mc_global.tray_rest_progress_qaction = QtWidgets.QAction("")
        self.tray_menu.addAction(mc_global.tray_rest_progress_qaction)
        mc_global.tray_rest_progress_qaction.setDisabled(True)
        mc_global.update_tray_rest_progress_bar(0, 1)
        self.tray_rest_now_qaction = QtWidgets.QAction("Take a Break Now")
        self.tray_menu.addAction(self.tray_rest_now_qaction)
        self.tray_rest_now_qaction.triggered.connect(self.main_window.show_rest_reminder)

        self.tray_menu.addSeparator()

        mc_global.tray_breathing_enabled_qaction = QtWidgets.QAction("Enable Breathing Reminder")
        self.tray_menu.addAction(mc_global.tray_breathing_enabled_qaction)
        mc_global.tray_breathing_enabled_qaction.setCheckable(True)
        mc_global.tray_breathing_enabled_qaction.setChecked(settings.breathing_reminder_active_bool)
        mc_global.tray_breathing_enabled_qaction.toggled.connect(
            self.main_window.breathing_settings_widget.on_switch_toggled
        )
        mc_global.tray_breathing_enabled_qaction.setDisabled(True)


        count_int = 0
        mc_global.tray_phrase_qaction_list.clear()
        for l_phrase in mc.model.PhrasesM.get_all():
            INDENTATION_STR = "  "
            ACTIVE_MARKER_STR = "•"
            INACTIVE_MARKER_STR = " "
            active_or_inactive_str = INACTIVE_MARKER_STR
            if l_phrase.id_int == mc_global.active_phrase_id_it:
                active_or_inactive_str = ACTIVE_MARKER_STR
            tray_phrase_qaction = QtWidgets.QAction(active_or_inactive_str + INDENTATION_STR + l_phrase.title_str)
            tray_phrase_qaction.triggered.connect(
                functools.partial(
                    self.main_window.phrase_list_widget.on_new_row_selected_from_system_tray,
                    l_phrase.id_int
                )
            )
            mc_global.tray_phrase_qaction_list.append(tray_phrase_qaction)
            # self.tray_phrase_qaction = QtWidgets.QAction(l_phrase.title_str)
            self.tray_menu.addAction(tray_phrase_qaction)
            count_int += 1
            if count_int >= 5:
                break

        self.tray_menu.addSeparator()

        self.tray_restore_action = QtWidgets.QAction("Restore")
        self.tray_menu.addAction(self.tray_restore_action)
        self.tray_restore_action.triggered.connect(self.main_window.showNormal)
        self.tray_quit_action = QtWidgets.QAction("Quit")
        self.tray_menu.addAction(self.tray_quit_action)
        self.tray_quit_action.triggered.connect(self.main_window.exit_application)

        self.main_window.tray_icon.setContextMenu(self.tray_menu)


"""
        self.tray_maximize_action = QtWidgets.QAction("Maximize")
        self.tray_menu.addAction(self.tray_maximize_action)
        self.tray_maximize_action.triggered.connect(self.main_window.showMaximized)
        
"""

