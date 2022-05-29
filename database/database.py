import mysql.connector

from config import HOST, USER, PASSWORD


class DataBase:
    def __init__(self):
        """Initialization"""
        self.host = HOST
        self.user = USER
        self.password = PASSWORD
