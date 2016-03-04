from db.factory import MysqlFactory, MongoFactory, RedisFactory


def valid_login(username, password):
    with MysqlFactory().get_connection() as conn:
        return False


def signup(username, password):
    with MysqlFactory().get_connection() as conn:
        return False


