# coding=utf-8
import MySQLdb
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from config import DbConfig


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

    def insert_wantjoin(self, username, projectid, m_type):
        cursor = self._conn_instance.cursor()
        mes_num = self.find_mes_id(username, projectid, m_type)[0]
        if mes_num == 0:
            result = cursor.execute("insert into wantjoin(username, projectid, m_type)values('%s','%s','%s')" % (
                username, projectid, m_type))
            self._conn_instance.commit()
            return result
        else:
            print('you have already get one')

    def find_mes_id(self, username, projectid, m_type):
        cursor = self._conn_instance.cursor()
        result = cursor.execute(
            "select mes_id from wantjoin where username  = '%s'and projectid = '%s'" % (username, projectid))
        if result == 0:
            results = (result, -1)
        else:
            mes_id = cursor.fetchall()[0][0]
            results = (result, mes_id)
        return results

    def find_all_wantjoin_by_username(self, username):
        cursor = self._conn_instance.cursor()
        cursor.execute("select projectid from wantjoin where username  = '%s'" % username)
        result = cursor.fetchall()
        project_id = []
        for project in result:
            project_id.append(project[0])
        return project_id

    def merge_wantjoin(self, username, projectid, m_type):
        query = """ UPDATE wantjoin
                SET username = %s, projectid=%s, m_type= %s
                WHERE mes_id = %s """
        wantjoin_id = self.find_mes_id(username, projectid, m_type)[1]
        data = (username, projectid, m_type, wantjoin_id)
        cursor = self._conn_instance.cursor()
        result = cursor.execute(query, data)
        self._conn_instance.commit()
        return result

    def remove_wantjoin(self, username, projectid):
        cursor = self._conn_instance.cursor()
        mes_num = self.find_mes_id(username, projectid, 0)[0]
        if mes_num == 1:
            mes_id = self.find_mes_id(username, projectid, 0)[1]
            result = cursor.execute("delete from wantjoin where mes_id = '%s'" % mes_id)
            self._conn_instance.commit()
            return result
        else:
            print('you do not have any wantjoin')

    # Belle
    def insert_user(self, username, password):
        cursor = self._conn_instance.cursor()
        result = cursor.execute("insert into user(username,password)values('%s','%s')" % (username, password))
        self._conn_instance.commit()
        return result

    def insert_message(self, username, projectid, message_type, project_owner):
        cursor = self._conn_instance.cursor()
        result = cursor.execute(
            "insert into message(username, projectid, message_type, project_owner)values('%s','%s','%s','%s')" % (
                username, projectid, message_type, project_owner))
        self._conn_instance.commit()
        return result

    def get_all_message(self, username):
        cursor = self._conn_instance.cursor()
        cursor.execute("select * from message where username  = '%s'or project_owner = '%s'" % (username, username))
        result = cursor.fetchall()
        return result

    def get_myproject_message(self, username):
        cursor = self._conn_instance.cursor()
        cursor.execute("select * from message where username  = '%s'" % username)
        result = cursor.fetchall()
        return result

    def get_joined_project_message(self, username):
        cursor = self._conn_instance.cursor()
        cursor.execute("select * from message where username  = '%s'" % username)
        result = cursor.fetchall()
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
        client = MongoClient(host=self.config['host'], port=self.config['port'])
        conn = client.jishi
        conn.authenticate(self.config['user'],
                          password=self.config['password'])
        return conn

    def insert_user(self, username, password):
        self._conn_instance.users.insert_one({'username': username, 'password': password})
        return True

    def find_user_by_username(self, username):
        return list(self._conn_instance.users.find({'username': username}))

    def insert_message(self, message):
        message['created_time'] = datetime.now()
        self._conn_instance.messages.insert_one(message)
        return True

    def remove_message(self, message_id):
        self._conn_instance.messages.delete_many({'_id': ObjectId(message_id)})
        return True

    def read_message(self,message_id):
        return self._conn_instance.messages.update_one(
            { '_id': 'message_id'},
            { '$set': {  'message_state': 1}}
        )

    def get_all_message(self, username):
        messagesend = list(self._conn_instance.messages.find({'username':username}))
        messagereceived = list(self._conn_instance.messages.find({'project_owner':username}))
        messagereceived.extend(messagesend)
        return messagereceived

    def search_message(self, input, username):
        messagereceived = self.get_all_message(username)
        message_By_name = list(self._conn_instance.messages.find({'project_owner':{'$regex': input}}))
        message_By_Project = list(self._conn_instance.messages.find({'projectname':{'$regex': input}}))
        message_By_name.extend(message_By_Project)
        tmp = [val for val in messagereceived if val in message_By_name]
        return tmp

    def update_message(self, message):
        self._conn_instance.messages.update_one(message)
        return True

    def get_collection(self, collection_name):
        return self._conn_instance[collection_name]

    def findmessage(self):
        results = self._conn_instance.messages.find()
        return results

    def findmessagebyid(self, message_id):
        return self._conn_instance.messages.find_one({
            '_id': ObjectId(message_id)
        })




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
    test = MongoConnection()
    a = list(['a','b','c'])
    b = list(['b','c','d'])
    tmp = [val for val in a if val in b]
    print a
    print b
    print tmp
