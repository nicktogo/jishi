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

    def is_in_applier(self,username,project_id):
        project = self.find_project_by_id(project_id)
        appliers = project['applier']
        for applier in appliers:
            if applier == username:
                return 1
        return 0

    def is_in_team(self,username,project_id):
        project = self.find_project_by_id(project_id)
        members = project['team']
        for member in members:
            if member == username:
                return 1
        return 0

    def apply_project(self, applier_name, project_id):
        # TODO project_owner
        projectapplyed = self.find_project_by_id(project_id)
        projectOwner = projectapplyed['creator']
        projectName = projectapplyed['name']
        if(self.is_in_applier(applier_name,project_id)):
            return "已存在"
        else:
            message.apply(applier_name, project_id, projectName , projectOwner)
            return self._projects.update_one({
                '_id': ObjectId(project_id)
            }, {
                '$push': {
                    'applier': applier_name
                }
            })

    def approve_applier(self, applier_name, project_id):
        # TODO project_owner
        projectapplyed = self.find_project_by_id(project_id)
        projectOwner = projectapplyed['creator']
        projectName = projectapplyed['name']
        currentPeople = projectapplyed['currentPeople'] + 1
        if(self.is_in_team(applier_name,project_id)):
            return '已在team中'
        else:
            message.accept(applier_name, project_id, projectName,projectOwner)
            result = self._projects.update_one({
                '_id': ObjectId(project_id)
            }, {
                '$pull': {
                    'applier': applier_name
                }
            })
            result_ = self._projects.update_one({
                '_id': ObjectId(project_id)
            }, {
                '$push': {
                    'team': applier_name
                }
            })
            result__ = self._projects.update_one({
                '_id': ObjectId(project_id)
            },{
                '$set': {
                    'currentPeople' : currentPeople
                }
            })
            return result and result_ and result__

    def quit(self, username, project_id):
        # TODO project_owner
        if(self.is_in_team(username,project_id)):
            message.quit(username, project_id, "")
            project = self.find_project_by_id(project_id)
            currentPeople = project['currentPeople'] - 1
            result = self._projects.update_one({
                '_id': ObjectId(project_id)
            }, {
                '$pull': {
                    'team': username
                }
            })
            result__ = self._projects.update_one({
                '_id': ObjectId(project_id)
            },{
                '$set': {
                    'currentPeople' : currentPeople
                }
            })
            return result and result__
        else:
            return '不在项目中'

    def kick_out(self, username, project_id):
        # TODO project_owner
        if(self.is_in_team(username,project_id)):
            project = self.find_project_by_id(project_id)
            currentPeople = project['currentPeople'] - 1
            message.kick_out(username, project_id, "")
            result =  self._projects.update_one({
                '_id': ObjectId(project_id)
            }, {
                '$pull': {
                    'team': username
                }
            })
            result__ = self._projects.update_one({
                '_id': ObjectId(project_id)
            },{
                '$set': {
                    'currentPeople': currentPeople
                }
            })
            return result and result__
        else:
            return '不在项目中'

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


