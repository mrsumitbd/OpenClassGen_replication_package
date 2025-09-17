class DataManagerTask(object):
    '''
    Task to be performed in the :class:`~kitty.data.data_manager.DataManager`
    context
    '''

    def __init__(self, task, *args):
        '''
        :type task: function(:class:`~kitty.data.data_manager.DataManager`, *args) -> object
        :param task: task to be performed
        '''
        self._task = task
        self._args = args
        self._result = None

    def execute(self, dataman):
        '''
        run the task

        :type dataman: :class:`~kitty.data.data_manager.DataManager`
        :param dataman: the executing data manager
        '''
        self._result = self._task(dataman, *self._args)
        return self._result

    def get_results(self):
        '''
        :return: result from running the task
        '''
        return self._result