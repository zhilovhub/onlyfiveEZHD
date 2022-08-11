from database import *


class EventCommands(DataBase):
    def __init__(self, connection: Connection) -> None:
        """Initialization"""
        super().__init__(connection)

    @classmethod
    async def get_self(cls, connection: Connection):
        self = cls(connection)

        try:
            async with self.connection.cursor() as cursor:
                await cursor.execute(EventQueries.create_table_event_diary_query)
                await cursor.execute(EventQueries.create_table_event_query)
                await cursor.execute(EventQueries.create_table_event_collective_info_query)
                await cursor.execute(EventQueries.create_table_user_customize_query)
        except Error as e:
            print(e)

        return self

    async def get_customizing_event_id(self, user_id: int) -> int:
        """Returns customizing event_id"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.get_customizing_event_id_query, (user_id,))
            return list(await cursor.fetchone())[0]

    async def get_event_diary_id(self, classroom_id: int) -> int:
        """Returns event_diary_id"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.get_event_diary_id_query, (classroom_id,))
            return list(await cursor.fetchone())[0]

    async def get_all_classroom_events(self, classroom_id: int) -> list:
        """Returns all classroom's events"""
        events = []

        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.get_classroom_events_query, (classroom_id,))
            for event in list(await cursor.fetchall()):
                await cursor.execute(EventQueries.get_event_students_query, (event[0],))

                events.append({
                    "start_time": event[3],
                    "end_time": event[4],
                    "label": event[5],
                    "message_event_id": event[6],
                    "collective": event[7],
                    "current_count": event[8],
                    "required_count": event[9],
                    "current_students_count": len(list(await cursor.fetchall())),
                    "required_students_count": event[10],
                    "last": event[11],
                    "finished": event[12]
                })

            return sorted(events, key=lambda x: (-x["collective"], x["start_time"]))

    async def get_classroom_event(self, event_id: int) -> dict:
        """Returns classroom event"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.get_classroom_event_query, (event_id,))
            event = list(await cursor.fetchone())
            await cursor.execute(EventQueries.get_event_students_query, (event[0],))

            return {
                    "start_time": event[3],
                    "end_time": event[4],
                    "label": event[5],
                    "message_event_id": event[6],
                    "collective": event[7],
                    "current_count": event[8],
                    "required_count": event[9],
                    "current_students_count": len(list(await cursor.fetchall())),
                    "required_students_count": event[10],
                    "last": event[11],
                    "finished": event[12]
                }

    async def get_event_students(self, event_id: int) -> list:
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.get_event_students_query, (event_id,))
            return [row[0] for row in list(await cursor.fetchall())]

    async def get_event_start_time(self, event_id: int) -> datetime:
        """Returns start time"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.get_event_start_time_query, (event_id,))
            return list(await cursor.fetchone())[0]

    async def get_event_end_time(self, event_id: int) -> datetime:
        """Returns end time"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.get_event_end_time_query, (event_id,))
            return list(await cursor.fetchone())[0]

    async def get_event_current_count(self, event_id: int) -> int:
        """Returns current count"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.get_event_current_count_query, (event_id,))
            return list(await cursor.fetchone())[0]

    async def get_event_collective(self, event_id: int) -> int:
        """Returns collective"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.get_event_collective_query, (event_id,))
            return list(await cursor.fetchone())[0]

    async def get_event_finished(self, event_id: int) -> datetime:
        """Returns finished date"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.get_event_finished_query, (event_id,))
            return list(await cursor.fetchone())[0]

    async def get_event_id_by_message_event_id(self, message_event_id: int, classroom_id: int) -> int:
        """Returns event_id by message_event_id"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.get_event_id_by_message_event_id_query, (message_event_id, classroom_id))

            return list(await cursor.fetchone())[0]

    async def get_event_classroom_id(self, event_id: int) -> int:
        """Returns event's classroom id"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.get_event_classroom_id_query, (event_id,))

            return list(await cursor.fetchone())[0]

    async def get_started_events_and_mark_them(self) -> list:
        """Returns just started events and mark them last"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.get_just_started_events_query)
            event_ids = [row[0] for row in list(await cursor.fetchall())]

            if event_ids:
                await cursor.execute(EventQueries.update_events_last_query.format(",".join(map(str, event_ids))))
                await self.connection.commit()

            return event_ids

    async def get_finished_events_and_mark_them(self) -> list:
        """Returns just finished events and mark them finished"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.get_just_finished_events_query)
            event_ids = [row[0] for row in list(await cursor.fetchall())]

            if event_ids:
                await cursor.execute(EventQueries.update_events_finished_query.format(",".join(map(str, event_ids))))
                await self.connection.commit()

            return event_ids

    async def get_deleted_finished_events(self) -> list:
        """Returns and events that finished two days ago"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.get_deleted_finished_events_query)
            event_ids = [row[0] for row in list(await cursor.fetchall())]

            return event_ids

    async def insert_new_event_diary(self, classroom_id: int) -> None:
        """Inserts new row into event_diary table"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.insert_event_diary_query, (classroom_id,))
            await self.connection.commit()

    async def insert_new_event(self, event_diary_id: int) -> int:
        """Inserts new event"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.insert_event_query, (event_diary_id,))
            await self.connection.commit()

            return cursor.lastrowid

    async def insert_new_student(self, event_id: int, student_id: int) -> None:
        """Inserts new student to the collective event"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.insert_new_student_query, (event_id, student_id))
            await self.connection.commit()

    async def update_customizing_event_id(self, user_id: int, event_id) -> None:
        """Updates customizing event_id"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.update_customizing_event_id_query, (event_id, user_id))
            await self.connection.commit()

    async def update_event_type(self, event_id: int, collective: bool) -> None:
        """Updates event's type"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.update_event_type_query, (collective, event_id))
            await self.connection.commit()

    async def update_event_label(self, event_id: int, label: str) -> None:
        """Updates event's label"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.update_event_label_query, (label, event_id))
            await self.connection.commit()

    async def update_event_start_time(self, event_id: int, start_time: datetime) -> None:
        """Updates event's start_time"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.update_event_start_time_query, (start_time, event_id))
            await self.connection.commit()

    async def update_event_end_time(self, event_id: int, end_time) -> None:
        """Updates event's end_time"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.update_event_end_time_query, (end_time, event_id))
            await self.connection.commit()

    async def update_event_message_event_id(self, event_id: int, message_event_id=None, auto=False) -> None:
        """Updates event's message_event_id"""
        async with self.connection.cursor() as cursor:
            if auto:
                await cursor.execute(EventQueries.get_event_classroom_id_query, (event_id,))
                classroom_id = list(await cursor.fetchone())[0]
                await cursor.execute(EventQueries.get_classroom_message_event_ids_query, (classroom_id,))
                message_event_ids = [row[0] for row in list(await cursor.fetchall())]

                for i in range(1, 21):
                    if i not in message_event_ids:
                        await cursor.execute(EventQueries.update_event_message_event_id_query, (i, event_id))
                        break
            else:
                await cursor.execute(EventQueries.update_event_message_event_id_query, (message_event_id, event_id))

            await self.connection.commit()

    async def update_event_current_count(self, event_id: int, current_count) -> None:
        """Updates event's current count"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.update_event_current_count_query, (current_count, event_id))
            await self.connection.commit()

    async def update_event_required_count(self, event_id: int, required_count) -> None:
        """Updates event's required count"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.update_event_required_count_query, (required_count, event_id))
            await self.connection.commit()

    async def update_event_required_students_count(self, event_id: int, required_students_count) -> None:
        """Updates event's required students count"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.update_event_required_students_count_query, (required_students_count, event_id))
            await self.connection.commit()

    async def update_event_created(self, event_id: int, created: bool) -> None:
        """Updates event's created"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.update_event_created_query, (created, event_id))
            await self.connection.commit()

    async def update_event_last_and_finished(self, event_id: int, last: bool, finished) -> None:
        """Updates event's last and finished"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.update_event_last_and_finished_query, (last, finished, event_id))
            await self.connection.commit()

    async def delete_event(self, event_id: int) -> None:
        """Deletes event"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.delete_event_query, (event_id,))
            await self.connection.commit()

    async def delete_student(self, event_id: int, student_id: int) -> None:
        """Deletes student from the collective event"""
        async with self.connection.cursor() as cursor:
            await cursor.execute(EventQueries.delete_student_query, (event_id, student_id))
            await self.connection.commit()

    async def delete_finished_events(self, event_ids: list) -> None:
        """Deletes evevnts that finished two days ago"""
        async with self.connection.cursor() as cursor:
            if event_ids:
                await cursor.execute(EventQueries.delete_events_query.format(",".join(map(str, event_ids))))
                await self.connection.commit()


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
        last BOOLEAN DEFAULT 0,
        finished DATETIME DEFAULT NULL,
        
        FOREIGN KEY (event_diary_id) REFERENCES event_diary (event_diary_id) ON DELETE CASCADE
    )"""

    create_table_event_collective_info_query = """CREATE TABLE IF NOT EXISTS event_collective(
        id INT NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
        event_id INT,
        student_id INT,
        
        FOREIGN KEY (event_id) REFERENCES event (event_id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES Student (student_id) ON DELETE CASCADE
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
    get_event_id_by_message_event_id_query = """SELECT event_id FROM event WHERE message_event_id=%s AND 
    event_diary_id IN (SELECT event_diary_id FROM event_diary WHERE classroom_id=%s)"""
    get_customizing_event_id_query = """SELECT event_id FROM UserCustomize WHERE user_id=%s"""
    get_event_diary_id_query = """SELECT event_diary_id FROM event_diary WHERE classroom_id=%s"""
    get_event_start_time_query = """SELECT start_time FROM event WHERE event_id=%s"""
    get_event_end_time_query = """SELECT end_time FROM event WHERE event_id=%s"""
    get_event_current_count_query = """SELECT current_count FROM event WHERE event_id=%s"""
    get_event_collective_query = """SELECT collective FROM event WHERE event_id=%s"""
    get_event_finished_query = """SELECT finished FROM event WHERE event_id=%s"""
    get_event_classroom_id_query = """SELECT classroom_id FROM event_diary WHERE 
    event_diary_id IN (SELECT event_diary_id FROM event WHERE event_id=%s)"""
    get_just_started_events_query = """SELECT event_id FROM event WHERE NOW() > start_time AND last=0 AND 
    finished IS NULL AND created=1"""
    get_just_finished_events_query = """SELECT event_id FROM event 
    WHERE ((NOW() > end_time) OR (end_time IS NULL AND NOW() > start_time)) AND finished IS NULL AND created=1"""
    get_deleted_finished_events_query = """SELECT event_id FROM event
    WHERE DATEDIFF(NOW(), finished) >= 2"""

    insert_event_diary_query = """INSERT INTO event_diary (classroom_id) VALUES (%s)"""
    insert_event_query = """INSERT INTO event (event_diary_id) VALUES (%s)"""
    insert_new_student_query = """INSERT INTO event_collective (event_id, student_id) VALUES (%s, %s)"""

    update_customizing_event_id_query = """UPDATE UserCustomize SET event_id=%s WHERE user_id=%s"""
    update_event_type_query = """UPDATE event SET collective=%s WHERE event_id=%s"""
    update_event_label_query = """UPDATE event SET label=%s WHERE event_id=%s"""
    update_event_start_time_query = """UPDATE event SET start_time=%s WHERE event_id=%s"""
    update_event_end_time_query = """UPDATE event SET end_time=%s WHERE event_id=%s"""
    update_event_message_event_id_query = """UPDATE event SET message_event_id=%s WHERE event_id=%s"""
    update_event_current_count_query = """UPDATE event SET current_count=%s WHERE event_id=%s"""
    update_event_required_count_query = """UPDATE event SET required_count=%s WHERE event_id=%s"""
    update_event_required_students_count_query = """UPDATE event SET required_students_count=%s WHERE event_id=%s"""
    update_event_created_query = """UPDATE event SET created=%s WHERE event_id=%s"""
    update_event_last_and_finished_query = """UPDATE event SET last=%s, finished=%s WHERE event_id=%s"""
    update_events_last_query = """UPDATE event SET last=1 WHERE event_id IN ({})"""
    update_events_finished_query = """UPDATE event SET finished=NOW() WHERE event_id IN ({})"""

    delete_event_query = """DELETE FROM event WHERE event_id=%s"""
    delete_student_query = """DELETE FROM event_collective WHERE event_id=%s AND student_id=%s"""
    delete_events_query = """DELETE FROM event WHERE event_id IN ({})"""


if __name__ == '__main__':
    connection = connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        db=DATABASE_NAME
    )

    event_db = EventCommands(connection)
    print(event_db.get_all_classroom_events(35))
