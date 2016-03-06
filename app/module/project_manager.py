from db.factory import MongoFactory, MysqlFactory
import format


class ProjectManager:
    def __init__(self):
        self._mysql_conn = MysqlFactory().get_connection()
        self._mongo_conn = MongoFactory().get_connection()

    def create_project(self, creator_id, project_id):
        result = self._mongo_conn.createProject(creator_id, project_id)
        return result

    def apply_project(self, applier_id, project_id):
        pass

    def approve_applier(self, applier_id, project_id):
        pass

    def start_project(self, project_id):
        pass

    def finish_project(self, project_id):
        pass

    def cancel_project(self, project_id):
        pass

    def find_all_project(self):
        raw_projects = self._mongo_conn.find_all_project()
        projects = format.todict(raw_projects)
        return projects
