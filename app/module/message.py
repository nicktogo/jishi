from db.factory import MysqlFactory


def apply(username, projectid, project_owner):
    conn = MysqlFactory().get_connection()
    m_type = 0
    result = conn.insert_wantjoin(username, projectid, m_type)
    conn.insert_message(username, projectid, 0, project_owner)
    return result


def accept(username, projectid, project_owner):
    conn = MysqlFactory().get_connection()
    m_type = 1
    result = conn.merge_wantjoin(username, projectid, m_type)
    conn.insert_message(username, projectid, 1, project_owner)
    return result


def quit(username, projectid, project_owner):
    conn = MysqlFactory().get_connection()
    result = conn.remove_wantjoin(username, projectid)
    conn.insert_message(username, projectid, 2, project_owner)
    return result


def kick_out(username, projectid, project_owner):
    conn = MysqlFactory().get_connection()
    result = conn.remove_wantjoin(username, projectid)
    conn.insert_message(username, projectid, 3, project_owner)
    return result


def show_all_wantjoin_by_username(username):
    conn = MysqlFactory().get_connection()
    result = conn.find_all_wantjoin_by_username(username)
    return result


def show_all_message(username):
    conn = MysqlFactory().get_connection()
    result = conn.get_all_message(username)
    return result


def show_myproject_message(username):
    conn = MysqlFactory().get_connection()
    result = conn.get_myproject_message(username)
    return result


def show_joined_project_message(username):
    conn = MysqlFactory().get_connection()
    result = conn.get_joined_project_message(username)
    return result


if __name__ == '__main__':
    print show_all_message('zhangjiaqi121@126.com')





