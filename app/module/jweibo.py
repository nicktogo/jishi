from db.factory import MongoFactory
from bson.objectid import ObjectId


def get_db():
    return MongoFactory().get_connection()


def is_exist(wid):
    conn = get_db()
    return conn.users.find({'wid': wid})


def create_user(weibo_info, code):
    user = dict()
    user['wid'] = weibo_info['id']
    user['username'] = weibo_info['id']
    user['name'] = weibo_info['name']
    user['password'] = '123456'
    user['school'] = ''
    user['gender'] = ''
    user['grade'] = ''
    user['major'] = ''
    user['phone'] = ''
    user['nickname'] = ''
    conn = get_db()
    conn.users.insert_one(user)
    conn.weibos.insert_one(dict(wid=weibo_info['id'], code=code))