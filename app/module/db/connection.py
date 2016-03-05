from config import DbConfig


# using borg design pattern, every instance share a connection

class AbstractConnection:

    def __init__(self, sql):
        self.config = DbConfig().get_config(sql)

    def get_instance(self):
        raise NotImplementedError


class MysqlConnection(AbstractConnection):
    __share_state = {}

    def __init__(self):
        AbstractConnection.__init__(self,'mysql')
        self.__dict__ = self.__share_state
        if not hasattr(self, 'conn_instance'):
            print 'create...'
            self.conn_instance = self.get_instance()

    def get_instance(self):
        return 'Mysql connection'


class MongoConnection(AbstractConnection):
    __share_state = {}

    def __init__(self):
        AbstractConnection.__init__(self,'mongo')
        self.__dict__ = self.__share_state
        if not hasattr(self, 'conn_instance'):
            print 'create...'
            self.conn_instance = self.get_instance()

    def get_instance(self):
        return 'Mongo connection'


class RedisConnection(AbstractConnection):
    __share_state = {}

    def __init__(self):
        AbstractConnection.__init__(self,'redis')
        self.__dict__ = self.__share_state
        if not hasattr(self, 'conn_instance'):
            print 'create...'
            self.conn_instance = self.get_instance()

    def get_instance(self):
        return 'Redis connection'

if __name__ == '__main__':
    conn = MysqlConnection()
    conn2 = MysqlConnection()
    print conn.conn_instance # => 'Mysql connection'
    print conn2.conn_instance # => 'Mysql connection'
    conn.conn_instance = '123'
    print conn.conn_instance # => 123
    print conn2.conn_instance # => 123
