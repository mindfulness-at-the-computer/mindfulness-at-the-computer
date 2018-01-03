import csv
import os
import enum
import logging
import typing
from mc import db
import mc.mc_global


class MoveDirectionEnum(enum.Enum):
    up = 1
    down = 2


class MinOrMaxEnum(enum.Enum):
    min = "MIN"
    max = "MAX"


def db_exec(i_sql: str, i_params: tuple=None):
    db_connection = db.Helper.get_db_connection()
    db_cursor = db_connection.cursor()
    db_cursor_result = None
    if i_params is not None:
        db_cursor_result = db_cursor.execute(i_sql, i_params)
    else:
        db_cursor_result = db_cursor.execute(i_sql)
    db_connection.commit()
    return db_cursor_result


class PhrasesM:
    def __init__(
        self,
        i_id: int,
        i_vert_order: int,
        i_title: str,
        i_ib: str,
        i_ob: str,
        i_ib_short: str,
        i_ob_short: str
    ) -> None:
        self._id_int = i_id
        self._vert_order_int = i_vert_order
        self._title_str = i_title
        self._ib_str = i_ib
        self._ob_str = i_ob
        self._ib_short_str = i_ib_short
        self._ob_short_str = i_ob_short

    @property
    def id(self) -> int:
        return self._id_int

    @property
    def title(self) -> str:
        return self._title_str

    @title.setter
    def title(self, i_new_title: str):
        self._title_str = i_new_title
        self._update(db.Schema.PhrasesTable.Cols.title, i_new_title)

    @property
    def vert_order(self) -> int:
        return self._vert_order_int

    @vert_order.setter
    def vert_order(self, i_new_vert_order: int):
        self._vert_order_int = i_new_vert_order
        self._update(db.Schema.PhrasesTable.Cols.vertical_order, i_new_vert_order)

    @property
    def ib(self) -> str:
        return self._ib_str

    @ib.setter
    def ib(self, i_new_ib: str):
        self._ib_str = i_new_ib
        self._update(db.Schema.PhrasesTable.Cols.ib_phrase, i_new_ib)

    @property
    def ob(self) -> str:
        return self._ob_str

    @ob.setter
    def ob(self, i_new_ob: str):
        self._ib_str = i_new_ob
        self._update(db.Schema.PhrasesTable.Cols.ob_phrase, i_new_ob)

    @property
    def ib_short(self) -> str:
        return self._ib_short_str

    @ib_short.setter
    def ib_short(self, i_new_ib_short: str):
        self._ib_short_str = i_new_ib_short
        self._update(db.Schema.PhrasesTable.Cols.ib_short_phrase, i_new_ib_short)

    @property
    def ob_short(self) -> str:
        return self._ob_short_str

    @ob_short.setter
    def ob_short(self, i_new_ob_short: str):
        self._ob_short_str = i_new_ob_short
        self._update(db.Schema.PhrasesTable.Cols.ob_short_phrase, i_new_ob_short)

    @staticmethod
    def add(i_title: str, i_ib: str, i_ob: str, ib_short: str, ob_short: str) -> None:
        # vertical_order_last_pos_int = len(PhrasesM.get_all())
        vertical_order_last_pos_int = PhrasesM._get_highest_or_lowest_sort_value(MinOrMaxEnum.max) + 1
        db_exec(
            "INSERT INTO " + db.Schema.PhrasesTable.name + "("
            + db.Schema.PhrasesTable.Cols.vertical_order + ", "
            + db.Schema.PhrasesTable.Cols.title + ", "
            + db.Schema.PhrasesTable.Cols.ib_phrase + ", "
            + db.Schema.PhrasesTable.Cols.ob_phrase + ", "
            + db.Schema.PhrasesTable.Cols.ib_short_phrase + ", "
            + db.Schema.PhrasesTable.Cols.ob_short_phrase
            + ") VALUES (?, ?, ?, ?, ?, ?)",
            (vertical_order_last_pos_int, i_title, i_ib, i_ob, ib_short, ob_short)
        )

    @staticmethod
    def get(i_id: int):
        db_cursor_result = db_exec(
            "SELECT * FROM " + db.Schema.PhrasesTable.name
            + " WHERE " + db.Schema.PhrasesTable.Cols.id + "=?",
            (str(i_id),)
        )
        reminder_db_te = db_cursor_result.fetchone()
        return PhrasesM(*reminder_db_te)
        # -the asterisk (*) will "expand" the tuple into separate arguments for the function header

    @staticmethod
    def get_all():
        ret_phrase_list = []
        db_cursor_result = db_exec(
            "SELECT * FROM " + db.Schema.PhrasesTable.name
            + " ORDER BY " + db.Schema.PhrasesTable.Cols.vertical_order
        )
        phrases_db_te_list = db_cursor_result.fetchall()
        for phrases_db_te in phrases_db_te_list:
            ret_phrase_list.append(PhrasesM(*phrases_db_te))
        return ret_phrase_list

    @staticmethod
    def remove(i_id: int):
        db_exec(
            "DELETE FROM " + db.Schema.PhrasesTable.name
            + " WHERE " + db.Schema.PhrasesTable.Cols.id + "=?",
            (str(i_id),)
        )

    @staticmethod
    def is_empty():
        db_cursor_result = db_exec(
            "SELECT count(*) FROM "
            + db.Schema.PhrasesTable.name
        )
        empty_rows_te = db_cursor_result.fetchone()
        logging.debug(*empty_rows_te)
        if empty_rows_te[0] == 0:
            return True
        else:
            return False

    def _update(self, i_col_name: str, i_new_value):
        db_exec(
            "UPDATE " + db.Schema.PhrasesTable.name
            + " SET " + i_col_name + " = ?"
            + " WHERE " + db.Schema.PhrasesTable.Cols.id + " = ?",
            (i_new_value, str(self._id_int))
        )

    @staticmethod
    def _update_sort_order_move_up_down(i_id: int, i_move_direction: MoveDirectionEnum) -> bool:
        main_id_int = i_id
        main_sort_order_int = PhrasesM.get(i_id)._vert_order_int
        if i_move_direction == MoveDirectionEnum.up:
            if (main_sort_order_int <= PhrasesM._get_highest_or_lowest_sort_value(MinOrMaxEnum.min)
            or main_sort_order_int > PhrasesM._get_highest_or_lowest_sort_value(MinOrMaxEnum.max)):
                return False
        elif i_move_direction == MoveDirectionEnum.down:
            if (main_sort_order_int < PhrasesM._get_highest_or_lowest_sort_value(MinOrMaxEnum.min)
            or main_sort_order_int >= PhrasesM._get_highest_or_lowest_sort_value(MinOrMaxEnum.max)):
                return False
        other = PhrasesM._get_by_vert_order(main_sort_order_int, i_move_direction)
        other_id_int = other._id_int
        other_sort_order_int = other._vert_order_int
        db_exec(
            "UPDATE " + db.Schema.PhrasesTable.name
            + " SET " + db.Schema.PhrasesTable.Cols.vertical_order + " = ?"
            + " WHERE " + db.Schema.PhrasesTable.Cols.id + " = ?",
            (str(other_sort_order_int), str(main_id_int))
        )
        db_exec(
            "UPDATE " + db.Schema.PhrasesTable.name
            + " SET " + db.Schema.PhrasesTable.Cols.vertical_order + " = ?"
            + " WHERE " + db.Schema.PhrasesTable.Cols.id + " = ?",
            (str(main_sort_order_int), str(other_id_int))
        )
        return True

    @staticmethod
    def _get_by_vert_order(i_sort_order: int, i_move_direction: MoveDirectionEnum):
        direction_as_lt_gt_str = ">"
        sort_direction_str = "DESC"
        if i_move_direction == MoveDirectionEnum.up:
            direction_as_lt_gt_str = "<"
            sort_direction_str = "DESC"
        elif i_move_direction == MoveDirectionEnum.down:
            direction_as_lt_gt_str = ">"
            sort_direction_str = "ASC"

        db_cursor_result = db_exec(
            "SELECT * FROM " + db.Schema.PhrasesTable.name
            + " WHERE " + db.Schema.PhrasesTable.Cols.vertical_order + direction_as_lt_gt_str + str(i_sort_order)
            + " ORDER BY " + db.Schema.PhrasesTable.Cols.vertical_order + " " + sort_direction_str
        )
        phrase_db_te = db_cursor_result.fetchone()

        return PhrasesM(*phrase_db_te)

    @staticmethod
    def _get_highest_or_lowest_sort_value(i_min_or_max: MinOrMaxEnum) -> int:
        db_cursor_result = db_exec(
            "SELECT " + i_min_or_max.value
            + " (" + mc.db.Schema.PhrasesTable.Cols.vertical_order + ")"
            + " FROM " + mc.db.Schema.PhrasesTable.name
        )
        return_value_int = db_cursor_result.fetchone()[0]
        # -0 has to be added here even though there can only be one value

        if return_value_int is None:
            # -to prevent error when the tables are empty
            return 0
        return return_value_int


class RestActionsM:
    def __init__(
        self,
        i_id: int,
        i_vertical_order: int,
        i_title: str,
        i_image_path: str
    ) -> None:
        self._id_int = i_id
        self._vert_order_int = i_vertical_order
        self._title_str = i_title
        self._image_path_str = i_image_path

    @property
    def id(self) -> int:
        return self._id_int
    # no setter

    @property
    def vert_order(self) -> int:
        return self._vert_order_int
    # no setter

    @property
    def title(self) -> str:
        return self._title_str

    @title.setter
    def title(self, i_new_title: str):
        self._title_str = i_new_title
        self._update(db.Schema.RestActionsTable.Cols.title, i_new_title)

    @property
    def image_path(self):
        return self._image_path_str

    @image_path.setter
    def image_path(self, i_new_path: str):
        self._image_path_str = i_new_path
        self._update(db.Schema.RestActionsTable.Cols.image_path, i_new_path)

    def _update(self, i_col_name: str, i_new_value):
        db_exec(
            "UPDATE " + db.Schema.PhrasesTable.name
            + " SET " + i_col_name + " = ?"
            + " WHERE " + db.Schema.PhrasesTable.Cols.id + " = ?",
            (i_new_value, str(self._id_int))
        )

    @staticmethod
    def add(i_title: str, i_image_path: str) -> None:
        vertical_order_last_pos_int = RestActionsM._get_highest_or_lowest_sort_value(MinOrMaxEnum.max)
        db_exec(
            "INSERT INTO " + db.Schema.RestActionsTable.name + "("
            + db.Schema.RestActionsTable.Cols.vertical_order + ", "
            + db.Schema.RestActionsTable.Cols.title + ", "
            + db.Schema.RestActionsTable.Cols.image_path
            + ") VALUES (?, ?, ?)",
            (vertical_order_last_pos_int, i_title, i_image_path)
        )

    @staticmethod
    def get(i_id: int):
        db_cursor_result = db_exec(
            "SELECT * FROM " + db.Schema.RestActionsTable.name
            + " WHERE " + db.Schema.RestActionsTable.Cols.id + "=?",
            (str(i_id),)
        )
        rest_action_db_te = db_cursor_result.fetchone()
        return RestActionsM(*rest_action_db_te)
        # -the asterisk (*) will "expand" the tuple into separate arguments for the function header

    @staticmethod
    def remove(i_id: int):
        db_exec(
            "DELETE FROM " + db.Schema.RestActionsTable.name
            + " WHERE " + db.Schema.RestActionsTable.Cols.id + "=?",
            (str(i_id),)
        )

    @staticmethod
    def get_all():
        ret_reminder_list = []
        db_cursor_result = db_exec(
            "SELECT * FROM " + db.Schema.RestActionsTable.name
            + " ORDER BY " + db.Schema.RestActionsTable.Cols.vertical_order
        )
        rest_actions_db_te_list = db_cursor_result.fetchall()
        for rest_action_db_te in rest_actions_db_te_list:
            ret_reminder_list.append(RestActionsM(*rest_action_db_te))
        return ret_reminder_list

    @staticmethod
    def update_sort_order_move_up_down(i_id: int, i_move_direction: MoveDirectionEnum) -> bool:
        main_id_int = i_id
        main_sort_order_int = RestActionsM.get(i_id)._vert_order_int
        if i_move_direction == MoveDirectionEnum.up:
            if (main_sort_order_int <= RestActionsM._get_highest_or_lowest_sort_value(MinOrMaxEnum.min)
            or main_sort_order_int > RestActionsM._get_highest_or_lowest_sort_value(MinOrMaxEnum.max)):
                return False
        elif i_move_direction == MoveDirectionEnum.down:
            if (main_sort_order_int < RestActionsM._get_highest_or_lowest_sort_value(MinOrMaxEnum.min)
            or main_sort_order_int >= RestActionsM._get_highest_or_lowest_sort_value(MinOrMaxEnum.max)):
                return False
        other = RestActionsM.get_by_vert_order(main_sort_order_int, i_move_direction)
        other_id_int = other.id
        other_sort_order_int = other._vert_order_int
        db_exec(
            "UPDATE " + db.Schema.RestActionsTable.name
            + " SET " + db.Schema.RestActionsTable.Cols.vertical_order + " = ?"
            + " WHERE " + db.Schema.RestActionsTable.Cols.id + " = ?",
            (str(other_sort_order_int), str(main_id_int))
        )
        db_exec(
            "UPDATE " + db.Schema.RestActionsTable.name
            + " SET " + db.Schema.RestActionsTable.Cols.vertical_order + " = ?"
            + " WHERE " + db.Schema.RestActionsTable.Cols.id + " = ?",
            (str(main_sort_order_int), str(other_id_int))
        )
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
        db_cursor_result = db_exec(
            "SELECT * FROM " + db.Schema.RestActionsTable.name
            + " WHERE " + db.Schema.RestActionsTable.Cols.vertical_order
            + " " + direction_as_lt_gt_str + " " + str(i_sort_order)
            + " ORDER BY " + db.Schema.RestActionsTable.Cols.vertical_order + " " + sort_direction_str
        )
        journal_db_te = db_cursor_result.fetchone()
        return RestActionsM(*journal_db_te)

    @staticmethod
    def _get_highest_or_lowest_sort_value(i_min_or_max: MinOrMaxEnum) -> int:
        db_cursor_result = db_exec(
            "SELECT " + i_min_or_max.value
            + " (" + mc.db.Schema.RestActionsTable.Cols.vertical_order + ")"
            + " FROM " + mc.db.Schema.RestActionsTable.name
        )
        return_value_int = db_cursor_result.fetchone()[0]
        # -0 has to be added here even though there can only be one value

        if return_value_int is None:
            # -to prevent error when the tables are empty
            return 0
        return return_value_int


class SettingsM:
    # noinspection PyUnusedLocal
    def __init__(
        self,
        i_id: int,  # unused
        i_rest_reminder_active: int,
        i_rest_reminder_interval: int,
        i_rest_reminder_audio_path: str,
        i_rest_reminder_volume: int,
        i_rest_reminder_notification_type: int,
        i_breathing_reminder_active: int,
        i_breathing_reminder_interval: int,
        i_breathing_reminder_audio_path: str,
        i_breathing_reminder_volume: int,
        i_breathing_reminder_notification_type: int,
        i_breathing_reminder_phrase_setup: int,
        i_breathing_reminder_nr_before_dialog: int,
        i_breathing_reminder_dialog_audio_active: int
    ) -> None:
        self.rest_reminder_active_bool = True if i_rest_reminder_active else False
        self.rest_reminder_interval_int = i_rest_reminder_interval
        self.rest_reminder_audio_path_str = i_rest_reminder_audio_path
        self.rest_reminder_volume_int = i_rest_reminder_volume
        self.rest_reminder_notification_type_int = i_rest_reminder_notification_type
        self.breathing_reminder_active_bool = True if i_breathing_reminder_active else False
        self.breathing_reminder_interval_int = i_breathing_reminder_interval
        self.breathing_reminder_audio_path_str = i_breathing_reminder_audio_path
        self.breathing_reminder_volume_int = i_breathing_reminder_volume
        self.breathing_reminder_notification_type_int = i_breathing_reminder_notification_type
        self.breathing_reminder_phrase_setup_int = i_breathing_reminder_phrase_setup
        self.breathing_reminder_nr_before_dialog_int = i_breathing_reminder_nr_before_dialog
        self.breathing_reminder_dialog_audio_active_bool = True if i_breathing_reminder_dialog_audio_active else False

    @property
    def rest_reminder_active(self) -> bool:
        return self.rest_reminder_active_bool

    @rest_reminder_active.setter
    def rest_reminder_active(self, i_new_is_active: bool):
        new_is_active_as_int = db.SQLITE_TRUE_INT if i_new_is_active else db.SQLITE_FALSE_INT
        self._update(
            db.Schema.SettingsTable.Cols.rest_reminder_active,
            new_is_active_as_int
        )

    @property
    def rest_reminder_interval(self) -> int:
        return self.rest_reminder_interval_int

    @rest_reminder_interval.setter
    def rest_reminder_interval(self, i_new_interval: int):
        self.rest_reminder_interval = i_new_interval
        self._update(
            db.Schema.SettingsTable.Cols.rest_reminder_interval,
            i_new_interval
        )

    @property
    def rest_reminder_audio_path(self) -> str:
        return self.rest_reminder_audio_path

    @rest_reminder_audio_path.setter
    def rest_reminder_audio_path(self, i_new_path: str):
        self.rest_reminder_audio_path_str = i_new_path
        self._update(
            db.Schema.SettingsTable.Cols.rest_reminder_audio_path,
            i_new_path
        )

    @property
    def rest_reminder_volume(self) -> int:
        return self.rest_reminder_volume_int

    @rest_reminder_volume.setter
    def rest_reminder_volume(self, i_new_volume: int):
        self.rest_reminder_volume_int = i_new_volume
        self._update(
            db.Schema.SettingsTable.Cols.rest_reminder_volume,
            i_new_volume
        )

    # rest_reminder_notification_type_int

    @property
    def rest_reminder_notification_type(self) -> mc.mc_global.NotificationType:
        ret_notification_type = mc.mc_global.NotificationType(self.rest_reminder_notification_type_int)
        return ret_notification_type

    @rest_reminder_notification_type.setter
    def rest_reminder_notification_type(
        self,
        i_new_notification_type: mc.mc_global.NotificationType
    ):
        self.rest_reminder_notification_type_int = i_new_notification_type.value
        self._update(
            db.Schema.SettingsTable.Cols.rest_reminder_notification_type,
            i_new_notification_type.value
        )

    @staticmethod
    def _update(i_col_name: str, i_new_value: typing.Any):
        db_exec(
            "UPDATE " + db.Schema.SettingsTable.name
            + " SET " + i_col_name + " = ?"
            + " WHERE " + db.Schema.SettingsTable.Cols.id + " = ?",
            (i_new_value, str(db.SINGLE_SETTINGS_ID_INT))
        )

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
    def update_rest_reminder_audio_path(i_new_audio_path: str):
        SettingsM._update(
            db.Schema.SettingsTable.Cols.rest_reminder_audio_path,
            i_new_audio_path
        )

    @staticmethod
    def update_breathing_dialog_audio_active(i_audio_active: bool):
        new_value_bool_as_int = db.SQLITE_TRUE_INT if i_audio_active else db.SQLITE_FALSE_INT
        SettingsM._update(
            db.Schema.SettingsTable.Cols.breathing_reminder_dialog_audio_active,
            new_value_bool_as_int
        )

    @staticmethod
    def update_rest_reminder_volume(i_new_volume: int):
        SettingsM._update(
            db.Schema.SettingsTable.Cols.rest_reminder_volume,
            i_new_volume
        )

    @staticmethod
    def update_rest_reminder_notification_type(i_new_notification_type: int):
        SettingsM._update(
            db.Schema.SettingsTable.Cols.rest_reminder_notification_type,
            i_new_notification_type
        )

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
        logging.debug("result=" + str(SettingsM.get().rest_reminder_active))

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
    def update_breathing_reminder_nr_per_dialog(i_new_nr_per_dialog: int):
        SettingsM._update(
            db.Schema.SettingsTable.Cols.breathing_reminder_nr_before_dialog,
            i_new_nr_per_dialog
        )

    @staticmethod
    def _update(i_col_name: str, i_new_value):
        db_exec(
            "UPDATE " + db.Schema.SettingsTable.name
            + " SET " + i_col_name + " = ?"
            + " WHERE " + db.Schema.PhrasesTable.Cols.id + " = ?",
            (i_new_value, str(db.SINGLE_SETTINGS_ID_INT))
        )

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
    # csv_writer.writeheader()
    csv_writer.writerow(("",))
    csv_writer.writerow(("===== Breathing Phrases =====",))
    for phrase in PhrasesM.get_all():
        csv_writer.writerow((phrase.title, phrase.ib, phrase.ob, phrase.ib_short, phrase.ob_short))
    csv_writer.writerow(("",))
    csv_writer.writerow(("===== Rest Actions =====",))
    for rest_action in RestActionsM.get_all():
        csv_writer.writerow((rest_action.title,))


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


def get_app_systray_icon_path() -> str:
    icon_file_name_str = "icon.png"
    settings = SettingsM.get()
    b_active = breathing_reminder_active()
    if b_active and settings.rest_reminder_active:
        icon_file_name_str = "icon-br.png"
    elif b_active:
        icon_file_name_str = "icon-b.png"
    elif settings.rest_reminder_active:
        icon_file_name_str = "icon-r.png"

    ret_icon_path_str = os.path.join(mc.mc_global.get_base_dir(), mc.mc_global.ICONS_DIR_STR, icon_file_name_str)
    return ret_icon_path_str
