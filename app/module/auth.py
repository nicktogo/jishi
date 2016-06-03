from db.factory import MysqlFactory
from db.factory import MongoFactory
from flask import g
from bson import ObjectId

def valid_login(username, password):
    conn = MongoFactory().get_connection().get_collection(collection_name='users')
    user = list(conn.find({'username': username}))
    if user_not_exist(user):
        return False
    if equal_password(user, password):
        user[0]['_id'] = str(user[0]['_id'])
        g.user = user[0]
        return True


def signup(user):
    conn = MongoFactory().get_connection().get_collection(collection_name='users')
    _user = list(conn.find({'username': user['username']}))
    if not user_not_exist(_user):
        return False
    user['wid'] = 0
    result = conn.insert_one(user).inserted_id
    if result:
        return True
    else:
        return False


def find_user_by_username(username):
    conn = MongoFactory().get_connection().get_collection(collection_name='users')
    return conn.find_one({'username': username})


def find_user_by_userId(userId):
    conn = MongoFactory().get_connection().get_collection(collection_name='users')
    return conn.find_one({'_id': ObjectId(userId)})


def user_not_exist(user):
    if len(user) == 0:
        return True
    else:
        return False


def equal_password(user, password):
    user = user[0]
    if user['password'] == password:
        return True
    else:
        return False

