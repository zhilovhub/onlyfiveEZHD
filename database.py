from config import *


class DataBase:
    def __init__(self):
        self.host = HOST
        self.user = USER
        self.password = PASSWORD

        try:
            self.connection = connect(
                        host=self.host,
                        user=self.user,
                        password=self.password,
                        database=DATABASE_NAME
                )
        except Error as e:
            print(e)

    def get_connection(self):
        return self.connection

    def __del__(self):
        self.connection.close()
