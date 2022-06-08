from config import *


class UserDataBase:
    def __init__(self) -> None:
        """Initialization"""
        self.host = HOST
        self.user = USER
        self.password = PASSWORD

        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(DataBaseQueries.create_db_query)

            with connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=DATABASE_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(DataBaseQueries.create_table_user_query)
                    cursor.execute(DataBaseQueries.create_table_classroom_query)
                    cursor.execute(DataBaseQueries.create_table_student_query)
                    connection.commit()

        except Error as e:
            print(e)

    def insert_new_user(self, user_id: int, screen_name: str, first_name: str, is_ready: bool) -> None:
        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=DATABASE_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(DataBaseQueries.insert_new_user_query.format(user_id, screen_name, first_name, is_ready))
                    connection.commit()

        except Error as e:
            print(e)

    def set_user_is_ready(self, user_id: int) -> None:
        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=DATABASE_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(DataBaseQueries.set_user_is_ready_query.format(user_id))
                    connection.commit()

        except Error as e:
            print(e)

    def check_user_is_ready(self, user_id: int) -> bool:
        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=DATABASE_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(DataBaseQueries.check_user_is_ready_query.format(user_id))
                    user = cursor.fetchone()
                    return True if user else False

        except Error as e:
            print(e)

    def get_user_dialog_state(self, user_id: int) -> int:
        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=DATABASE_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(DataBaseQueries.get_user_dialog_state_query.format(user_id))
                    state = cursor.fetchone()[0]

                    return state

        except Error as e:
            print(e)

    def set_user_dialog_state(self, user_id: int, state: int) -> None:
        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=DATABASE_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(DataBaseQueries.set_user_dialog_state_query.format(state, user_id))
                    connection.commit()

        except Error as e:
            print(e)


class DataBaseQueries:
    create_db_query = f"""CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}"""

    create_table_user_query = """CREATE TABLE IF NOT EXISTS User(
        user_id INT NOT NULL UNIQUE PRIMARY KEY,
        screen_name VARCHAR(255),
        first_name VARCHAR(255),
        is_ready BOOLEAN,
        state INT
    )"""

    create_table_classroom_query = """CREATE TABLE IF NOT EXISTS Classroom(
        classroom_id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
        classroom_name VARCHAR(255)
    )"""

    create_table_student_query = """CREATE TABLE IF NOT EXISTS Student(
        user_id INT,
        classroom_id INT,
        role VARCHAR(255),
        FOREIGN KEY (user_id) REFERENCES User (user_id),
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id)
    )"""

    insert_new_user_query = """INSERT INTO User VALUES({}, '{}', '{}', {}, 0)"""

    set_user_is_ready_query = """UPDATE User SET is_ready=TRUE WHERE user_id={}"""

    check_user_is_ready_query = """SELECT * FROM User WHERE user_id={} AND is_ready=TRUE"""

    get_user_dialog_state_query = """SELECT state FROM User WHERE user_id={}"""

    set_user_dialog_state_query = """UPDATE User SET state={} WHERE user_id={}"""


if __name__ == '__main__':
    db = UserDataBase()
