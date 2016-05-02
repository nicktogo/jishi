from db.factory import MysqlFactory
from db.factory import MongoFactory
from bson.objectid import ObjectId


def apply(username, projectid, project_owner):
    conn = MongoFactory().get_connection()
    m_type = 0
    message = {
        'username': username,
        'project_id': projectid,
        'message_type': m_type,
        'message_state': 0,
        'project_owner': project_owner
    }
    result = conn.insert_message(message)
    return result


def accept(username, projectid, project_owner):
    conn = MongoFactory().get_connection()
    m_type = 1
    message = {
        'username': username,
        'project_id': projectid,
        'message_type': m_type,
        'message_state': 0,
        'project_owner': project_owner
    }
    result = conn.insert_message(message)
    return result


def quit(username, projectid, project_owner):
    conn = MongoFactory().get_connection()
    m_type = 2
    message = {
        'username': username,
        'project_id': projectid,
        'message_type': m_type,
        'message_state': 0,
        'project_owner': project_owner
    }
    result = conn.insert_message(message)
    return result


def kick_out(username, projectid, project_owner):
    conn = MongoFactory().get_connection()
    m_type = 3
    message = {
        'username': username,
        'project_id': projectid,
        'message_type': m_type,
        'message_state': 0,
        'project_owner': project_owner
    }
    result = conn.insert_message(message)
    return result


def get_all_message(username):
    conn = MongoFactory().get_connection()
    result = conn.get_all_message(username)
    return result


def read_message(message_id):
    conn = MongoFactory().get_connection()
    return conn.read_message(message_id)



def show_myproject_message(username):
    conn = MysqlFactory().get_connection()
    result = conn.get_myproject_message(username)
    return result


def show_joined_project_message(username):
    conn = MysqlFactory().get_connection()
    result = conn.get_joined_project_message(username)
    return result


if __name__ == '__main__':
    print read_message('57215e4023470e274030464d')





