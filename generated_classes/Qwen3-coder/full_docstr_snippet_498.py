class DataManagerTask(object):
    '''
    Task to be performed in the :class:`~kitty.data.data_manager.DataManager`
    context
    '''

    def __init__(self, task, *args):
        '''
        :type task: function(:class:`~kitty.data.data_manager.DataManager`) -> object
        :param task: task to be performed
        '''
        self.task = task
        self.args = args
        self.results = None

    def execute(self, dataman):
        '''
        run the task

        :type dataman: :class:`~kitty.data.data_manager.DataManager`
        :param dataman: the executing data manager
        '''
        self.results = self.task(dataman, *self.args)

    def get_results(self):
        '''
        :return: result from running the task
        '''
        return self.results