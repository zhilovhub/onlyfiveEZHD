from mysql.connector import connect, Error

from config import HOST, USER, PASSWORD, DATABASE_NAME


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
                    connection.commit()

        except Error as e:
            print(e)


class DataBaseQueries:
    create_db_query = f"""CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}"""

    create_table_user_query = """CREATE TABLE IF NOT EXISTS User(
        user_id int NOT NULL UNIQUE PRIMARY KEY,
        username VARCHAR(255),
        name VARCHAR(255)
    )"""


if __name__ == '__main__':
    db = DataBase()
