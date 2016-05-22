# coding=utf-8
from bson.objectid import ObjectId
from app.module.db.factory import MongoFactory
import message
import pymongo


class ProjectManager:
    def __init__(self):
        self._projects = MongoFactory().get_connection().get_collection(collection_name='projects')

    def create_project(self, data):
        return self._projects.insert_one(data).inserted_id

    def apply_project(self, applier_name, project_id):
        # TODO project_owner
        projectapplyed = self.find_project_by_id(project_id)
        projectOwner = projectapplyed['name']
        projectName = projectapplyed['projectname']
        message.apply(applier_name, project_id, projectName , projectOwner)
        return self._projects.update_one({
            '_id': ObjectId(project_id)
        }, {
            '$push': {
                'appliers': applier_name
            }
        })

    def approve_applier(self, applier_name, project_id):
        # TODO project_owner
        projectapplyed = self.find_project_by_id(project_id)
        projectOwner = projectapplyed['name']
        projectName = projectapplyed['projectname']
        message.accept(applier_name, project_id, projectName,projectOwner)
        result = self._projects.update_one({
            '_id': ObjectId(project_id)
        }, {
            '$pull': {
                'appliers': applier_name
            }
        })
        result_ = self._projects.update_one({
            '_id': ObjectId(project_id)
        }, {
            '$push': {
                'members': applier_name
            }
        })
        return result and result_

    def quit(self, username, project_id):
        # TODO project_owner
        message.quit(username, project_id, "")
        return self._projects.update_one({
            '_id': ObjectId(project_id)
        }, {
            '$pull': {
                'members': username
            }
        })

    def kick_out(self, username, project_id):
        # TODO project_owner
        message.kick_out(username, project_id, "")
        return self._projects.update_one({
            '_id': ObjectId(project_id)
        }, {
            '$pull': {
                'members': username
            }
        })

    def start_project(self, project_id):
        return self._projects.update_one({
            '_id': ObjectId(project_id)
        }, {
            '$set': {
                'status': statuses.STARTED
            }
        })

    def finish_project(self, project_id):
        return self._projects.update_one({
            '_id': ObjectId(project_id)
        }, {
            '$set': {
                'status': statuses.FINISHED
            }
        })

    def cancel_project(self, project_id):
        return self._projects.update_one({
            '_id': ObjectId(project_id)
        }, {
            '$set': {
                'status': statuses.CANCELED
            }
        })

    def find_all_project(self, page=1):
        limit = 3
        offset = (page-1) * limit
        return self._projects.find().skip(offset).limit(limit).sort([('created_time', pymongo.DESCENDING)])

    def project_count(self):
        return len(list(self._projects.find())) / 3 + 1

    def find_project_by_id(self, project_id):
        return self._projects.find_one({
            '_id': ObjectId(project_id)
        })

    def find_project_by_title(self, project_title):
        return self._projects.find_one({
            'name': project_title
        })


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


statuses = enum('CREATED', 'STARTED', 'FINISHED', 'CANCELED')
