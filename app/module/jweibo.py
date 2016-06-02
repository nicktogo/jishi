from db.factory import MongoFactory
from bson.objectid import ObjectId


def get_db():
    return MongoFactory().get_connection()._conn_instance


def find_user(wid):
    conn = get_db()
    return conn.users.find_one({'wid': wid})


def create_user(weibo_info, code, access_token, expire_in):
    user = dict()
    user['wid'] = int(weibo_info['id'])
    user['username'] = str(weibo_info['id'])
    user['name'] = weibo_info['name']
    user['password'] = '123456'
    user['school'] = ''
    user['gender'] = ''
    user['grade'] = ''
    user['major'] = ''
    user['phone'] = ''
    user['nickname'] = ''
    user['profile_image_url'] = weibo_info['profile_image_url']
    conn = get_db()
    conn.users.insert_one(user)
    conn.weibos.insert_one(dict(wid=weibo_info['id'], code=code, access_token=access_token, expire_in=expire_in))
    return user

if __name__ == '__main__':
    conn = get_db()
    print conn.users.find_one({'wid':5148478576})