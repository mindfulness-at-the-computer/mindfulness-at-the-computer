import enum


NO_DIARY_ENTRY_SELECTED = -1
DATABASE_FILE_NAME = "mb_database_file.db"

active_question_id_it = NO_DIARY_ENTRY_SELECTED
active_collection_id_it = NO_DIARY_ENTRY_SELECTED
persistent_bool = False


class BreathingState(enum.Enum):
    inactive = 0
    breathing_in = 1
    breathing_out = 2

breathing_state = BreathingState.inactive


def get_database_filename():
    if persistent_bool:
        return DATABASE_FILE_NAME
    else:
        return ":memory:"



