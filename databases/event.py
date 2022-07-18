from database import *


class EventCommands(DataBase):
    def __init__(self, connection: CMySQLConnection) -> None:
        """Initialization"""
        super().__init__(connection)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(EventQueries.create_table_event_diary_query)
                cursor.execute(EventQueries.create_table_event_query)
        except Error as e:
            print(e)

    def insert_new_event_diary(self, classroom_id: int) -> None:
        """Inserts new row into event_diary table"""
        with self.connection.cursor() as cursor:
            cursor.execute(EventQueries.insert_event_diary_query, (classroom_id,))
            self.connection.commit()


class EventQueries:
    create_table_event_diary_query = """CREATE TABLE IF NOT EXISTS event_diary(
        event_diary_id INT NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
        classroom_id INT,
        
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE
    )"""

    create_table_event_query = """CREATE TABLE IF NOT EXISTS event(
        event_id INT NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
        event_diary_id INT,
        
        start_time DATETIME,
        end_time DATETIME,
        label TEXT,
        
        FOREIGN KEY (event_diary_id) REFERENCES event_diary (event_diary_id) ON DELETE CASCADE
    )"""

    insert_event_diary_query = """INSERT INTO event_diary (classroom_id) VALUES (%s)"""
