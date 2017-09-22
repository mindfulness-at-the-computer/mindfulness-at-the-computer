import enum
import os
from PyQt5 import QtCore
from PyQt5 import QtMultimedia


APPLICATION_TITLE_STR = "Mindfulness at the Computer"
APPLICATION_VERSION_STR = "0.1"
NO_PHRASE_SELECTED_INT = -1
NO_REST_ACTION_SELECTED_INT = -1

APPLICATION_ICON_NAME_STR = "icon.png"
DATABASE_FILE_STR = "mindfulness-at-the-computer.db"
README_FILE_STR = "README.md"

USER_FILES_DIR_STR = "user_files"
IMAGES_DIR_STR = "images"
ICONS_DIR_STR = "icons"
AUDIO_DIR_STR = "audio"

active_rest_action_id_it = NO_REST_ACTION_SELECTED_INT
active_phrase_id_it = NO_PHRASE_SELECTED_INT
testing_bool = False
rest_reminder_minutes_passed_int = 0
# active_rest_image_full_path_str = "user_files/tea.png"
db_file_exists_at_application_startup_bl = False
display_inline_help_texts_bool = True  # -TODO

tray_rest_progress_qaction = None


def update_tray_rest_progress_bar(time_passed_int, interval_minutes_int):
    if tray_rest_progress_qaction is not None:
        time_passed_str = ""
        parts_of_ten_int = (10 * time_passed_int) // interval_minutes_int
        for i in range(0, 9):
            if i < parts_of_ten_int:
                time_passed_str += "◾"
            else:
                time_passed_str += "◽"
        tray_rest_progress_qaction.setText(time_passed_str)


tray_rest_enabled_qaction = None
def update_tray_rest_checked(i_active: bool):
    if tray_rest_enabled_qaction is not None:
        tray_rest_enabled_qaction.setChecked(i_active)

tray_breathing_enabled_qaction = None
def update_tray_breathing_checked(i_checked: bool):
    if tray_breathing_enabled_qaction is not None:
        tray_breathing_enabled_qaction.setChecked(i_checked)
def update_tray_breathing_enabled(i_enabled: bool):
    if tray_breathing_enabled_qaction is not None:
        tray_breathing_enabled_qaction.setEnabled(i_enabled)


class BreathingState(enum.Enum):
    inactive = 0
    breathing_in = 1
    breathing_out = 2

breathing_state = BreathingState.inactive


def get_base_dir():
    base_dir_str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return base_dir_str


def get_database_filename():
    if testing_bool:
        return ":memory:"
    else:
        ret_path_str = os.path.join(get_base_dir(), USER_FILES_DIR_STR, DATABASE_FILE_STR)
        return ret_path_str


def get_user_images_path(i_file_name: str=""):
    if i_file_name:
        user_images_path_str = os.path.join(get_base_dir(), USER_FILES_DIR_STR, IMAGES_DIR_STR, i_file_name)
    else:
        user_images_path_str = os.path.join(get_base_dir(), USER_FILES_DIR_STR, IMAGES_DIR_STR)
    return user_images_path_str
    # user_dir_path_str = QtCore.QDir.currentPath() + "/user_files/images/"
    # return QtCore.QDir.toNativeSeparators(user_dir_path_str)


def get_icon_path(i_file_name: str):
    return os.path.join(get_base_dir(), ICONS_DIR_STR, i_file_name)


def get_app_icon_path():
    app_icon_path_str = get_icon_path(APPLICATION_ICON_NAME_STR)
    return app_icon_path_str


def get_user_files_path(i_file_name: str):
    return os.path.join(get_base_dir(), USER_FILES_DIR_STR, i_file_name)


def get_audio_path(i_file_name: str):
    return os.path.join(get_base_dir(), USER_FILES_DIR_STR, AUDIO_DIR_STR, i_file_name)

"""
def does_database_exist_started() -> bool:
    if os.path.isfile(DATABASE_FILE_NAME):
        return True
    else:
        return False
"""


def play_audio():
    """
    Qt audio overview: http://doc.qt.io/qt-5/audiooverview.html
    Please note that the audio file must be wav, if we want to play compressed audio files it will be
    more complicated (see docs page above)
    """

    QtMultimedia.QSound.play(
        get_audio_path("219028__jarredgibb__tibetan-bells-192khz-original[cc0]-1.wav")
    )


