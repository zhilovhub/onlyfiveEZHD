from config import *


class DataBase:
    def __init__(self, connection) -> None:
        """Initialization"""
        self.host = HOST
        self.user = USER
        self.password = PASSWORD
        self.database_name = DATABASE_NAME
        self.connection = connection

    def __del__(self):
        self.connection.close()
