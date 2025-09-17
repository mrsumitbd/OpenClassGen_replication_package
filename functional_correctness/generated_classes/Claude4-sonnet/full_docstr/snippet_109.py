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
        if hasattr(self.settings, 'progress_queue') and self.settings.progress_queue:
            self.settings.progress_queue.put({
                'type': 'creating_project',
                'message': 'Creating project...'
            })

    def create_context(self, message_queue, task_id):
        '''
        Create data needed by upload_project_run(DukeDS connection info).
        :param message_queue: Queue: queue background process can send messages to us on
        :param task_id: int: id of this command's task so message will be routed correctly
        '''
        return {
            'message_queue': message_queue,
            'task_id': task_id,
            'settings': self.settings,
            'local_project': self.local_project
        }

    def after_run(self, result_id):
        '''
        Save uuid associated with project we just created.
        :param result_id: str: uuid of the project
        '''
        self.local_project.remote_id = result_id