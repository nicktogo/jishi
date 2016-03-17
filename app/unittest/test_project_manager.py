# coding=utf-8
import unittest
from app.module import project_manager

new_project = dict(requirements=u"无", title=u"专综", des="123", submit=u"提交", time=2016, number_of_member=1)


class TestPM(unittest.TestCase):
    def setUp(self):
        self._pm = project_manager.ProjectManager()

    def test_create(self):
        print self._pm.create_project(new_project)

    def test_apply(self):
        result = self._pm.apply_project(applier_name='nick', project_id='56e9ff5a0640fd0a318047c0')
        self.assertEqual(result.modified_count, 1)
        project = self._pm.find_project_by_id(project_id='56e9ff5a0640fd0a318047c0')
        self.assertIn('nick', project['appliers'])

    def test_approve(self):
        result = self._pm.approve_applier(applier_name='nick', project_id='56e9ff5a0640fd0a318047c0')
        self.assertEqual(result.modified_count, 1)
        project = self._pm.find_project_by_id(project_id='56e9ff5a0640fd0a318047c0')
        self.assertIn('nick', project['appliers'])

    def test_start(self):
        self._pm.start_project(project_id='56e9ff5a0640fd0a318047c0')
        project = self._pm.find_project_by_id(project_id='56e9ff5a0640fd0a318047c0')
        self.assertEqual(project['status'], project_manager.statuses.STARTED)

    def test_finish(self):
        self._pm.finish_project(project_id='56e9ff5a0640fd0a318047c0')
        project = self._pm.find_project_by_id(project_id='56e9ff5a0640fd0a318047c0')
        self.assertEqual(project['status'], project_manager.statuses.FINISHED)

    def test_cancel(self):
        self._pm.cancel_project(project_id='56e9ff5a0640fd0a318047c0')
        project = self._pm.find_project_by_id(project_id='56e9ff5a0640fd0a318047c0')
        self.assertEqual(project['status'], project_manager.statuses.CANCELED)

    def test_find_all(self):
        print self._pm.find_all_project()


if __name__ == '__main__':
    unittest.main()
