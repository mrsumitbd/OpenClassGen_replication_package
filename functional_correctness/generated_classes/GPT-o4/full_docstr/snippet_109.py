class CreateProjectCommand(object):
    '''
    Create project in DukeDS.
    '''

    def __init__(self, settings, local_project):
        '''
        Setup passing in all necessary data to create project and update external state.
        :param settings: UploadSettings: settings to be used/updated when we upload the project.
        :param local_project: LocalProject: information about the project(holds remote_id when done)
        '''
        self.settings = settings
        self.local_project = local_project

    def before_run(self, parent_task_result):
        '''
        Notify progress bar that we are creating the project.
        '''
        # If this is a Celery AsyncResult-like, update progress
        if hasattr(parent_task_result, 'update_state'):
            try:
                parent_task_result.update_state(
                    state='PROGRESS',
                    meta={'status': 'Creating project in DukeDS...', 'current': 0, 'total': 1}
                )
            except Exception:
                pass

    def create_context(self, message_queue, task_id):
        '''
        Create data needed by upload_project_run(DukeDS connection info).
        :param message_queue: Queue: queue background process can send messages to us on
        :param task_id: int: id of this command's task so message will be routed correctly
        '''
        return {
            'settings': self.settings,
            'local_project': self.local_project,
            'message_queue': message_queue,
            'task_id': task_id,
        }

    def after_run(self, result_id):
        '''
        Save uuid associated with project we just created.
        :param result_id: str: uuid of the project
        '''
        # Store on the local project
        setattr(self.local_project, 'remote_id', result_id)
        if hasattr(self.local_project, 'save'):
            try:
                self.local_project.save()
            except Exception:
                pass

        # Also persist to upload settings if desired
        setattr(self.settings, 'project_remote_id', result_id)
        if hasattr(self.settings, 'save'):
            try:
                self.settings.save()
            except Exception:
                pass