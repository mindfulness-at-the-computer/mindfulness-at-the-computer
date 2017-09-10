
import csv

from mc import db


class PhrasesM:
    def __init__(self, i_id: int, i_title: str, i_ib: str, i_ob: str) -> None:
        self.id_int = i_id
        self.title_str = i_title
        self.ib_str = i_ib
        self.ob_str = i_ob

    @staticmethod
    def add(i_title: str, i_ib: str, i_ob: str) -> None:
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "INSERT INTO " + db.Schema.PhrasesTable.name + "("
            + db.Schema.PhrasesTable.Cols.title + ", "
            + db.Schema.PhrasesTable.Cols.ib_phrase + ", "
            + db.Schema.PhrasesTable.Cols.ob_phrase
            + ") VALUES (?, ?, ?)", (i_title, i_ib, i_ob)
        )
        db_connection.commit()

    @staticmethod
    def get(i_id: int):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + db.Schema.PhrasesTable.name
            + " WHERE " + db.Schema.PhrasesTable.Cols.id + "=" + str(i_id)
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
            + " WHERE " + db.Schema.PhrasesTable.Cols.id + "=" + str(i_id_int)
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


class RestActionsM:
    def __init__(self, i_id: int, i_title: str, i_image_path: str) -> None:
        self.id_int = i_id
        self.title_str = i_title
        self.image_path_str = i_image_path

    @staticmethod
    def add(i_title: str, i_image_path: str) -> None:
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "INSERT INTO " + db.Schema.RestActionsTable.name + "("
            + db.Schema.RestActionsTable.Cols.title + ", "
            + db.Schema.RestActionsTable.Cols.image_path
            + ") VALUES (?, ?)", (i_title, i_image_path)
        )
        db_connection.commit()

    @staticmethod
    def get(i_id: int):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + db.Schema.RestActionsTable.name
            + " WHERE " + db.Schema.RestActionsTable.Cols.id + "=" + str(i_id)
        )
        rest_action_db_te = db_cursor_result.fetchone()
        db_connection.commit()

        return RestActionsM(*rest_action_db_te)
        # -the asterisk (*) will "expand" the tuple into separate arguments for the function header

    @staticmethod
    def get_all():
        ret_reminder_list = []
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + db.Schema.RestActionsTable.name
        )
        rest_actions_db_te_list = db_cursor_result.fetchall()
        for rest_action_db_te in rest_actions_db_te_list:
            ret_reminder_list.append(RestActionsM(*rest_action_db_te))
        db_connection.commit()
        return ret_reminder_list

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
        self.rest_reminder_active_bool = True if i_rest_reminder_active else False
        self.rest_reminder_interval_int = i_rest_reminder_interval
        self.breathing_reminder_active_bool = True if i_breathing_reminder_active else False
        self.breathing_reminder_interval_int = i_breathing_reminder_interval
        self.breathing_reminder_length_int = i_breathing_reminder_length

    @staticmethod
    def get():
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + db.Schema.SettingsTable.name
            + " WHERE " + db.Schema.SettingsTable.Cols.id + "=" + str(db.SINGLE_SETTINGS_ID_INT)
        )
        reminder_db_te = db_cursor_result.fetchone()
        db_connection.commit()

        return SettingsM(*reminder_db_te)
        # -the asterisk (*) will "expand" the tuple into separate arguments for the function header

    @staticmethod
    def update_rest_reminder_active(i_reminder_active: bool):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + db.Schema.SettingsTable.name
            + " SET " + db.Schema.SettingsTable.Cols.rest_reminder_active + " = ?"
            + " WHERE " + db.Schema.SettingsTable.Cols.id + " = ?",
            (db.SQLITE_TRUE_INT if i_reminder_active else db.SQLITE_FALSE_INT, db.SINGLE_SETTINGS_ID_INT)
        )
        db_connection.commit()

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
    def update_breathing_reminder_length(i_reminder_length: int):
        db_connection = db.Helper.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + db.Schema.SettingsTable.name
            + " SET " + db.Schema.SettingsTable.Cols.breathing_reminder_length + " = ?"
            + " WHERE " + db.Schema.SettingsTable.Cols.id + " = ?",
            (str(i_reminder_length), db.SINGLE_SETTINGS_ID_INT)
        )
        db_connection.commit()


def export_all():
    csv_writer = csv.writer(open("user-files/exported.csv", "w"))
    for phrase in PhrasesM.get_all():
        # time_datetime = datetime.date.fromtimestamp(phrase.date_added_it)
        # date_str = time_datetime.strftime("%Y-%m-%d")
        csv_writer.writerow((phrase.title_str, phrase.ib_str, phrase.ob_str))


def populate_db_with_setup_data():
    PhrasesM.add(
        "In, out",
        "Breathing in, I know I am breathing in",
        "Breathing out, I know I am breathing out",
    )
    PhrasesM.add(
        "Happy, safe",
        "Breathing in, may I be peaceful, happy, and safe",
        "Breathing out, may I be free from fear, hatred, and delusion",
    )
    PhrasesM.add(
        "Aware of Body",
        "Aware of my body, I breathe in",
        "Aware of my body, I breathe out",
    )
    PhrasesM.add(
        "Aware of painful feeling",
        "Breathing in, I am aware of a painful feeling in my body",
        "Breathing out, I am aware of a painful feeling in my body",
    )
    PhrasesM.add(
        "Caring for Body",
        "Breathing in, I care for my body",
        "Breathing out, I relax my body",
    )
    PhrasesM.add(
        "Confidence, peace",
        "Breathing in confidence",
        "Breathing out peace",
    )

    RestActionsM.add(
        "Making a cup of tea",
        "user_files/images/tea.png"
    )
    RestActionsM.add(
        "Movement exercise with the arms",
        "user_files/images/stones.png"
    )
    RestActionsM.add(
        "Going outside",
        ""
    )
    RestActionsM.add(
        "Slow Mindful walking",
        ""
    )
    RestActionsM.add(
        "Opening a window",
        ""
    )
    RestActionsM.add(
        "Eating a healthy snack",
        ""
    )
    RestActionsM.add(
        "sitting meditation",
        ""
    )
    RestActionsM.add(
        "watering the plants",
        ""
    )
    RestActionsM.add(
        "taking a walk outside",
        ""
    )
    RestActionsM.add(
        "mindful slow walking inside",
        ""
    )
    RestActionsM.add(
        "opening the window",
        ""
    )
    RestActionsM.add(
        "letting in some fresh air",
        ""
    )


    """
    movement_qpb = QtWidgets.QPushButton("Movement exercise")
    rest_kindness_alternatives_qbb.addButton(movement_qpb, QtWidgets.QDialogButtonBox.YesRole)
    walk_qpb = QtWidgets.QPushButton("Taking a walk")
    rest_kindness_alternatives_qbb.addButton(walk_qpb, QtWidgets.QDialogButtonBox.YesRole)
    """


def populate_db_with_test_data():
    populate_db_with_setup_data()

    """
    PhrasesM.add(
        "Test - In, out",
        "Breathing in, i know i am breathing in",
        "Breathing out, i know i am breathing out",
    )
    PhrasesM.add(
        "Test - Happy, safe",
        "Breathing in, may i be peaceful, happy, and safe",
        "Breathing out, may i be free from fear, hatred, and delusion",
    )
    PhrasesM.add(
        "Test - Aware of Body",
        "Aware of my body, i breathe in",
        "Aware of my feelings, i breathe out",
    )
    PhrasesM.add(
        "Test - Caring for Body",
        "Breathing in, i care for my body",
        "Breathing out, i care for my body",
    )
    PhrasesM.add(
        "Test - Aware of painful feeling",
        "Breathing in, i am aware of a painful feeling",
        "Breathing out, i am aware of a painful feeling",
    )
    """



