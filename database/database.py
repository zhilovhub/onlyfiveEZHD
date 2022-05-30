from mysql.connector import connect, Error

from .config import HOST, USER, PASSWORD, DATABASE_NAME


class DataBase:
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

    def insert_new_user(self, user_id: int, screen_name: str, first_name: str) -> None:
        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=DATABASE_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(DataBaseQueries.insert_new_user_query.format(user_id, screen_name, first_name))
                    connection.commit()

        except Error as e:
            print(e)


class DataBaseQueries:
    create_db_query = f"""CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}"""

    create_table_user_query = """CREATE TABLE IF NOT EXISTS User(
        user_id int NOT NULL UNIQUE PRIMARY KEY,
        screen_name VARCHAR(255),
        first_name VARCHAR(255)
    )"""

    create_table_classroom_query = """CREATE TABLE IF NOT EXISTS Classroom(
        classroom_id int NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
        classroom_name VARCHAR(255)
    )"""

    create_table_student_query = """CREATE TABLE IF NOT EXISTS Student(
        user_id int,
        classroom_id int,
        role VARCHAR(255),
        FOREIGN KEY (user_id) REFERENCES User (user_id),
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id)
    )"""

    insert_new_user_query = """INSERT INTO User VALUES({}, '{}', '{}')"""


if __name__ == '__main__':
    db = DataBase()
