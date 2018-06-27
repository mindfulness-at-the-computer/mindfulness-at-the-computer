import enum
import os
from PyQt5 import QtGui

#############################################
# This file contains
# * global application state which is not stored in the database (on disk)
# * global functions relating to file names/paths
# * global font functions
# * potentially other global functions
#############################################

APPLICATION_TITLE_STR = "Mindfulness at the Computer"
APPLICATION_VERSION_STR = "1.0.0-alpha.4"
NO_PHRASE_SELECTED_INT = -1
NO_REST_ACTION_SELECTED_INT = -1
NOTHING_SELECTED_INT = -1
# -TODO: merge these three above into one
FEEDBACK_DIALOG_NOT_SHOWN_AT_STARTUP = -1
NR_OF_TIMES_UNTIL_FEEDBACK_SHOWN_INT = 10

LIST_ITEM_HEIGHT_INT = 30

GRID_VERTICAL_SPACING_LINUX = 15
BUTTON_BAR_HORIZONTAL_SPACING_LINUX = 2

APPLICATION_ICON_NAME_STR = "icon.png"
DATABASE_FILE_STR = "mindfulness-at-the-computer.db"
README_FILE_STR = "README.md"

USER_FILES_DIR_STR = "user_files"
IMAGES_DIR_STR = "images"
ICONS_DIR_STR = "icons"
OPEN_ICONIC_ICONS_DIR_STR = "open_iconic"
AUDIO_DIR_STR = "audio"

SMALL_BELL_SHORT_FILENAME_STR = "small_bell_short[cc0].wav"
SMALL_BELL_LONG_FILENAME_STR = "small_bell_long[cc0].wav"
WIND_CHIMES_FILENAME_STR = "wind_chimes[cc0].wav"

active_rest_action_id_it = NO_REST_ACTION_SELECTED_INT
active_phrase_id_it = NO_PHRASE_SELECTED_INT
rest_window_shown_bool = False
testing_bool = False
rest_reminder_minutes_passed_int = 0
# active_rest_image_full_path_str = "user_files/tea.png"
db_file_exists_at_application_startup_bl = False
display_inline_help_texts_bool = True  # -TODO
breathing_notification_counter_int = 0


class BreathingState(enum.Enum):
    inactive = 0
    breathing_in = 1
    breathing_out = 2


MC_LIGHT_GREEN_COLOR_STR = "#bfef7f"
MC_DARK_GREEN_COLOR_STR = "#7fcc19"  # "#7fcc19"
MC_DARKER_GREEN_COLOR_STR = "#548811"  # "#7fcc19"
MC_WHITE_COLOR_STR = "#ffffff"


class PhraseSetup(enum.Enum):
    Long = 0
    Switch = 1
    Short = 2


class NotificationType(enum.Enum):
    Both = 0
    Visual = 1
    Audio = 2


class BreathingPhraseType(enum.Enum):
    in_out = 0
    single = 1


class PhraseSelection(enum.Enum):
    same = 0
    random = 1


breathing_state = BreathingState.inactive


class BreathingVisType(enum.Enum):
    mainwindow_widget = 0
    popup_dialog = 1


def get_base_dir() -> str:
    base_dir_str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # -__file__ is the file that was started, in other words mindfulness-at-the-computer.py
    return base_dir_str


def get_database_filename(i_backup_timestamp: str = "") -> str:
    if testing_bool:
        return ":memory:"
    else:
        database_filename_str = DATABASE_FILE_STR
        if i_backup_timestamp:
            database_filename_str = i_backup_timestamp + "_" + DATABASE_FILE_STR
        ret_path_str = os.path.join(
            get_base_dir(),
            USER_FILES_DIR_STR,
            database_filename_str
        )
        return ret_path_str


def get_user_images_path(i_file_name: str="") -> str:
    if i_file_name:
        user_images_path_str = os.path.join(get_base_dir(), USER_FILES_DIR_STR, IMAGES_DIR_STR, i_file_name)
    else:
        user_images_path_str = os.path.join(get_base_dir(), USER_FILES_DIR_STR, IMAGES_DIR_STR)
    return user_images_path_str
    # user_dir_path_str = QtCore.QDir.currentPath() + "/user_files/images/"
    # return QtCore.QDir.toNativeSeparators(user_dir_path_str)


def get_user_audio_path(i_file_name: str="") -> str:
    if i_file_name:
        user_audio_path_str = os.path.join(get_base_dir(), USER_FILES_DIR_STR, AUDIO_DIR_STR, i_file_name)
    else:
        user_audio_path_str = os.path.join(get_base_dir(), USER_FILES_DIR_STR, AUDIO_DIR_STR)
    return user_audio_path_str


def get_app_icon_path(i_file_name: str) -> str:
    ret_icon_path_str = os.path.join(get_base_dir(), ICONS_DIR_STR, i_file_name)
    return ret_icon_path_str


def get_icon_path(i_file_name: str) -> str:
    ret_icon_path_str = os.path.join(get_base_dir(), ICONS_DIR_STR, OPEN_ICONIC_ICONS_DIR_STR, i_file_name)
    return ret_icon_path_str


"""
def get_icon_path(i_filename: str) -> str:
    return os.path.join(get_base_dir(), ICONS_DIR_STR, i_filename)

def get_app_icon_path() -> str:
    icon_file_name_str = "icon.png"
    ret_icon_path_str = os.path.join(get_base_dir(), ICONS_DIR_STR, icon_file_name_str)
    return ret_icon_path_str
"""


def get_user_files_path(i_file_name: str) -> str:
    return os.path.join(get_base_dir(), USER_FILES_DIR_STR, i_file_name)


"""
def does_database_exist_started() -> bool:
    if os.path.isfile(DATABASE_FILE_NAME):
        return True
    else:
        return False
"""

# Standard font size is (on almost all systems) 12


def get_font_small(i_italics: bool=False, i_bold: bool=False) -> QtGui.QFont:
    font = QtGui.QFont()
    font.setPointSize(9)
    font.setItalic(i_italics)
    font.setBold(i_bold)
    return font


def get_font_medium(i_italics: bool=False, i_bold: bool=False) -> QtGui.QFont:
    font = QtGui.QFont()
    font.setItalic(i_italics)
    font.setBold(i_bold)
    return font


def get_font_large(i_underscore: bool=False, i_italics: bool=False, i_bold: bool=False) -> QtGui.QFont:
    font = QtGui.QFont()
    font.setPointSize(13)
    font.setUnderline(i_underscore)
    font.setItalic(i_italics)
    font.setBold(i_bold)
    return font


def get_font_xlarge(i_underscore: bool=False, i_italics: bool=False, i_bold: bool=False) -> QtGui.QFont:
    font = QtGui.QFont()
    font.setPointSize(16)
    font.setUnderline(i_underscore)
    font.setItalic(i_italics)
    font.setBold(i_bold)
    return font


def get_font_xxlarge(i_underscore: bool=False, i_italics: bool=False, i_bold: bool=False) -> QtGui.QFont:
    font = QtGui.QFont()
    font.setPointSize(24)
    font.setUnderline(i_underscore)
    font.setItalic(i_italics)
    font.setBold(i_bold)
    return font


def get_html(i_text: str) -> str:
    ret_str = '<p style="text-align:center">' + i_text + '</p>'
    return ret_str


class EventSource(enum.Enum):
    undefined = 0
    rest_action_changed = 11
    rest_list_selection_changed = 12
    breathing_list_phrase_updated = 21
    breathing_list_selection_changed = 22
    breathing_phrase_deleted = 23
    rest_settings_changed_from_settings = 31
    rest_settings_changed_from_intro = 32
    rest_slider_value_changed = 34
    breathing_settings_changed_from_settings = 3
    breathing_settings_changed_from_intro = 4
    rest_opened = 5
    rest_closed = 6


db_upgrade_message_str = None


sys_info_telist = []


def clear_widget_and_layout_children(qlayout_or_qwidget) -> None:
    if qlayout_or_qwidget.widget():
        qlayout_or_qwidget.widget().deleteLater()
    elif qlayout_or_qwidget.layout():
        while qlayout_or_qwidget.layout().count():
            child_qlayoutitem = qlayout_or_qwidget.takeAt(0)
            clear_widget_and_layout_children(child_qlayoutitem)  # Recursive call
