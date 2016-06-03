from db.factory import MysqlFactory
from db.factory import MongoFactory
from bson.objectid import ObjectId


def apply(username, projectid, projectname, project_owner):
    conn = MongoFactory().get_connection()
    m_type = 0
    message = {
        'username': username,
        'projectname': projectname,
        'project_id': projectid,
        'message_type': m_type,
        'message_state': 0,
        'isSolved': 0,
        'project_owner': project_owner
    }
    result = conn.insert_message(message)
    return result


def accept(username, projectid, projectname, project_owner, message_id):
    conn = MongoFactory().get_connection()
    m_type = 1
    conn.get_collection(collection_name='messages').update_one({
                '_id': ObjectId(message_id)
            }, {
                '$set': {
                    'isSolved': 1
                }
            })

    message = {
        'username': username,
        'project_id': projectid,
        'projectname': projectname,
        'message_type': m_type,
        'message_state': 0,
        'isSolved': 1,
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


def search_message(input, username):
    conn = MongoFactory().get_connection()
    result = conn.search_message(input, username)
    return result


def read_message(message_id):
    conn = MongoFactory().get_connection()
    return conn.read_message(message_id)


def show_myproject_message(username):
    conn = MysqlFactory().get_connection()
    result = conn.get_myproject_message(username)
    return result


def show_all_message():
    conn = MongoFactory().get_connection()
    return conn.findmessage()


def find_mes_by_id(message_id):
    conn = MongoFactory().get_connection()
    return conn.findmessagebyid(message_id)


def show_joined_project_message(username):
    conn = MysqlFactory().get_connection()
    result = conn.get_joined_project_message(username)
    return result


def find_message_by_user(username, page_no, page_size):
    conn = MongoFactory().get_connection()
    return conn.find_message_by_user(username=username, page_no=page_no, page_size=page_size)


def count_message_by_user(username):
    conn = MongoFactory().get_connection()
    return conn.count_message_by_user(username=username)

def UnSolvedMessageCount(username):
    conn = MongoFactory().get_connection()
    return len(list(conn.get_collection(collection_name='messages').find({'$and': [{'username': username},{'isSolved': '0'}]})))

if __name__ == '__main__':
    print UnSolvedMessageCount('admin')

