class UploadContext(object):
    '''
    Values passed to a background worker.
    Contains UploadSettings and parameters specific to the function to be run.
    '''

    def __init__(self, settings, params, message_queue, task_id):
        '''
        Setup context so it can be passed.
        :param settings: UploadSettings: project level info
        :param params: tuple: values specific to the function being run
        :param message_queue: Queue: queue background process can send messages to us on
        :param task_id: int: id of this command's task so message will be routed correctly
        '''
        self.settings = settings
        self.params = params
        self.message_queue = message_queue
        self.task_id = task_id

    def make_data_service(self):
        '''
        Recreate data service from within background worker.
        :return: DataServiceApi
        '''
        return self.settings.make_data_service()

    def send_message(self, data):
        '''
        Sends a message to the command's on_message(data) method.
        :param data: object: data sent to on_message
        '''
        self.message_queue.put((self.task_id, data))

    def start_waiting(self):
        '''
        Called when we start waiting for project to be ready for file uploads.
        '''
        self.send_message({'status': 'waiting', 'message': 'Waiting for project to be ready for file uploads'})

    def done_waiting(self):
        '''
        Called when project is ready for file uploads (after waiting).
        '''
        self.send_message({'status': 'ready', 'message': 'Project is ready for file uploads'})