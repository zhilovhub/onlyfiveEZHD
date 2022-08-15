from config import *


class DataBase:
    def __init__(self, connection) -> None:
        """Initialization"""
        self.connection = connection

    def __del__(self):
        self.connection.close()
