import csv
import os
import enum
import logging
from mc import db
import mc.mc_global


class MoveDirectionEnum(enum.Enum):
    up = 1
    down = 2


class PhrasesM:
    def __init__(
        self,
        i_id: int,
        i_title: str,
        i_ib: str,
        i_ob: str,
        i_vert_order: int,
        i_ib_short: str,
        i_ob_short: str
    ) -> None:
        self.id_int = i_id
        self.title_str = i_title
        self.ib_str = i_ib
        self.ob_str = i_ob
        self.vert_order_int = i_vert_order
        self.ib_short_str = i_ib_short
        self.ob_short_str = i_ob_short

    @staticmethod
    def get_highest_sort_value() -> int:
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT MAX(" + mc.db.Schema.PhrasesTable.Cols.vertical_order + ")"
            + " FROM " + mc.db.Schema.PhrasesTable.name
        )
        return_value_int = db_cursor_result.fetchone()[0]
        # -0 has to be added here even though there can only be one value

        if return_value_int is None:
            # -to prevent error when the tables are empty
            return 0
        return return_value_int

    @staticmethod
    def get_lowest_sort_value() -> int:
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT MIN(" + mc.db.Schema.PhrasesTable.Cols.vertical_order + ")"
            + " FROM " + mc.db.Schema.PhrasesTable.name
        )
        return_value_int = db_cursor_result.fetchone()[0]
        # -0 has to be added here even though there can only be one value

        #to prevent error when the tables are empty
        if return_value_int == None:
            return 0
        return return_value_int

    @staticmethod
    def add(i_title: str, i_ib: str, i_ob: str, ib_short: str, ob_short: str) -> None:
        # vertical_order_last_pos_int = len(PhrasesM.get_all())
        if mc.mc_global.db_file_exists_at_application_startup_bl:
            vertical_order_last_pos_int = PhrasesM.get_highest_sort_value() + 1
        else:
            vertical_order_last_pos_int = 0
        logging.debug("vertical_order_last_pos_int = " + str(vertical_order_last_pos_int))
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "INSERT INTO " + db.Schema.PhrasesTable.name + "("
            + db.Schema.PhrasesTable.Cols.title + ", "
            + db.Schema.PhrasesTable.Cols.ib_phrase + ", "
            + db.Schema.PhrasesTable.Cols.ob_phrase + ", "
            + db.Schema.PhrasesTable.Cols.vertical_order + ", "
            + db.Schema.PhrasesTable.Cols.ib_short_phrase + ", "
            + db.Schema.PhrasesTable.Cols.ob_short_phrase
            + ") VALUES (?, ?, ?, ?, ?, ?)",
            (i_title, i_ib, i_ob, vertical_order_last_pos_int, ib_short, ob_short)
        )
        db_connection.commit()

    @staticmethod
    def get(i_id: int):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + db.Schema.PhrasesTable.name
            + " WHERE " + db.Schema.PhrasesTable.Cols.id + "=?",
            (str(i_id),)
        )
        reminder_db_te = db_cursor_result.fetchone()
        db_connection.commit()

        return PhrasesM(*reminder_db_te)
        # -the asterisk (*) will "expand" the tuple into separate arguments for the function header

    @staticmethod
    def get_all():
        ret_reminder_list = []
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + db.Schema.PhrasesTable.name
            + " ORDER BY " + db.Schema.PhrasesTable.Cols.vertical_order
        )
        phrases_db_te_list = db_cursor_result.fetchall()
        for phrases_db_te in phrases_db_te_list:
            ret_reminder_list.append(PhrasesM(*phrases_db_te))
        db_connection.commit()
        return ret_reminder_list

    @staticmethod
    def remove(i_id_int):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "DELETE FROM " + db.Schema.PhrasesTable.name
            + " WHERE " + db.Schema.PhrasesTable.Cols.id + "=?",
            (str(i_id_int),)
        )
        db_connection.commit()

    @staticmethod
    def update_title(i_id: int, i_new_title: str):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + db.Schema.PhrasesTable.name
            + " SET " + db.Schema.PhrasesTable.Cols.title + " = ?"
            + " WHERE " + db.Schema.PhrasesTable.Cols.id + " = ?",
            (i_new_title, str(i_id))
        )
        db_connection.commit()

    @staticmethod
    def update_in_breath(i_id: int, i_new_in_breath: str):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + db.Schema.PhrasesTable.name
            + " SET " + db.Schema.PhrasesTable.Cols.ib_phrase + " = ?"
            + " WHERE " + db.Schema.PhrasesTable.Cols.id + " = ?",
            (i_new_in_breath, str(i_id))
        )
        db_connection.commit()

    @staticmethod
    def update_out_breath(i_id: int, i_new_out_breath: str):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + db.Schema.PhrasesTable.name
            + " SET " + db.Schema.PhrasesTable.Cols.ob_phrase + " = ?"
            + " WHERE " + db.Schema.PhrasesTable.Cols.id + " = ?",
            (i_new_out_breath, str(i_id))
        )
        db_connection.commit()

    @staticmethod
    def update_short_ib_phrase(i_id: int, i_shortened_ib_phrase: str):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + db.Schema.PhrasesTable.name
            + " SET " + db.Schema.PhrasesTable.Cols.ib_short_phrase + " = ?"
            + " WHERE " + db.Schema.PhrasesTable.Cols.id + " = ?",
            (i_shortened_ib_phrase, str(i_id))
        )
        db_connection.commit()

    @staticmethod
    def update_short_ob_phrase(i_id: int, i_shortened_ob_phrase: str):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + db.Schema.PhrasesTable.name
            + " SET " + db.Schema.PhrasesTable.Cols.ob_short_phrase + " = ?"
            + " WHERE " + db.Schema.PhrasesTable.Cols.id + " = ?",
            (i_shortened_ob_phrase, str(i_id))
        )
        db_connection.commit()

    @staticmethod
    def update_sort_order_move_up_down(i_id: int, i_move_direction: MoveDirectionEnum) -> bool:
        main_id_int = i_id
        main_sort_order_int = PhrasesM.get(i_id).vert_order_int
        logging.debug("main_sort_order_int = " + str(main_sort_order_int))
        logging.debug("PhrasesM.get_highest_sort_value() = " + str(PhrasesM.get_highest_sort_value()))
        if i_move_direction == MoveDirectionEnum.up:
            if (main_sort_order_int <= PhrasesM.get_lowest_sort_value()
            or main_sort_order_int > PhrasesM.get_highest_sort_value()):
                return False
        elif i_move_direction == MoveDirectionEnum.down:
            if (main_sort_order_int < PhrasesM.get_lowest_sort_value()
            or main_sort_order_int >= PhrasesM.get_highest_sort_value()):
                return False
        other = PhrasesM.get_by_vert_order(main_sort_order_int, i_move_direction)
        other_id_int = other.id_int
        other_sort_order_int = other.vert_order_int

        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + db.Schema.PhrasesTable.name
            + " SET " + db.Schema.PhrasesTable.Cols.vertical_order + " = ?"
            + " WHERE " + db.Schema.PhrasesTable.Cols.id + " = ?",
            (str(other_sort_order_int), str(main_id_int))
        )
        db_cursor.execute(
            "UPDATE " + db.Schema.PhrasesTable.name
            + " SET " + db.Schema.PhrasesTable.Cols.vertical_order + " = ?"
            + " WHERE " + db.Schema.PhrasesTable.Cols.id + " = ?",
            (str(main_sort_order_int), str(other_id_int))
        )
        db_connection.commit()
        return True

    @staticmethod
    def get_by_vert_order(i_sort_order: int, i_move_direction: MoveDirectionEnum):

        direction_as_lt_gt_str = ">"
        sort_direction_str = "DESC"
        if i_move_direction == MoveDirectionEnum.up:
            direction_as_lt_gt_str = "<"
            sort_direction_str = "DESC"
        elif i_move_direction == MoveDirectionEnum.down:
            direction_as_lt_gt_str = ">"
            sort_direction_str = "ASC"

        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + db.Schema.PhrasesTable.name
            + " WHERE " + db.Schema.PhrasesTable.Cols.vertical_order + direction_as_lt_gt_str + str(i_sort_order)
            + " ORDER BY " + db.Schema.PhrasesTable.Cols.vertical_order + " " + sort_direction_str
        )
        journal_db_te = db_cursor_result.fetchone()
        db_connection.commit()

        return PhrasesM(*journal_db_te)


class RestActionsM:
    def __init__(
        self,
        i_id: int,
        i_title: str,
        i_image_path: str,
        i_vertical_order: int
    ) -> None:
        self.id_int = i_id
        self.title_str = i_title
        self.image_path_str = i_image_path
        self.vert_order_int = i_vertical_order

    @staticmethod
    def get_highest_sort_value() -> int:
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT MAX(" + mc.db.Schema.RestActionsTable.Cols.vertical_order + ")"
            + " FROM " + mc.db.Schema.RestActionsTable.name
        )
        return_value_int = db_cursor_result.fetchone()[0]
        # -0 has to be added here even though there can only be one value
        return return_value_int

    @staticmethod
    def get_lowest_sort_value() -> int:
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT MIN(" + mc.db.Schema.RestActionsTable.Cols.vertical_order + ")"
            + " FROM " + mc.db.Schema.RestActionsTable.name
        )
        return_value_int = db_cursor_result.fetchone()[0]
        # -0 has to be added here even though there can only be one value
        return return_value_int

    @staticmethod
    def add(i_title: str, i_image_path: str) -> None:
        vertical_order_last_pos_int = len(RestActionsM.get_all())
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "INSERT INTO " + db.Schema.RestActionsTable.name + "("
            + db.Schema.RestActionsTable.Cols.title + ", "
            + db.Schema.RestActionsTable.Cols.image_path + ", "
            + db.Schema.RestActionsTable.Cols.vertical_order
            + ") VALUES (?, ?, ?)", (i_title, i_image_path, vertical_order_last_pos_int)
        )
        db_connection.commit()

    @staticmethod
    def get(i_id: int):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + db.Schema.RestActionsTable.name
            + " WHERE " + db.Schema.RestActionsTable.Cols.id + "=?",
            (str(i_id), )
        )
        rest_action_db_te = db_cursor_result.fetchone()
        db_connection.commit()

        return RestActionsM(*rest_action_db_te)
        # -the asterisk (*) will "expand" the tuple into separate arguments for the function header

    @staticmethod
    def remove(i_id_int):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "DELETE FROM " + db.Schema.RestActionsTable.name
            + " WHERE " + db.Schema.RestActionsTable.Cols.id + "=?",
            (str(i_id_int), )
        )
        db_connection.commit()

    @staticmethod
    def get_all():
        ret_reminder_list = []
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + db.Schema.RestActionsTable.name
            + " ORDER BY " + db.Schema.RestActionsTable.Cols.vertical_order
        )
        rest_actions_db_te_list = db_cursor_result.fetchall()
        for rest_action_db_te in rest_actions_db_te_list:
            ret_reminder_list.append(RestActionsM(*rest_action_db_te))
        db_connection.commit()
        return ret_reminder_list

    @staticmethod
    def update_title(i_id: int, i_new_title: str):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + db.Schema.RestActionsTable.name
            + " SET " + db.Schema.RestActionsTable.Cols.title + " = ?"
            + " WHERE " + db.Schema.RestActionsTable.Cols.id + " = ?",
            (i_new_title, str(i_id))
        )
        db_connection.commit()

    @staticmethod
    def update_rest_action_image_path(i_id: int, i_new_image_path: str):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + db.Schema.RestActionsTable.name
            + " SET " + db.Schema.RestActionsTable.Cols.image_path + " = ?"
            + " WHERE " + db.Schema.RestActionsTable.Cols.id + " = ?",
            (i_new_image_path, str(i_id))
        )
        db_connection.commit()

    @staticmethod
    def update_sort_order_move_up_down(i_id: int, i_move_direction: MoveDirectionEnum) -> bool:
        main_id_int = i_id
        main_sort_order_int = RestActionsM.get(i_id).vert_order_int
        logging.debug("main_sort_order_int = " + str(main_sort_order_int))
        logging.debug("RestActionsM.get_highest_sort_value() = " + str(RestActionsM.get_highest_sort_value()))
        logging.debug("RestActionsM.get_lowest_sort_value() = " + str(RestActionsM.get_lowest_sort_value()))
        if i_move_direction == MoveDirectionEnum.up:
            if (main_sort_order_int == RestActionsM.get_lowest_sort_value()
            or main_sort_order_int > RestActionsM.get_highest_sort_value()):
                logging.debug("Exiting update_sort_order_move_up_down [up]")
                return False
        elif i_move_direction == MoveDirectionEnum.down:
            if (main_sort_order_int < RestActionsM.get_lowest_sort_value()
            or main_sort_order_int >= RestActionsM.get_highest_sort_value()):
                logging.debug("Exiting update_sort_order_move_up_down [down]")
                return False
        other = RestActionsM.get_by_vert_order(main_sort_order_int, i_move_direction)
        other_id_int = other.id_int
        other_sort_order_int = other.vert_order_int

        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + db.Schema.RestActionsTable.name
            + " SET " + db.Schema.RestActionsTable.Cols.vertical_order + " = ?"
            + " WHERE " + db.Schema.RestActionsTable.Cols.id + " = ?",
            (str(other_sort_order_int), str(main_id_int))
        )
        db_cursor.execute(
            "UPDATE " + db.Schema.RestActionsTable.name
            + " SET " + db.Schema.RestActionsTable.Cols.vertical_order + " = ?"
            + " WHERE " + db.Schema.RestActionsTable.Cols.id + " = ?",
            (str(main_sort_order_int), str(other_id_int))
        )
        db_connection.commit()
        return True

    @staticmethod
    def get_by_vert_order(i_sort_order: int, i_move_direction: MoveDirectionEnum):

        direction_as_lt_gt_str = ">"
        sort_direction_str = "DESC"
        if i_move_direction == MoveDirectionEnum.up:
            direction_as_lt_gt_str = "<"
            sort_direction_str = "DESC"
        elif i_move_direction == MoveDirectionEnum.down:
            direction_as_lt_gt_str = ">"
            sort_direction_str = "ASC"

        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + db.Schema.RestActionsTable.name
            + " WHERE " + db.Schema.RestActionsTable.Cols.vertical_order
            + " " + direction_as_lt_gt_str + " " + str(i_sort_order)
            + " ORDER BY " + db.Schema.RestActionsTable.Cols.vertical_order + " " + sort_direction_str
        )
        journal_db_te = db_cursor_result.fetchone()
        db_connection.commit()

        return RestActionsM(*journal_db_te)


class SettingsM:
    # noinspection PyUnusedLocal
    def __init__(
        self,
        i_id: int,  # unused
        i_rest_reminder_active: int,
        i_rest_reminder_interval: int,
        i_breathing_reminder_active: int,
        i_breathing_reminder_interval: int,
        i_breathing_reminder_audio_path: str,
        i_breathing_reminder_volume: int,
        i_breathing_reminder_notification_type: int,
        i_breathing_reminder_phrase_setup: int
    ) -> None:
        self.rest_reminder_active_bool = True if i_rest_reminder_active else False
        self.rest_reminder_interval_int = i_rest_reminder_interval
        self.breathing_reminder_active_bool = True if i_breathing_reminder_active else False
        self.breathing_reminder_interval_int = i_breathing_reminder_interval
        self.breathing_reminder_audio_path_str = i_breathing_reminder_audio_path
        self.breathing_reminder_volume_int = i_breathing_reminder_volume
        self.breathing_reminder_notification_type_int = i_breathing_reminder_notification_type
        self.breathing_reminder_phrase_setup_int = i_breathing_reminder_phrase_setup

    @staticmethod
    def get():
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + db.Schema.SettingsTable.name
            + " WHERE " + db.Schema.SettingsTable.Cols.id + "=?",
            (str(db.SINGLE_SETTINGS_ID_INT),)
        )
        settings_db_te = db_cursor_result.fetchone()
        db_connection.commit()

        return SettingsM(*settings_db_te)
        # -the asterisk (*) will "expand" the tuple into separate arguments for the function header

    @staticmethod
    def update_rest_reminder_active(i_reminder_active: bool):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        new_value_bool_as_int = db.SQLITE_TRUE_INT if i_reminder_active else db.SQLITE_FALSE_INT
        logging.debug("new_value_bool_as_int = " + str(new_value_bool_as_int))
        db_cursor.execute(
            "UPDATE " + db.Schema.SettingsTable.name
            + " SET " + db.Schema.SettingsTable.Cols.rest_reminder_active + " = ?"
            + " WHERE " + db.Schema.SettingsTable.Cols.id + " = ?",
            (new_value_bool_as_int, db.SINGLE_SETTINGS_ID_INT)
        )
        db_connection.commit()

        logging.debug("result=" + str(SettingsM.get().rest_reminder_active_bool))

    @staticmethod
    def update_rest_reminder_interval(i_reminder_interval: int):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + db.Schema.SettingsTable.name
            + " SET " + db.Schema.SettingsTable.Cols.rest_reminder_interval + " = ?"
            + " WHERE " + db.Schema.SettingsTable.Cols.id + " = ?",
            (str(i_reminder_interval), db.SINGLE_SETTINGS_ID_INT)
        )
        db_connection.commit()

    @staticmethod
    def update_breathing_reminder_active(i_reminder_active: bool):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + db.Schema.SettingsTable.name
            + " SET " + db.Schema.SettingsTable.Cols.breathing_reminder_active + " = ?"
            + " WHERE " + db.Schema.SettingsTable.Cols.id + " = ?",
            (db.SQLITE_TRUE_INT if i_reminder_active else db.SQLITE_FALSE_INT, db.SINGLE_SETTINGS_ID_INT)
        )
        db_connection.commit()

    @staticmethod
    def update_breathing_reminder_interval(i_reminder_interval: int):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + db.Schema.SettingsTable.name
            + " SET " + db.Schema.SettingsTable.Cols.breathing_reminder_interval + " = ?"
            + " WHERE " + db.Schema.SettingsTable.Cols.id + " = ?",
            (str(i_reminder_interval), db.SINGLE_SETTINGS_ID_INT)
        )
        db_connection.commit()

    @staticmethod
    def update_breathing_reminder_audio_path(i_new_audio_path: str):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + db.Schema.SettingsTable.name
            + " SET " + db.Schema.SettingsTable.Cols.breathing_reminder_audio_path + " = ?"
            + " WHERE " + db.Schema.SettingsTable.Cols.id + " = ?",
            (i_new_audio_path, str(db.SINGLE_SETTINGS_ID_INT))
        )
        db_connection.commit()

    @staticmethod
    def update_breathing_reminder_volume(i_new_volume: int):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + db.Schema.SettingsTable.name
            + " SET " + db.Schema.SettingsTable.Cols.breathing_reminder_volume + " = ?"
            + " WHERE " + db.Schema.SettingsTable.Cols.id + " = ?",
            (i_new_volume, str(db.SINGLE_SETTINGS_ID_INT))
        )
        db_connection.commit()

    @staticmethod
    def update_breathing_reminder_notification_type(i_new_notification_type: int):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + db.Schema.SettingsTable.name
            + " SET " + db.Schema.SettingsTable.Cols.breathing_reminder_notification_type + " = ?"
            + " WHERE " + db.Schema.SettingsTable.Cols.id + " = ?",
            (i_new_notification_type, str(db.SINGLE_SETTINGS_ID_INT))
        )
        db_connection.commit()

    @staticmethod
    def update_breathing_reminder_notification_phrase_setup(i_new_phrase_setup: int):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + db.Schema.SettingsTable.name
            + " SET " + db.Schema.SettingsTable.Cols.breathing_reminder_phrase_setup + " = ?"
            + " WHERE " + db.Schema.SettingsTable.Cols.id + " = ?",
            (i_new_phrase_setup, str(db.SINGLE_SETTINGS_ID_INT))
        )
        db_connection.commit()


def export_all():
    csv_writer = csv.writer(open(mc.mc_global.get_user_files_path("exported.csv"), "w"))
    for phrase in PhrasesM.get_all():
        # time_datetime = datetime.date.fromtimestamp(phrase.date_added_it)
        # date_str = time_datetime.strftime("%Y-%m-%d")
        csv_writer.writerow((phrase.title_str, phrase.ib_str, phrase.ob_str))


def populate_db_with_setup_data():
    PhrasesM.add(
        "In, Out",
        "Breathing in, I know I am breathing in",
        "Breathing out, I know I am breathing out",
        "in",
        "out"
    )
    PhrasesM.add(
        "Aware of Body",
        "Aware of my body, I breathe in",
        "Aware of my body, I breathe out",
        "body, in",
        "body, out"
    )
    PhrasesM.add(
        "Caring, Relaxing",
        "Breathing in, I care for my body",
        "Breathing out, I relax my body",
        "caring",
        "relaxing"
    )
    PhrasesM.add(
        "Happy, Safe",
        "May I be happy",
        "May I be peaceful",
        "happy",
        "peaceful"
    )
    PhrasesM.add(
        "Compassion",
        "Breathing in compassion to myself",
        "Breathing out compassion to others",
        "compassion to myself",
        "compassion to others"
    )
    PhrasesM.add(
        "Sharing, Contributing",
        "Breathing in I share in the well-being of others",
        "Breathing out I contribute to the well-being of others",
        "sharing well-being",
        "contributing to well-being"
    )

    RestActionsM.add(
        "Making a cup of tea",
        mc.mc_global.get_user_images_path("tea.png")
    )
    RestActionsM.add(
        "Filling a water bottle for my desk",
        ""
    )
    RestActionsM.add(
        "Stretching my arms",
        ""
    )
    RestActionsM.add(
        "Opening a window",
        mc.mc_global.get_user_images_path("window.png")
    )
    RestActionsM.add(
        "Watering the plants",
        ""
    )
    RestActionsM.add(
        "Cleaning/organizing my space",
        ""
    )
    RestActionsM.add(
        "Eating something healthy",
        mc.mc_global.get_user_images_path("oranges-with-flower.png")
    )
    RestActionsM.add(
        "Slow mindful walking inside",
        mc.mc_global.get_user_images_path("footprint.png")
    )
    RestActionsM.add(
        "Walking outside",
        mc.mc_global.get_user_images_path("boots-and-autumn-leaves.png")
    )


def populate_db_with_test_data():
    populate_db_with_setup_data()


def breathing_reminder_active() -> bool:
    settings = SettingsM.get()
    ret_value_bool = (
        (mc.mc_global.active_phrase_id_it != mc.mc_global.NO_PHRASE_SELECTED_INT)
        and
        settings.breathing_reminder_active_bool
    )
    return ret_value_bool


def get_app_systray_icon_path():
    icon_file_name_str = "icon.png"
    settings = SettingsM.get()
    b_active = breathing_reminder_active()
    if b_active and settings.rest_reminder_active_bool:
        icon_file_name_str = "icon-br.png"
    elif b_active:
        icon_file_name_str = "icon-b.png"
    elif settings.rest_reminder_active_bool:
        icon_file_name_str = "icon-r.png"

    ret_icon_path_str = os.path.join(mc.mc_global.get_base_dir(), mc.mc_global.ICONS_DIR_STR, icon_file_name_str)
    return ret_icon_path_str
