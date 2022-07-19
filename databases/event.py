from database import *


class EventCommands(DataBase):
    def __init__(self, connection: CMySQLConnection) -> None:
        """Initialization"""
        super().__init__(connection)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(EventQueries.create_table_event_diary_query)
                cursor.execute(EventQueries.create_table_event_query)
                cursor.execute(EventQueries.create_table_event_collective_info_query)
        except Error as e:
            print(e)

    def get_all_classroom_events(self, classroom_id: int) -> list:
        """Returns all classroom's events"""
        events = []

        with self.connection.cursor() as cursor:
            cursor.execute(EventQueries.get_classroom_events_query, (classroom_id,))
            for event in cursor.fetchall():
                cursor.execute(EventQueries.get_event_students_query, (event[0], ))

                events.append({
                    "start_time": event[2],
                    "end_time": event[3],
                    "label": event[4],
                    "message_event_id": event[5],
                    "collective": event[6],
                    "current_count": event[7],
                    "required_count": event[8],
                    "current_students_count": len(cursor.fetchall()),
                    "required_students_count": event[9]
                })

            return sorted(events, key=lambda x: (-x["collective"], x["start_time"]))

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
        message_event_id INT,
        collective BOOL,
        current_count INT,
        required_count INT,
        required_students_count INT,
        
        FOREIGN KEY (event_diary_id) REFERENCES event_diary (event_diary_id) ON DELETE CASCADE
    )"""

    create_table_event_collective_info_query = """CREATE TABLE IF NOT EXISTS event_collective(
        id INT NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
        event_id INT,
        student_id INT,
        
        FOREIGN KEY (event_id) REFERENCES event (event_id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES student (student_id) ON DELETE CASCADE
    )"""

    get_classroom_events_query = """SELECT * FROM event WHERE event_diary_id IN (SELECT event_diary_id FROM event_diary
    WHERE classroom_id=%s)"""

    get_event_students_query = """SELECT student_id FROM event_collective WHERE event_id=%s"""

    insert_event_diary_query = """INSERT INTO event_diary (classroom_id) VALUES (%s)"""


if __name__ == '__main__':
    connection = connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE_NAME
    )

    event_db = EventCommands(connection)
    print(event_db.get_all_classroom_events(35))
