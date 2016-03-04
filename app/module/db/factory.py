from config import DbConfig
import MySQLdb


class DbFactory():
    def __init__(self):
        pass

    def get_connection(self):
        raise NotImplementedError


class MysqlFactory(DbFactory):

    def get_connection(self):
        config = DbConfig().get_config('mysql')
        return None


class MongoFactory(DbFactory):

    def get_connection(self):
        config = DbConfig().get_config('mongo')
        return None


class RedisFactory(DbFactory):
    def get_connection(self):
        config = DbConfig().get_config('redis')
        return None
