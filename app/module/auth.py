from db.factory import MysqlFactory


def valid_login(username, password):
    conn = MysqlFactory().get_connection()
    user = conn.find_user_by_username(username)
    if user_not_exist(user):
        return False
    if equal_password(user, password):
        return True


def signup(username, password):
    conn = MysqlFactory().get_connection()

    user = conn.find_user_by_username(username)
    if not user_not_exist(user):
        return False
    result = conn.insert_user(username, password)
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
    _, user_password = user[0]
    if user_password == password:
        return True
    else:
        return False

