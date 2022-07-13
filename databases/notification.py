from database import *


class NotificationCommands(DataBase):
    def __init__(self, connection: CMySQLConnection) -> None:
        """Initialization"""
        super().__init__(connection)


class NotificationQueries:
    pass
