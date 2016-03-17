from app.module import project_manager

if __name__ == '__main__':
    pm = project_manager.ProjectManager()
    result = pm.apply_project(applier_name='nick', project_id='56e9ff5a0640fd0a318047c0')
    print 'matched count: {}, modified count: {}'.format(result.matched_count, result.modified_count)
