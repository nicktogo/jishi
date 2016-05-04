from db.factory import MysqlFactory
from db.factory import MongoFactory


def valid_login(username, password):
    conn = MongoFactory().get_connection().get_collection(collection_name='users')
    user = list(conn.find({'email': username}))
    if user_not_exist(user):
        return False
    if equal_password(user, password):
        return True


def signup(email, password):
    conn = MongoFactory().get_connection().get_collection(collection_name='users')

    user = list(conn.find({'email': email}))
    if not user_not_exist(user):
        return False
    result = conn.insert_one({'email': email, 'password': password})
    if result:
        return True
    else:
        return False


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

