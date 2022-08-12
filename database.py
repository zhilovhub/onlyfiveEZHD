from config import *
from abc import abstractmethod, ABC


class DataBase(ABC):
    def __init__(self, pool: Pool) -> None:
        """Initialization"""
        self.host = HOST
        self.user = USER
        self.password = PASSWORD
        self.database_name = DATABASE_NAME
        self.pool = pool

    @abstractmethod
    async def get_self(cls, pool: Pool):
        """Returns cls's self"""

    def __del__(self):
        self.pool.close()
