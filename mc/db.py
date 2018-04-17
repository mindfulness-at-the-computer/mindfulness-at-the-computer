import datetime
import shutil
import sqlite3
import logging
from mc import mc_global
from mc import model

SQLITE_FALSE_INT = 0
SQLITE_TRUE_INT = 1
SQLITE_NULL_STR = "NULL"
NO_REFERENCE_INT = -1
NO_REST_REMINDER_INT = -1
NO_BREATHING_REMINDER_INT = -1
DEFAULT_REST_REMINDER_INTERVAL_MINUTES_INT = 30
DEFAULT_BREATHING_REMINDER_INTERVAL_MINUTES_INT = 5
SINGLE_SETTINGS_ID_INT = 0
DEFAULT_VOLUME_INT = 50
DEFAULT_BREATHING_REMINDER_NR_BEFORE_DIALOG_INT = 3


def get_schema_version(i_db_conn: sqlite3.Connection) -> int:
    t_cursor = i_db_conn.execute("PRAGMA user_version")
    return t_cursor.fetchone()[0]


def set_schema_version(i_db_conn, i_version_it: sqlite3.Connection) -> None:
    i_db_conn.execute("PRAGMA user_version={:d}".format(i_version_it))


def initial_schema_and_setup(i_db_conn: sqlite3.Connection) -> None:
    # Auto-increment is not needed in our case: https://www.sqlite.org/autoinc.html

    i_db_conn.execute(
        "CREATE TABLE " + Schema.PhrasesTable.name + "("
        + Schema.PhrasesTable.Cols.id + " INTEGER PRIMARY KEY, "
        + Schema.PhrasesTable.Cols.vertical_order + " INTEGER NOT NULL, "
        + Schema.PhrasesTable.Cols.title + " TEXT NOT NULL, "
        + Schema.PhrasesTable.Cols.ib_phrase + " TEXT NOT NULL, "
        + Schema.PhrasesTable.Cols.ob_phrase + " TEXT NOT NULL, "
        + Schema.PhrasesTable.Cols.ib_short_phrase + " TEXT NOT NULL DEFAULT '', "
        + Schema.PhrasesTable.Cols.ob_short_phrase + " TEXT NOT NULL DEFAULT '', "
        + Schema.PhrasesTable.Cols.type + " INTEGER NOT NULL"
        + " DEFAULT " + str(mc_global.BreathingPhraseType.in_out.value)
        + ")"
    )

    i_db_conn.execute(
        "CREATE TABLE " + Schema.RestActionsTable.name + "("
        + Schema.RestActionsTable.Cols.id + " INTEGER PRIMARY KEY, "
        + Schema.RestActionsTable.Cols.vertical_order + " INTEGER NOT NULL, "
        + Schema.RestActionsTable.Cols.title + " TEXT NOT NULL"
        + ")"
    )

    i_db_conn.execute(
        "CREATE TABLE " + Schema.SettingsTable.name + "("
        + Schema.SettingsTable.Cols.id + " INTEGER PRIMARY KEY, "
        + Schema.SettingsTable.Cols.rest_reminder_active + " INTEGER NOT NULL"
        + " DEFAULT " + str(SQLITE_TRUE_INT) + ", "
        + Schema.SettingsTable.Cols.rest_reminder_interval + " INTEGER NOT NULL"
        + " DEFAULT " + str(DEFAULT_REST_REMINDER_INTERVAL_MINUTES_INT) + ", "
        + Schema.SettingsTable.Cols.rest_reminder_audio_filename + " TEXT NOT NULL"
        + " DEFAULT '" + mc_global.WIND_CHIMES_FILENAME_STR + "'" + ", "
        + Schema.SettingsTable.Cols.rest_reminder_volume + " INTEGER NOT NULL"
        + " DEFAULT " + str(DEFAULT_VOLUME_INT) + ", "
        + Schema.SettingsTable.Cols.rest_reminder_notification_type + " INTEGER NOT NULL"
        + " DEFAULT " + str(mc_global.NotificationType.Both.value) + ", "
        + Schema.SettingsTable.Cols.breathing_reminder_active + " INTEGER NOT NULL"
        + " DEFAULT " + str(SQLITE_TRUE_INT) + ", "
        + Schema.SettingsTable.Cols.breathing_reminder_interval + " INTEGER NOT NULL"
        + " DEFAULT " + str(DEFAULT_BREATHING_REMINDER_INTERVAL_MINUTES_INT) + ", "
        + Schema.SettingsTable.Cols.breathing_reminder_audio_filename + " TEXT NOT NULL"
        + " DEFAULT '" + mc_global.SMALL_BELL_SHORT_FILENAME_STR + "'" + ", "
        + Schema.SettingsTable.Cols.breathing_reminder_volume + " INTEGER NOT NULL"
        + " DEFAULT " + str(DEFAULT_VOLUME_INT) + ", "
        + Schema.SettingsTable.Cols.breathing_reminder_notification_type + " INTEGER NOT NULL"
        + " DEFAULT " + str(mc_global.NotificationType.Both.value) + ", "
        + Schema.SettingsTable.Cols.breathing_reminder_phrase_setup + " INTEGER NOT NULL"
        + " DEFAULT " + str(mc_global.PhraseSetup.Long.value) + ", "
        + Schema.SettingsTable.Cols.breathing_reminder_nr_before_dialog + " INTEGER NOT NULL"
        + " DEFAULT " + str(DEFAULT_BREATHING_REMINDER_NR_BEFORE_DIALOG_INT) + ", "
        + Schema.SettingsTable.Cols.breathing_reminder_dialog_audio_active + " INTEGER NOT NULL"
        + " DEFAULT " + str(SQLITE_TRUE_INT) + ", "
        + Schema.SettingsTable.Cols.breathing_reminder_dialog_close_on_hover + " INTEGER NOT NULL"
        + " DEFAULT " + str(SQLITE_FALSE_INT) + ", "
        + Schema.SettingsTable.Cols.breathing_reminder_text + " TEXT NOT NULL"
        + " DEFAULT ''" + ", "
        + Schema.SettingsTable.Cols.breathing_dialog_phrase_selection + " INTEGER NOT NULL"
        + " DEFAULT " + str(mc_global.PhraseSelection.same.value) + ", "
        + Schema.SettingsTable.Cols.prep_reminder_audio_filename + " TEXT NOT NULL"
        + " DEFAULT '" + mc_global.SMALL_BELL_LONG_FILENAME_STR + "'" + ", "
        + Schema.SettingsTable.Cols.prep_reminder_audio_volume + " INTEGER NOT NULL"
        + " DEFAULT " + str(DEFAULT_VOLUME_INT) + ", "
        + Schema.SettingsTable.Cols.run_on_startup + " INTEGER NOT NULL"
        + " DEFAULT " + str(SQLITE_FALSE_INT)
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
    22: initial_schema_and_setup,
}


class Helper(object):
    __db_connection = None  # "Static"

    # noinspection PyTypeChecker
    @staticmethod
    def get_db_connection() -> sqlite3.Connection:

        if Helper.__db_connection is None:
            Helper.__db_connection = sqlite3.connect(mc_global.get_database_filename())

            # Upgrading the database
            # Very good upgrade explanation:
            # http://stackoverflow.com/questions/19331550/database-change-with-software-update
            # More info here: https://www.sqlite.org/pragma.html#pragma_schema_version
            current_db_ver_it = get_schema_version(Helper.__db_connection)
            target_db_ver_it = max(upgrade_steps)
            database_tables_dropped_bool = False
            if current_db_ver_it < min(upgrade_steps) and mc_global.db_file_exists_at_application_startup_bl:
                database_tables_dropped_bool = True
                backup_db_file()
                mc_global.db_upgrade_message_str = (
                    "Database upgraded, all user entries have been removed. "
                    "The old db has been backed up, and is available in the user_files directory. "
                )
                try:
                    model.export_all()
                    # -please note that there is a high likelihood that this fails, the reason is that the tables
                    #  have now been changed
                    mc_global.db_upgrade_message_str += (
                        "Some of the old db contents has also been exported to a text file "
                        "that you can find here: /user_files/exported.csv"
                    )
                except:
                    pass
                Helper.drop_all_db_tables(Helper.__db_connection)
            for upgrade_step_nr_int in range(current_db_ver_it + 1, target_db_ver_it + 1):
                if upgrade_step_nr_int in upgrade_steps:
                    upgrade_steps[upgrade_step_nr_int](Helper.__db_connection)
                    set_schema_version(Helper.__db_connection, upgrade_step_nr_int)

            if mc_global.testing_bool:
                model.populate_db_with_test_data()
            else:
                if database_tables_dropped_bool:
                    model.populate_db_with_setup_data()
                elif not mc_global.db_file_exists_at_application_startup_bl:
                    model.populate_db_with_setup_data()
                else:
                    pass  # -default, the user has started the application before and is not testing

            # TODO: Where do we close the db connection? (Do we need to close it?)
            # http://stackoverflow.com/questions/3850261/doing-something-before-program-exit

        return Helper.__db_connection

    @staticmethod
    def drop_all_db_tables(i_db_conn: sqlite3.Connection) -> None:
        Helper.drop_db_table(i_db_conn, Schema.PhrasesTable.name)
        Helper.drop_db_table(i_db_conn, Schema.RestActionsTable.name)
        Helper.drop_db_table(i_db_conn, Schema.SettingsTable.name)

    @staticmethod
    def drop_db_table(i_db_conn, i_table_name: sqlite3.Connection) -> None:
        i_db_conn.execute("DROP TABLE IF EXISTS " + i_table_name)

    @staticmethod
    def close_db():
        if Helper.__db_connection is not None:
            Helper.__db_connection.close()
            Helper.__db_connection = None
            logging.debug("Database closed")


class Schema:

    class PhrasesTable:
        name = "phrases"

        class Cols:
            id = "id"  # key
            vertical_order = "vertical_order"
            title = "title"
            ib_phrase = "ib_phrase"
            ob_phrase = "ob_phrase"
            ib_short_phrase = "ib_short_phrase"
            ob_short_phrase = "ob_short_phrase"
            type = "type"

    class RestActionsTable:
        name = "rest_actions"

        class Cols:
            id = "id"
            vertical_order = "vertical_order"
            title = "title"

    class SettingsTable:
        name = "settings"

        class Cols:
            id = "id"  # key
            rest_reminder_active = "rest_reminder_active"
            rest_reminder_interval = "rest_reminder_interval"
            rest_reminder_audio_filename = "rest_reminder_audio_filename"
            rest_reminder_volume = "rest_reminder_volume"
            rest_reminder_notification_type = "rest_reminder_notification_type"
            breathing_reminder_active = "breathing_reminder_active"
            breathing_reminder_interval = "breathing_reminder_interval"
            breathing_reminder_audio_filename = "breathing_reminder_audio_filename"
            breathing_reminder_volume = "breathing_reminder_volume"
            breathing_reminder_notification_type = "breathing_reminder_notification_type"
            breathing_reminder_phrase_setup = "breathing_reminder_phrase_setup"
            breathing_reminder_nr_before_dialog = "breathing_reminder_nr_before_dialog"
            breathing_reminder_dialog_audio_active = "breathing_reminder_dialog_audio_active"
            breathing_reminder_dialog_close_on_hover = "breathing_reminder_dialog_close_on_hover"
            breathing_reminder_text = "breathing_reminder_text"
            breathing_dialog_phrase_selection = "breathing_dialog_phrase_selection"
            prep_reminder_audio_filename = "prep_reminder_audio_filename"
            prep_reminder_audio_volume = "prep_reminder_audio_volume"
            run_on_startup = "run_on_startup"


def backup_db_file() -> None:
    if mc_global.testing_bool:
        return
    date_sg = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_file_name_sg = mc_global.get_database_filename(date_sg)
    shutil.copyfile(mc_global.get_database_filename(), new_file_name_sg)
