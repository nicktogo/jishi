# coding=utf-8
from config import DbConfig
import MySQLdb
from pymongo import MongoClient
from flask import request


# using borg design pattern, every instance share a connection


class AbstractConnection:
    def __init__(self, sql):
        self.config = DbConfig().get_config(sql)

    def _get_instance(self):
        raise NotImplementedError


class MysqlConnection(AbstractConnection):
    __share_state = {}

    def __init__(self):
        AbstractConnection.__init__(self, 'mysql')
        self.__share_state['config'] = self.config
        self.__dict__ = self.__share_state
        if not hasattr(self, 'conn_instance'):
            print 'create...'
            self._conn_instance = self._get_instance()

    def _get_instance(self):
        conn = MySQLdb.connect(host=self.config['host'],
                               user=self.config['user'],
                               passwd=self.config['password'],
                               db=self.config['database'],
                               port=int(self.config['port']))
        return conn

    def find_user_by_username(self, username):
        cursor = self._conn_instance.cursor()
        cursor.execute("select * from user where username = '%s'" % username)
        results = cursor.fetchall()
        return results

    # Belle
    def insert_user(self, username, password):
        cursor = self._conn_instance.cursor()
        result = cursor.execute("insert into user(username,password)values('%s','%s')" % (username, password))
        self._conn_instance.commit()
        return result


class MongoConnection(AbstractConnection):
    __share_state = {}

    def __init__(self):
        AbstractConnection.__init__(self, 'mongo')

        self.__share_state['config'] = self.config
        self.__dict__ = self.__share_state
        if not hasattr(self, '_conn_instance'):
            print 'create...'
            self._conn_instance = self._get_instance()

    def _get_instance(self):
        client = MongoClient('120.55.160.237', 27017)
        conn = client.jishi
        return conn

    def create_project(self):
        data = dict((key, unicode.encode(request.form.getlist(key)[0], 'utf-8')) for key in request.form.keys())

        # delete csrf token added by WTF
        del data['csrf_token']
        projects = self._conn_instance.projects
        project_id = projects.insert_one(data).inserted_id
        return project_id

    def find_all_project(self):
        projects = self._conn_instance.projects
        return projects.find()


class RedisConnection(AbstractConnection):
    __share_state = {}

    def __init__(self):
        AbstractConnection.__init__(self, 'redis')
        self.__share_state['config'] = self.config
        self.__dict__ = self.__share_state
        if not hasattr(self, 'conn_instance'):
            print 'create...'
            self._conn_instance = self._get_instance()

    def _get_instance(self):
        return 'Redis connection'


if __name__ == '__main__':
    test = MysqlConnection()
    print test.find_user_by_username('tzx')
