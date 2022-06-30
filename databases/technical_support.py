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
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.connection.cursor() as cursor:
            cursor.execute(TechnicalSupportQueries.insert_message_query.format(user_id, message, current_datetime))
            self.connection.commit()

    def get_message(self, user_id: int) -> str:
        """Return the message from DB by user_id"""
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(TechnicalSupportQueries.get_message_query.format(user_id))
                message = cursor.fetchone()

                return message[0] if message else ''
            except Error:
                return ''


class TechnicalSupportQueries:
    create_table_technical_support_messages_query = """CREATE TABLE IF NOT EXISTS Technical_support_messages(
    user_id INT,
    message TEXT,
    datetime DATETIME,
    FOREIGN KEY (user_id) REFERENCES User (user_id)
    )"""

    insert_message_query = """INSERT INTO Technical_support_messages VALUES({}, '{}', '{}')"""

    get_message_query = """SELECT message FROM Technical_support_messages WHERE user_id={} ORDER BY datetime DESC LIMIT 1"""
