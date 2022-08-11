from config import *
from abc import abstractmethod, ABC


class DataBase(ABC):
    def __init__(self, connection: Connection) -> None:
        """Initialization"""
        self.host = HOST
        self.user = USER
        self.password = PASSWORD
        self.database_name = DATABASE_NAME
        self.connection = connection

    @abstractmethod
    async def get_self(cls, connection: Connection):
        """Returns cls's self"""

    def __del__(self):
        self.connection.close()
