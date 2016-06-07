from db.factory import MongoFactory
from bson.objectid import ObjectId
from weibo import APIClient
from flask_oauthlib.client import OAuth


def get_log_by_project_id(project_id):
    conn = MongoFactory().get_connection()
    log_conn = conn.get_collection("logs")
    u_conn = conn.get_collection("users")
    log = log_conn.find_one({'project_id': project_id})
    for timeline in log['timelines']:
        if timeline['type'] == 0:
            timeline['creator'] = u_conn.find_one({'username': timeline['creator']})
        if timeline['type'] == 1 or timeline['type'] == 2:
            timeline['applier'] = u_conn.find_one({'username': timeline['applier']})
    return log


