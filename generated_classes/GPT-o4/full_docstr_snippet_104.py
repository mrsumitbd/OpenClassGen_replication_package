class Task(object):
    '''
    Represents a task that has a unique task id, a command specifying foreground code to run and
    a function that will be run in a background process.
    Command must have similar interface with before_run, create_context and after_run.
    '''

    def __init__(self, task_id, wait_for_task_id, command):
        '''
        Setup task so it can be executed.
        :param task_id: int: unique id of this task
        :param wait_for_task_id: int: unique id of the task that this one is waiting for
        :param command: object with foreground setup/teardown methods and background function
        '''
        self.task_id = task_id
        self.wait_for_task_id = wait_for_task_id
        self.command = command
        self.context = None

    def before_run(self, parent_task_result):
        '''
        Run in main process before run method.
        :param parent_task_result: object: result of previous task or None if no previous task
        '''
        return self.command.before_run(parent_task_result)

    def create_context(self, message_queue):
        '''
        Run serially before the run method.
        :return object: context object passing state to the thread
        '''
        self.context = self.command.create_context(message_queue)
        return self.context

    def after_run(self, results):
        '''
        Run in main process after run method.
        :param results: object: results from run method.
        '''
        return self.command.after_run(results)

    def on_message(self, data):
        '''
        Call on_message on our command passing data
        :param data: object: parameter passed to the on_message member of this task's command
        '''
        return self.command.on_message(data)