from db.factory import MysqlFactory


def apply(username, projectid):
    conn = MysqlFactory().get_connection()
    m_type = 0
    result = conn.insert_message(username, projectid, m_type)
    return result


def accept(username, projectid):
    conn = MysqlFactory().get_connection()
    m_type = 1
    result = conn.merge_message(username, projectid, m_type)
    return result


def quit(username, projectid):
    conn = MysqlFactory().get_connection()
    result = conn.remove_message(username, projectid)
    return result


def kick_out(username, projectid):
    conn = MysqlFactory().get_connection()
    result = conn.remove_message(username, projectid)
    return result


if __name__ == '__main__':
    if quit("candy_zhang", 3):
        print "successful";




