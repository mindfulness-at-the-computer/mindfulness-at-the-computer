import enum
import os

APPLICATION_TITLE_STR = "Mindful breathing"
APPLICATION_VERSION_STR = "0.1"
NO_PHRASE_SELECTED = -1
DATABASE_FILE_NAME = "matc.db"

active_phrase_id_it = NO_PHRASE_SELECTED
testing_bool = False
rest_reminder_minutes_passed_int = 0
active_rest_image_full_path_str = "tea.png"
db_file_exists_at_application_startup_bl = False


class BreathingState(enum.Enum):
    inactive = 0
    breathing_in = 1
    breathing_out = 2

breathing_state = BreathingState.inactive


def get_database_filename():
    if testing_bool:
        return ":memory:"
    else:
        return DATABASE_FILE_NAME


"""
def does_database_exist_started() -> bool:
    if os.path.isfile(DATABASE_FILE_NAME):
        return True
    else:
        return False
"""

