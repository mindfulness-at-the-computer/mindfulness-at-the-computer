
import datetime
import shutil
import sqlite3

from mc import mc_global
from mc import model

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
        "CREATE TABLE " + Schema.PhrasesTable.name + "("
        + Schema.PhrasesTable.Cols.id + " INTEGER PRIMARY KEY, "
        + Schema.PhrasesTable.Cols.title + " TEXT NOT NULL, "
        + Schema.PhrasesTable.Cols.ib_phrase + " TEXT NOT NULL, "
        + Schema.PhrasesTable.Cols.ob_phrase + " TEXT NOT NULL"
        + ")"
    )

    i_db_conn.execute(
        "CREATE TABLE " + Schema.RestActionsTable.name + "("
        + Schema.RestActionsTable.Cols.id + " INTEGER PRIMARY KEY, "
        + Schema.RestActionsTable.Cols.title + " TEXT NOT NULL, "
        + Schema.RestActionsTable.Cols.image_path + " TEXT NOT NULL"
        + ")"
    )

    i_db_conn.execute(
        "CREATE TABLE " + Schema.SettingsTable.name + "("
        + Schema.SettingsTable.Cols.id + " INTEGER PRIMARY KEY, "
        + Schema.SettingsTable.Cols.rest_reminder_active + " INTEGER NOT NULL"
        + " DEFAULT " + str(SQLITE_TRUE_INT) + ", "
        + Schema.SettingsTable.Cols.rest_reminder_interval + " INTEGER NOT NULL"
        + " DEFAULT " + str(DEFAULT_REST_REMINDER_INTERVAL_MINUTES_INT) + ", "
        + Schema.SettingsTable.Cols.breathing_reminder_active + " INTEGER NOT NULL"
        + " DEFAULT " + str(SQLITE_TRUE_INT) + ", "
        + Schema.SettingsTable.Cols.breathing_reminder_interval + " INTEGER NOT NULL"
        + " DEFAULT " + str(DEFAULT_BREATHING_REMINDER_INTERVAL_SECONDS_INT) + ", "
        + Schema.SettingsTable.Cols.breathing_reminder_length + " INTEGER NOT NULL"
        + " DEFAULT " + str(DEFAULT_BREATHING_REMINDER_LENGTH_SECONDS_INT)
        + ")"
    )

    db_connection = Helper.get_db_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        "INSERT OR IGNORE INTO " + Schema.SettingsTable.name + "("
        + Schema.SettingsTable.Cols.id
        + ") VALUES (?)", (SINGLE_SETTINGS_ID_INT,)
    )
    # -please note "OR IGNORE"
    db_connection.commit()

    if mc_global.testing_bool:
        model.populate_db_with_test_data()

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


class Helper(object):
    __db_connection = None  # "Static"

    # noinspection PyTypeChecker
    @staticmethod
    def get_db_connection():
        if Helper.__db_connection is None:
            Helper.__db_connection = sqlite3.connect(mc_global.get_database_filename())

            # Upgrading the database
            # Very good upgrade explanation:
            # http://stackoverflow.com/questions/19331550/database-change-with-software-update
            # More info here: https://www.sqlite.org/pragma.html#pragma_schema_version
            current_db_ver_it = get_schema_version(Helper.__db_connection)
            target_db_ver_it = max(upgrade_steps)
            for upgrade_step_it in range(current_db_ver_it + 1, target_db_ver_it + 1):
                if upgrade_step_it in upgrade_steps:
                    upgrade_steps[upgrade_step_it](Helper.__db_connection)
                    set_schema_version(Helper.__db_connection, upgrade_step_it)
            Helper.__db_connection.commit()

            # TODO: Where do we close the db connection? (Do we need to close it?)
            # http://stackoverflow.com/questions/3850261/doing-something-before-program-exit

        return Helper.__db_connection


class Schema:

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

    class RestActionsTable:
        name = "rest_actions"

        class Cols:
            id = "id"
            title = "title"
            image_path = "image_path"
            # TODO: notes as well here?

    class SettingsTable:
        name = "settings"

        class Cols:
            id = "id"  # key
            rest_reminder_active = "rest_reminder_active"
            rest_reminder_interval = "rest_reminder_interval"
            breathing_reminder_active = "breathing_reminder_active"
            breathing_reminder_interval = "breathing_reminder_interval"
            breathing_reminder_length = "breathing_reminder_length"


def backup_db_file():
    date_sg = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_file_name_sg = mc_global.get_database_filename() + "_" + date_sg
    shutil.copyfile(mc_global.get_database_filename(), new_file_name_sg)



