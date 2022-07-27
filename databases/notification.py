from database import *


class NotificationCommands(DataBase):
    def __init__(self, connection: CMySQLConnection) -> None:
        """Initialization"""
        super().__init__(connection)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(NotificationQueries.create_table_notification_query)

        except Error as e:
            print(e)

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

    get_notification_values_query = """SELECT * FROM notification WHERE user_id=%s AND classroom_id=%s"""
    get_notification_value_query = """SELECT {} FROM notification WHERE user_id=%s AND classroom_id=%s"""
    get_users_with_notification_type = """SELECT user_id FROM notification WHERE {}=1 AND classroom_id=%s"""

    insert_new_notification_query = """INSERT INTO notification (student_id, user_id, classroom_id) 
        VALUES(%s, %s, %s)"""

    update_notification_value_query = """UPDATE notification SET {}=%s WHERE user_id=%s AND classroom_id=%s"""
