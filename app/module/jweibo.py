from db.factory import MongoFactory
from bson.objectid import ObjectId
from weibo import APIClient
from flask_oauthlib.client import OAuth


APP_KEY = '148981535'  # app key
APP_SECRET = 'b12ec09cd669a458262881e580eba12e'  # app secret
CALLBACK_URL = 'http://lvh.me:5000/code'  # callback url


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


def get_wid(username):
    conn = get_db()
    user = conn.users.find_one({'username':username})
    if user['wid'] == 0:
        return None
    else:
        return user['wid']


def get_client(wid):
    conn = get_db()
    weibo_info = conn.weibos.find_one({'wid': wid})
    client_ = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    client_.set_access_token(weibo_info['access_token'], weibo_info['expire_in'])
    return client_


if __name__ == '__main__':
    conn = get_db()
    print conn.users.find_one({'wid':5148478576})