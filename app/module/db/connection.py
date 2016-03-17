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

    def insert_message(self, username, projectid, m_type):
        cursor = self._conn_instance.cursor()
        mes_num = self.find_mes_id(username, projectid, m_type)[0]
        if mes_num == 0:
            result = cursor.execute("insert into message(username, projectid, m_type)values('%s','%s','%s')"% (username, projectid, m_type))
            self._conn_instance.commit()
            return result
        else:
            print('you have already get one')

    def find_mes_id(self, username, projectid, m_type):
        cursor = self._conn_instance.cursor()
        result = cursor.execute("select mes_id from message where username  = '%s'and projectid = '%s'" % (username, projectid))
        if result == 0:
            results = (result, -1)
        else:
            mes_id = cursor.fetchall()[0][0]
            results = (result, mes_id)
        return results

    def merge_message(self,username, projectid, m_type):

        query = """ UPDATE message
                SET username = %s, projectid=%s, m_type= %s
                WHERE mes_id = %s """
        message_id = self.find_mes_id(username, projectid, m_type)[1]
        data = (username, projectid, m_type, message_id)
        cursor = self._conn_instance.cursor()
        result = cursor.execute(query, data)
        self._conn_instance.commit()
        return result

    def remove_message(self,username, projectid):
        cursor = self._conn_instance.cursor()
        mes_num = self.find_mes_id(username, projectid, 0)[0]
        if mes_num == 1:
            mes_id = self.find_mes_id(username, projectid, 0)[1]
            result = cursor.execute("delete from message where mes_id = '%s'" % mes_id)
            self._conn_instance.commit()
            return result
        else:
            print('you do not have any message')



    #Belle
    def insert_user(self,username,password):
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


