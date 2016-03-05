import connection


class DbFactory:
    def __init__(self):
        pass

    def get_connection(self):
        raise NotImplementedError


class MysqlFactory(DbFactory):

    def get_connection(self):
        return connection.MysqlConnection()


class MongoFactory(DbFactory):

    def get_connection(self):
        return connection.MongoConnection()


class RedisFactory(DbFactory):
    def get_connection(self):
        return connection.RedisConnection()
