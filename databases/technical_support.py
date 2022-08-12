from database import *


class TechnicalSupportCommands(DataBase):
    """Initialisation"""
    def __init__(self, pool: Pool) -> None:
        super().__init__(pool)

    @classmethod
    async def get_self(cls, pool: Pool):
        self = cls(pool)

        try:
            async with self.pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(TechnicalSupportQueries.create_table_technical_support_messages_query)

        except Error as e:
            print(e)

        return self

    async def insert_message(self, user_id: int, message: str) -> None:
        """Add a new message to message table"""
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(TechnicalSupportQueries.insert_message_query.format(user_id, message,
                                                                                         current_datetime))
                await connection.commit()

    async def get_message(self, user_id: int) -> str:
        """Return the message from DB by user_id"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(TechnicalSupportQueries.get_message_query.format(user_id))
                    message = list(await cursor.fetchone())

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

    get_message_query = """SELECT message FROM Technical_support_messages 
    WHERE user_id={} ORDER BY datetime DESC LIMIT 1"""
