from database import *


class TechnicalSupportCommands(DataBase):
    """Initialisation"""
    def __init__(self, connection: CMySQLConnection) -> None:
        super().__init__(connection)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(TechnicalSupportQueries.create_table_technical_support_messages_query)

        except Error as e:
            print(e)

    def insert_message(self, user_id: int, message: str) -> None:
        """Add a new message to message table"""
        date = str(struct_time[0]) + str(struct_time[1]) + str(struct_time[2])
        with self.connection.cursor() as cursor:
            cursor.execute(TechnicalSupportQueries.insert_message_query.format(user_id, message, date))


class TechnicalSupportQueries:
    create_table_technical_support_messages_query = """CREATE TABLE IF NOT EXIST Technical_support_messages(
    user_id INT,
    message TEXT,
    date DATE,
    FOREIGN KEY (user_id) REFERENCES User (user_id)
    )"""

    insert_message_query = """INSERT INTO Technical_support_messages VALUES({}, {}, {})"""
