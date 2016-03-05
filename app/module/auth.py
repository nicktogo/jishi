from db.factory import MysqlFactory, MongoFactory, RedisFactory


def valid_login(username, password):
    with MysqlFactory().get_connection() as conn:
        user = conn.find_user_by_id(username)
        if user_not_exist(user):
            return False
        if equal_password(user, password):
            return True


def signup(username, password):
    with MysqlFactory().get_connection() as conn:
        return False


def user_not_exist(user):
    pass


def equal_password(user, password):
    pass