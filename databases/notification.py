from database import *


class NotificationCommands(DataBase):
    def __init__(self, connection: CMySQLConnection) -> None:
        """Initialization"""
        super().__init__(connection)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(NotificationQueries.create_table_notification_query)
                cursor.execute(NotificationQueries.create_table_notification_diary_query)
                cursor.execute(NotificationQueries.create_table_notification_students_query)

        except Error as e:
            print(e)

    def get_customizing_notification_id(self, user_id: int, classroom_id: int) -> int:
        """Returns customizing notification id"""
        with self.connection.cursor() as cursor:
            cursor.execute(NotificationQueries.get_customizing_notification_id_query, (user_id, classroom_id))
            return cursor.fetchone()[0]

    def get_notification_values_dict(self, user_id: int, classroom_id: int) -> dict:
        """Returns notification's values"""
        with self.connection.cursor() as cursor:
            notification_types = [
                "new_classmate",
                "leave_classmate",
                "requests",
                "events"
            ]

            cursor.execute(NotificationQueries.get_notification_values_query, (user_id, classroom_id))
            notification_dict = {notification_type: value
                                 for notification_type, value in zip(notification_types, cursor.fetchone()[3:])}

            return notification_dict

    def get_notification_information(self, notification_id: int) -> tuple:
        """Returns notification's information"""
        with self.connection.cursor() as cursor:
            cursor.execute(NotificationQueries.get_notification_information_query, (notification_id,))
            student_id, text = cursor.fetchone()

            return student_id, text

    def get_users_with_notification_type(self, classroom_id: int, notification_type: str) -> list:
        """Returns tuple of the users who has this notification_type True"""
        with self.connection.cursor() as cursor:
            cursor.execute(NotificationQueries.get_users_with_notification_type.format(notification_type),
                           (classroom_id,))
            users = [row[0] for row in cursor.fetchall()]

            return users

    def insert_new_notification(self, student_id: int, user_id: int, classroom_id: int) -> None:
        """Inserts new notification row"""
        with self.connection.cursor() as cursor:
            cursor.execute(NotificationQueries.insert_new_notification_query, (student_id, user_id, classroom_id))
            self.connection.commit()

    def insert_new_notification_into_diary(self, user_id: int, classroom_id: int) -> None:
        """Inserts new notification into diary"""
        with self.connection.cursor() as cursor:
            cursor.execute(NotificationQueries.get_student_id_query, (user_id, classroom_id))
            student_id = cursor.fetchone()[0]
            cursor.execute(NotificationQueries.insert_new_notification_into_diary_query, (student_id,))
            self.connection.commit()

    def insert_notification_students(self, notification_id: int, student_ids: list) -> None:
        """Inserts notification students"""
        with self.connection.cursor() as cursor:
            for student_id in student_ids:
                cursor.execute(NotificationQueries.insert_notification_student_query, (notification_id, student_id))
            self.connection.commit()

    def update_notification_value(self, user_id: int, classroom_id: int, notification_type: str) -> None:
        """Updates notification's value"""
        with self.connection.cursor() as cursor:
            cursor.execute(NotificationQueries.get_notification_value_query.format(notification_type),
                           (user_id, classroom_id))
            old_value = cursor.fetchone()[0]
            new_value = not old_value

            cursor.execute(NotificationQueries.update_notification_value_query.format(notification_type),
                           (new_value, user_id, classroom_id))
            self.connection.commit()

    def update_notification_text(self, notification_id: int, text) -> None:
        """Updates notification's text"""
        with self.connection.cursor() as cursor:
            cursor.execute(NotificationQueries.update_notification_text_query, (text, notification_id))
            self.connection.commit()

    def update_notification_datetime(self, notification_id: int, notification_datetime) -> None:
        """Updates notification's text"""
        with self.connection.cursor() as cursor:
            cursor.execute(NotificationQueries.update_notification_datetime_query,
                           (notification_datetime, notification_id))
            self.connection.commit()

    def delete_notification_from_diary(self, notification_id: int) -> None:
        """Deletes notification from diary"""
        with self.connection.cursor() as cursor:
            cursor.execute(NotificationQueries.delete_notification_from_diary_query, (notification_id,))
            self.connection.commit()

    def delete_notification_students(self, notification_id: int) -> None:
        """Deletes notification's students"""
        with self.connection.cursor() as cursor:
            cursor.execute(NotificationQueries.delete_notification_students_query, (notification_id,))
            self.connection.commit()


class NotificationQueries:
    create_table_notification_query = """CREATE TABLE IF NOT EXISTS notification(
        student_id INT,
        user_id INT,
        classroom_id INT,
        FOREIGN KEY (student_id) REFERENCES Student (student_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE,
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE,
        
        new_classmate BOOLEAN DEFAULT 1,
        leave_classmate BOOLEAN DEFAULT 1,
        requests BOOLEAN DEFAULT 1,
        events BOOLEAN DEFAULT 1
    )"""

    create_table_notification_diary_query = """CREATE TABLE IF NOT EXISTS notification_diary(
        notification_id INT NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
        student_id INT,
        
        text TEXT,
        date DATETIME,
        created BOOLEAN DEFAULT 0,
        
        FOREIGN KEY (student_id) REFERENCES Student (student_id) ON DELETE CASCADE
    )"""

    create_table_notification_students_query = """CREATE TABLE IF NOT EXISTS notification_students(
        notification_id INT,
        student_id INT,
        
        FOREIGN KEY (notification_id) REFERENCES notification_diary (notification_id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES Student (student_id) ON DELETE CASCADE
    )"""

    get_customizing_notification_id_query = """SELECT notification_id FROM notification_diary 
    WHERE student_id IN (SELECT student_id FROM Student WHERE user_id=%s AND classroom_id=%s)"""
    get_notification_values_query = """SELECT * FROM notification WHERE user_id=%s AND classroom_id=%s"""
    get_notification_value_query = """SELECT {} FROM notification WHERE user_id=%s AND classroom_id=%s"""
    get_notification_information_query = """SELECT student_id, text FROM notification_diary WHERE notification_id=%s"""
    get_users_with_notification_type = """SELECT user_id FROM notification WHERE {}=1 AND classroom_id=%s"""
    get_student_id_query = """SELECT student_id FROM Student WHERE user_id=%s AND classroom_id=%s"""

    insert_new_notification_query = """INSERT INTO notification (student_id, user_id, classroom_id) 
        VALUES(%s, %s, %s)"""
    insert_new_notification_into_diary_query = """INSERT INTO notification_diary (student_id) VALUES (%s)"""
    insert_notification_student_query = """INSERT INTO notification_students VALUES (%s, %s)"""

    update_notification_value_query = """UPDATE notification SET {}=%s WHERE user_id=%s AND classroom_id=%s"""
    update_notification_text_query = """UPDATE notification_diary SET text=%s WHERE notification_id=%s"""
    update_notification_datetime_query = """UPDATE notification_diary SET date=%s WHERE notification_id=%s"""

    delete_notification_from_diary_query = """DELETE FROM notification_diary WHERE notification_id=%s"""
    delete_notification_students_query = """DELETE FROM notification_students WHERE notification_id=%s"""
