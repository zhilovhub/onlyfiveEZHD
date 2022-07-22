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
                cursor.execute(EventQueries.create_table_user_customize_query)
        except Error as e:
            print(e)

    def get_customizing_event_id(self, user_id: int) -> int:
        """Returns customizing event_id"""
        with self.connection.cursor() as cursor:
            cursor.execute(EventQueries.get_customizing_event_id_query, (user_id, ))
            return cursor.fetchone()[0]

    def get_event_diary_id(self, classroom_id: int) -> int:
        """Returns event_diary_id"""
        with self.connection.cursor() as cursor:
            cursor.execute(EventQueries.get_event_diary_id_query, (classroom_id,))
            return cursor.fetchone()[0]

    def get_all_classroom_events(self, classroom_id: int) -> list:
        """Returns all classroom's events"""
        events = []

        with self.connection.cursor() as cursor:
            cursor.execute(EventQueries.get_classroom_events_query, (classroom_id,))
            for event in cursor.fetchall():
                cursor.execute(EventQueries.get_event_students_query, (event[0], ))

                events.append({
                    "start_time": event[3],
                    "end_time": event[4],
                    "label": event[5],
                    "message_event_id": event[6],
                    "collective": event[7],
                    "current_count": event[8],
                    "required_count": event[9],
                    "current_students_count": len(cursor.fetchall()),
                    "required_students_count": event[10]
                })

            return sorted(events, key=lambda x: (-x["collective"], x["start_time"]))

    def get_classroom_event(self, event_id: int) -> dict:
        """Returns classroom event"""
        with self.connection.cursor() as cursor:
            cursor.execute(EventQueries.get_classroom_event_query, (event_id,))
            event = cursor.fetchone()
            cursor.execute(EventQueries.get_event_students_query, (event[0], ))

            return {
                    "start_time": event[3],
                    "end_time": event[4],
                    "label": event[5],
                    "message_event_id": event[6],
                    "collective": event[7],
                    "current_count": event[8],
                    "required_count": event[9],
                    "current_students_count": len(cursor.fetchall()),
                    "required_students_count": event[10]
                }

    def get_event_start_time(self, event_id: int) -> datetime:
        """Returns start time"""
        with self.connection.cursor() as cursor:
            cursor.execute(EventQueries.get_event_start_time_query, (event_id,))
            return cursor.fetchone()[0]

    def insert_new_event_diary(self, classroom_id: int) -> None:
        """Inserts new row into event_diary table"""
        with self.connection.cursor() as cursor:
            cursor.execute(EventQueries.insert_event_diary_query, (classroom_id,))
            self.connection.commit()

    def insert_new_event(self, event_diary_id: int) -> int:
        """Inserts new event"""
        with self.connection.cursor() as cursor:
            cursor.execute(EventQueries.insert_event_query, (event_diary_id,))
            self.connection.commit()

            return cursor.lastrowid

    def update_customizing_event_id(self, user_id: int, event_id) -> None:
        """Updates customizing event_id"""
        with self.connection.cursor() as cursor:
            cursor.execute(EventQueries.update_customizing_event_id_query, (event_id, user_id))
            self.connection.commit()

    def update_event_type(self, event_id: int, collective: bool) -> None:
        """Updates event's type"""
        with self.connection.cursor() as cursor:
            cursor.execute(EventQueries.update_event_type_query, (collective, event_id))
            self.connection.commit()

    def update_event_label(self, event_id: int, label: str) -> None:
        """Updates event's label"""
        with self.connection.cursor() as cursor:
            cursor.execute(EventQueries.update_event_label_query, (label, event_id))
            self.connection.commit()

    def update_event_start_time(self, event_id: int, start_time: datetime) -> None:
        """Updates event's start_time"""
        with self.connection.cursor() as cursor:
            cursor.execute(EventQueries.update_event_start_time_query, (start_time, event_id))
            self.connection.commit()

    def update_event_end_time(self, event_id: int, end_time) -> None:
        """Updates event's end_time"""
        with self.connection.cursor() as cursor:
            cursor.execute(EventQueries.update_event_end_time_query, (end_time, event_id))
            self.connection.commit()

    def update_event_message_event_id(self, event_id: int, message_event_id=None, auto=False) -> None:
        """Updates event's message_event_id"""
        with self.connection.cursor() as cursor:
            if auto:
                cursor.execute(EventQueries.get_event_classroom_id_query, (event_id,))
                classroom_id = cursor.fetchone()[0]
                cursor.execute(EventQueries.get_classroom_message_event_ids_query, (classroom_id,))
                message_event_ids = [row[0] for row in cursor.fetchall()]

                for i in range(1, 21):
                    if i not in message_event_ids:
                        cursor.execute(EventQueries.update_event_message_event_id_query, (i, event_id))
                        break
            else:
                cursor.execute(EventQueries.update_event_message_event_id_query, (message_event_id, event_id))

            self.connection.commit()

    def update_event_created(self, event_id: int, created: bool) -> None:
        """Updates event's created"""
        with self.connection.cursor() as cursor:
            cursor.execute(EventQueries.update_event_created_query, (created, event_id))
            self.connection.commit()

    def delete_event(self, event_id: int) -> None:
        """Deletes event"""
        with self.connection.cursor() as cursor:
            cursor.execute(EventQueries.delete_event_query, (event_id,))
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
        
        created BOOLEAN,
        start_time DATETIME,
        end_time DATETIME,
        label TEXT,
        message_event_id INT,
        collective BOOLEAN,
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

    create_table_user_customize_query = """CREATE TABLE IF NOT EXISTS UserCustomize(
            user_id INT UNIQUE,
            classroom_id INT,
            role_id INT,
            event_id INT,
            
            FOREIGN KEY (user_id) REFERENCES User (user_id),
            FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE SET NULL,
            FOREIGN KEY (role_id) REFERENCES Role (role_id) ON DELETE SET NULL,
            FOREIGN KEY (event_id) REFERENCES event (event_id) ON DELETE SET NULL
        )"""

    get_classroom_events_query = """SELECT * FROM event WHERE created=1 AND event_diary_id IN (SELECT event_diary_id 
    FROM event_diary WHERE classroom_id=%s)"""
    get_classroom_event_query = """SELECT * FROM event WHERE event_id=%s"""
    get_classroom_message_event_ids_query = """SELECT message_event_id FROM event WHERE message_event_id IS NOT NULL
    AND event_diary_id IN (SELECT event_diary_id FROM event_diary WHERE classroom_id=%s)"""

    get_event_students_query = """SELECT student_id FROM event_collective WHERE event_id=%s"""
    get_customizing_event_id_query = """SELECT event_id FROM UserCustomize WHERE user_id=%s"""
    get_event_diary_id_query = """SELECT event_diary_id FROM event_diary WHERE classroom_id=%s"""
    get_event_start_time_query = """SELECT start_time FROM event WHERE event_id=%s"""
    get_event_classroom_id_query = """SELECT classroom_id FROM event_diary WHERE 
    event_diary_id IN (SELECT event_diary_id FROM event WHERE event_id=%s)"""

    insert_event_diary_query = """INSERT INTO event_diary (classroom_id) VALUES (%s)"""
    insert_event_query = """INSERT INTO event (event_diary_id) VALUES (%s)"""

    update_customizing_event_id_query = """UPDATE UserCustomize SET event_id=%s WHERE user_id=%s"""
    update_event_type_query = """UPDATE event SET collective=%s WHERE event_id=%s"""
    update_event_label_query = """UPDATE event SET label=%s WHERE event_id=%s"""
    update_event_start_time_query = """UPDATE event SET start_time=%s WHERE event_id=%s"""
    update_event_end_time_query = """UPDATE event SET end_time=%s WHERE event_id=%s"""
    update_event_message_event_id_query = """UPDATE event SET message_event_id=%s WHERE event_id=%s"""
    update_event_created_query = """UPDATE event SET created=%s WHERE event_id=%s"""

    delete_event_query = """DELETE FROM event WHERE event_id=%s"""


if __name__ == '__main__':
    connection = connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE_NAME
    )

    event_db = EventCommands(connection)
    print(event_db.get_all_classroom_events(35))