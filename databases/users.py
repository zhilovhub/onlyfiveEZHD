from database import *


class UserDataCommands(DataBase):
    def __init__(self, connection: CMySQLConnection) -> None:
        """Initialization"""
        super().__init__(connection)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(UserDataQueries.create_table_user_query)

        except Error as e:
            print(e)

    def get_user_first_and_last_name(self, user_id: int) -> tuple:
        """Returns user's first and last name"""
        with self.connection.cursor() as cursor:
            cursor.execute(UserDataQueries.get_user_first_and_last_name_query.format(user_id))
            first_name, last_name = cursor.fetchone()

            return first_name, last_name

    def insert_new_user(self, user_id: int, screen_name: str, first_name: str, last_name: str, is_ready: bool) -> None:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(UserDataQueries.insert_new_user_query.format(user_id, screen_name, first_name,
                                                                            last_name, is_ready))
            except Error as e:
                print(e, 123)

    def set_user_is_ready(self, user_id: int) -> None:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(UserDataQueries.set_user_is_ready_query.format(user_id))

        except Error as e:
            print(e)

    def check_user_is_ready(self, user_id: int) -> bool:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(UserDataQueries.check_user_is_ready_query.format(user_id))
                user = cursor.fetchone()
                return True if user else False

        except Error as e:
            print(e)

    def get_user_dialog_state(self, user_id: int) -> int:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(UserDataQueries.get_user_dialog_state_query.format(user_id))
                state = cursor.fetchone()[0]

                return state

        except Error as e:
            print(e)

    def set_user_dialog_state(self, user_id: int, state: int) -> None:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(UserDataQueries.set_user_dialog_state_query.format(state, user_id))

        except Error as e:
            print(e)


class UserDataQueries:
    create_table_user_query = """CREATE TABLE IF NOT EXISTS Users(
        user_id INT NOT NULL UNIQUE PRIMARY KEY,
        screen_name VARCHAR(255),
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        is_ready BOOLEAN,
        state INT
    )"""

    insert_new_user_query = """INSERT INTO Users VALUES({}, '{}', '{}', '{}', {}, 0)"""

    set_user_is_ready_query = """UPDATE Users SET is_ready=TRUE WHERE user_id={}"""

    check_user_is_ready_query = """SELECT * FROM Users WHERE user_id={} AND is_ready=TRUE"""

    get_user_dialog_state_query = """SELECT state FROM Users WHERE user_id={}"""

    get_user_first_and_last_name_query = """SELECT first_name, last_name FROM Users WHERE user_id={}"""

    set_user_dialog_state_query = """UPDATE Users SET state={} WHERE user_id={}"""


if __name__ == '__main__':
    connection = connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE_NAME
    )

    db = UserDataCommands(connection)
    flag = input("Тестовый режим: ")

    # if flag == "new users":
    #     for i in range(1, 55):
    #         db.insert_new_user(i, "test_user", "Артём", "Пурапов", True)
