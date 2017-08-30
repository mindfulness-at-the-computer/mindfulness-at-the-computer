import csv
import datetime
import shutil
import sqlite3
import enum
import mb_global

SQLITE_FALSE_INT = 0
SQLITE_TRUE_INT = 1
SQLITE_NULL_STR = "NULL"
NO_REFERENCE_INT = -1
NO_REST_REMINDER_INT = -1
NO_BREATHING_REMINDER_INT = -1
DEFAULT_REST_REMINDER_INTERVAL_MINUTES_INT = 1
DEFAULT_BREATHING_REMINDER_INTERVAL_SECONDS_INT = 30
DEFAULT_BREATHING_REMINDER_LENGTH_SECONDS_INT = 10
SINGLE_SETTINGS_ID_INT = 0


def get_schema_version(i_db_conn):
    t_cursor = i_db_conn.execute("PRAGMA user_version")
    return t_cursor.fetchone()[0]


def set_schema_version(i_db_conn, i_version_it):
    i_db_conn.execute("PRAGMA user_version={:d}".format(i_version_it))


def initial_schema_and_setup(i_db_conn):
    """Auto-increment is not needed in our case: https://www.sqlite.org/autoinc.html
    """

    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.PhrasesTable.name + "("
        + DbSchemaM.PhrasesTable.Cols.id + " INTEGER PRIMARY KEY, "
        + DbSchemaM.PhrasesTable.Cols.title + " TEXT NOT NULL, "
        + DbSchemaM.PhrasesTable.Cols.ib_phrase + " TEXT NOT NULL, "
        + DbSchemaM.PhrasesTable.Cols.ob_phrase + " TEXT NOT NULL"
        + ")"
    )

    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.SettingsTable.name + "("
        + DbSchemaM.SettingsTable.Cols.id + " INTEGER PRIMARY KEY, "
        + DbSchemaM.SettingsTable.Cols.rest_reminder_active + " INTEGER NOT NULL"
        + " DEFAULT " + str(SQLITE_TRUE_INT) + ", "
        + DbSchemaM.SettingsTable.Cols.rest_reminder_interval + " INTEGER NOT NULL"
        + " DEFAULT " + str(DEFAULT_REST_REMINDER_INTERVAL_MINUTES_INT) + ", "
        + DbSchemaM.SettingsTable.Cols.breathing_reminder_active + " INTEGER NOT NULL"
        + " DEFAULT " + str(SQLITE_TRUE_INT) + ", "
        + DbSchemaM.SettingsTable.Cols.breathing_reminder_interval + " INTEGER NOT NULL"
        + " DEFAULT " + str(DEFAULT_BREATHING_REMINDER_INTERVAL_SECONDS_INT) + ", "
        + DbSchemaM.SettingsTable.Cols.breathing_reminder_length + " INTEGER NOT NULL"
        + " DEFAULT " + str(DEFAULT_BREATHING_REMINDER_LENGTH_SECONDS_INT)
        + ")"
    )

    db_connection = DbHelperM.get_db_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        "INSERT OR IGNORE INTO " + DbSchemaM.SettingsTable.name + "("
        + DbSchemaM.SettingsTable.Cols.id
        + ") VALUES (?)", (SINGLE_SETTINGS_ID_INT,)
    )
    # -please note "OR IGNORE"
    db_connection.commit()

    if mb_global.testing_bool:
        populate_db_with_test_data()

"""
Example of db upgrade code:
def upgrade_1_2(i_db_conn):
    backup_db_file()
    i_db_conn.execute(
        "ALTER TABLE " + DbSchemaM.ObservancesTable.name + " ADD COLUMN "
        + DbSchemaM.ObservancesTable.Cols.user_text + " TEXT DEFAULT ''"
    )
"""

upgrade_steps = {
    1: initial_schema_and_setup,
}


class DbHelperM(object):
    __db_connection = None  # "Static"

    # noinspection PyTypeChecker
    @staticmethod
    def get_db_connection():
        if DbHelperM.__db_connection is None:
            DbHelperM.__db_connection = sqlite3.connect(mb_global.get_database_filename())

            # Upgrading the database
            # Very good upgrade explanation:
            # http://stackoverflow.com/questions/19331550/database-change-with-software-update
            # More info here: https://www.sqlite.org/pragma.html#pragma_schema_version
            current_db_ver_it = get_schema_version(DbHelperM.__db_connection)
            target_db_ver_it = max(upgrade_steps)
            for upgrade_step_it in range(current_db_ver_it + 1, target_db_ver_it + 1):
                if upgrade_step_it in upgrade_steps:
                    upgrade_steps[upgrade_step_it](DbHelperM.__db_connection)
                    set_schema_version(DbHelperM.__db_connection, upgrade_step_it)
            DbHelperM.__db_connection.commit()

            # TODO: Where do we close the db connection? (Do we need to close it?)
            # http://stackoverflow.com/questions/3850261/doing-something-before-program-exit

        return DbHelperM.__db_connection


class DbSchemaM:

    class PhrasesTable:
        name = "phrases"

        class Cols:
            id = "id"  # key
            title = "title"
            ib_phrase = "ib_phrase"
            ob_phrase = "ob_phrase"
            # vertical_order = "vertical_order"
            # ib_short_phrase = "ib_short_phrase"
            # ob_short_phrase = "ob_short_phrase"

    class SettingsTable:
        name = "settings"

        class Cols:
            id = "id"  # key
            rest_reminder_active = "rest_reminder_active"
            rest_reminder_interval = "rest_reminder_interval"
            breathing_reminder_active = "breathing_reminder_active"
            breathing_reminder_interval = "breathing_reminder_interval"
            breathing_reminder_length = "breathing_reminder_length"


class PhrasesM:
    def __init__(self, i_id: int, i_title: str, i_ib: str, i_ob: str) -> None:
        self.id_int = i_id
        self.title_str = i_title
        self.ib_str = i_ib
        self.ob_str = i_ob

    @staticmethod
    def add(i_title: str, i_ib: str, i_ob: str) -> None:
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "INSERT INTO " + DbSchemaM.PhrasesTable.name + "("
            + DbSchemaM.PhrasesTable.Cols.title + ", "
            + DbSchemaM.PhrasesTable.Cols.ib_phrase + ", "
            + DbSchemaM.PhrasesTable.Cols.ob_phrase
            + ") VALUES (?, ?, ?)", (i_title, i_ib, i_ob)
        )
        db_connection.commit()

    @staticmethod
    def get(i_id: int):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.PhrasesTable.name
            + " WHERE " + DbSchemaM.PhrasesTable.Cols.id + "=" + str(i_id)
        )
        reminder_db_te = db_cursor_result.fetchone()
        db_connection.commit()

        return PhrasesM(*reminder_db_te)
        # -the asterisk (*) will "expand" the tuple into separate arguments for the function header

    @staticmethod
    def get_all():
        ret_reminder_list = []
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.PhrasesTable.name
        )
        phrases_db_te_list = db_cursor_result.fetchall()
        for phrases_db_te in phrases_db_te_list:
            ret_reminder_list.append(PhrasesM(*phrases_db_te))
        db_connection.commit()
        return ret_reminder_list

    @staticmethod
    def remove(i_id_int):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "DELETE FROM " + DbSchemaM.PhrasesTable.name
            + " WHERE " + DbSchemaM.PhrasesTable.Cols.id + "=" + str(i_id_int)
        )
        db_connection.commit()

    @staticmethod
    def update_title(i_id: int, i_new_title: str):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.PhrasesTable.name
            + " SET " + DbSchemaM.PhrasesTable.Cols.title + " = ?"
            + " WHERE " + DbSchemaM.PhrasesTable.Cols.id + " = ?",
            (i_new_title, str(i_id))
        )
        db_connection.commit()

    @staticmethod
    def update_in_breath(i_id: int, i_new_in_breath: str):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.PhrasesTable.name
            + " SET " + DbSchemaM.PhrasesTable.Cols.ib_phrase + " = ?"
            + " WHERE " + DbSchemaM.PhrasesTable.Cols.id + " = ?",
            (i_new_in_breath, str(i_id))
        )
        db_connection.commit()

    @staticmethod
    def update_out_breath(i_id: int, i_new_out_breath: str):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.PhrasesTable.name
            + " SET " + DbSchemaM.PhrasesTable.Cols.ob_phrase + " = ?"
            + " WHERE " + DbSchemaM.PhrasesTable.Cols.id + " = ?",
            (i_new_out_breath, str(i_id))
        )
        db_connection.commit()


class SettingsM:
    def __init__(
        self,
        i_id: int,
        i_rest_reminder_active: int,
        i_rest_reminder_interval: int,
        i_breathing_reminder_active: int,
        i_breathing_reminder_interval: int,
        i_breathing_reminder_length: int
    ) -> None:
        # (id is not used)
        self.rest_reminder_active_bool = SQLITE_TRUE_INT if i_rest_reminder_active else SQLITE_FALSE_INT
        self.rest_reminder_interval_int = i_rest_reminder_interval
        self.breathing_reminder_active_bool = SQLITE_TRUE_INT if i_breathing_reminder_active else SQLITE_FALSE_INT
        self.breathing_reminder_interval_int = i_breathing_reminder_interval
        self.breathing_reminder_length_int = i_breathing_reminder_length

    @staticmethod
    def get():
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.SettingsTable.name
            + " WHERE " + DbSchemaM.SettingsTable.Cols.id + "=" + str(SINGLE_SETTINGS_ID_INT)
        )
        reminder_db_te = db_cursor_result.fetchone()
        db_connection.commit()

        return SettingsM(*reminder_db_te)
        # -the asterisk (*) will "expand" the tuple into separate arguments for the function header

    @staticmethod
    def update_rest_reminder_active(i_reminder_active: bool):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.SettingsTable.name
            + " SET " + DbSchemaM.SettingsTable.Cols.rest_reminder_active + " = ?"
            + " WHERE " + DbSchemaM.SettingsTable.Cols.id + " = ?",
            (SQLITE_TRUE_INT if i_reminder_active else SQLITE_FALSE_INT, SINGLE_SETTINGS_ID_INT)
        )
        db_connection.commit()

    @staticmethod
    def update_rest_reminder_interval(i_reminder_interval: int):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.SettingsTable.name
            + " SET " + DbSchemaM.SettingsTable.Cols.rest_reminder_interval + " = ?"
            + " WHERE " + DbSchemaM.SettingsTable.Cols.id + " = ?",
            (str(i_reminder_interval), SINGLE_SETTINGS_ID_INT)
        )
        db_connection.commit()

    @staticmethod
    def update_breathing_reminder_active(i_reminder_active: bool):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.SettingsTable.name
            + " SET " + DbSchemaM.SettingsTable.Cols.breathing_reminder_active + " = ?"
            + " WHERE " + DbSchemaM.SettingsTable.Cols.id + " = ?",
            (SQLITE_TRUE_INT if i_reminder_active else SQLITE_FALSE_INT, SINGLE_SETTINGS_ID_INT)
        )
        db_connection.commit()

    @staticmethod
    def update_breathing_reminder_interval(i_reminder_interval: int):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.SettingsTable.name
            + " SET " + DbSchemaM.SettingsTable.Cols.breathing_reminder_interval + " = ?"
            + " WHERE " + DbSchemaM.SettingsTable.Cols.id + " = ?",
            (str(i_reminder_interval), SINGLE_SETTINGS_ID_INT)
        )
        db_connection.commit()

    @staticmethod
    def update_breathing_reminder_length(i_reminder_length: int):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.SettingsTable.name
            + " SET " + DbSchemaM.SettingsTable.Cols.breathing_reminder_length + " = ?"
            + " WHERE " + DbSchemaM.SettingsTable.Cols.id + " = ?",
            (str(i_reminder_length), SINGLE_SETTINGS_ID_INT)
        )
        db_connection.commit()


def export_all():
    csv_writer = csv.writer(open("exported.csv", "w"))
    for phrase in PhrasesM.get_all():
        time_datetime = datetime.date.fromtimestamp(phrase.date_added_it)
        date_str = time_datetime.strftime("%Y-%m-%d")
        csv_writer.writerow((date_str, phrase.diary_text))


def backup_db_file():
    date_sg = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_file_name_sg = mb_global.get_database_filename() + "_" + date_sg
    shutil.copyfile(mb_global.get_database_filename(), new_file_name_sg)


def populate_db_with_test_data():

    PhrasesM.add(
        "In, out",
        "Breathing in, i know i am breathing in",
        "Breathing out, i know i am breathing out",
    )
    PhrasesM.add(
        "Happy, safe",
        "Breathing in, may i be peaceful, happy, and safe",
        "Breathing out, may i be free from fear, hatred, and delusion",
    )
    PhrasesM.add(
        "Aware of Body",
        "Aware of my body, i breathe in",
        "Aware of my feelings, i breathe out",
    )
    PhrasesM.add(
        "Caring for Body",
        "Breathing in, i care for my body",
        "Breathing out, i care for my body",
    )

    PhrasesM.add(
        "Aware of painful feeling",
        "Breathing in, i am aware of a painful feeling",
        "Breathing out, i am aware of a painful feeling",
    )

"""
class CollectionSetupEnum(enum.Enum):
    # -only used at setup
    breathing = 1  # _te
    breathing_with_mental_formations = 2
    awareness_of_body = 3
    self_compassion = 4
"""

