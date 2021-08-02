import pypyodbc
from utils.read_config import Config


class MyConnection:

    def __init__(self):
        self.__connection_string = Config.get_connection_string()
        self.__conn = pypyodbc.connect(self.__connection_string)
        self.__cursor = self.conn.cursor()

    @property
    def conn(self):
        return self.__conn

    @property
    def cursor(self):
        return self.__cursor
