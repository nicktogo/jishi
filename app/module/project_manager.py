from app.module.db.factory import MongoFactory


class ProjectManager:
    def __init__(self):
        self._mongo_conn = MongoFactory().get_connection()

    def create_project(self):
        result = self._mongo_conn.create_project()
        return result

    def apply_project(self, applier_name, project_id):
        return self._mongo_conn.apply_project(applier_name, project_id)

    def approve_applier(self, applier_id, project_id):
        pass

    def start_project(self, project_id):
        pass

    def finish_project(self, project_id):
        pass

    def cancel_project(self, project_id):
        pass

    def find_all_project(self):
        return self._mongo_conn.find_all_project()
