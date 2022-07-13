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

    def update_notification_value(self, user_id: int, classroom_id: int, notification_type: str, new_value: bool
                                  ) -> None:
        """Updates notification's value"""
        with self.connection.cursor() as cursor:
            cursor.execute(NotificationQueries.update_notification_value_query.format(notification_type),
                           (new_value, user_id, classroom_id))
            self.connection.commit()


class NotificationQueries:
    create_table_notification_query = """CREATE TABLE IF NOT EXISTS notification(
        user_id INT,
        classroom_id INT,
        FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE,
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE,
        
        new_classmate BOOLEAN DEFAULT 1,
        leave_classmate BOOLEAN DEFAULT 1,
        requests BOOLEAN DEFAULT 1
    )"""

    update_notification_value_query = """UPDATE notification SET {}=%s WHERE user_id=%s AND classroom_id=%S"""
