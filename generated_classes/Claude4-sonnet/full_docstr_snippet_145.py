class WorkflowMonitor(object):
    '''
    Small helper class that provides logging output to monitor workflow progress
    '''

    def __init__(self, workflow):
        '''
        Initialise the workflow monitor

        :type workflow: Workflow
        '''
        self.workflow = workflow
        self.start_time = None
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        '''
        Entry point - called when workflow computation starts

        :return: self
        '''
        self.start_time = time.time()
        self.logger.info(f"Starting workflow: {self.workflow}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        Exit point - called when workflow computation ends

        :param exc_type: exception type
        :param exc_val: exception value
        :param exc_tb: exception traceback
        :return: self
        '''
        end_time = time.time()
        duration = end_time - self.start_time if self.start_time else 0
        
        if exc_type is None:
            self.logger.info(f"Workflow completed successfully in {duration:.2f} seconds: {self.workflow}")
        else:
            self.logger.error(f"Workflow failed after {duration:.2f} seconds: {self.workflow} - {exc_type.__name__}: {exc_val}")
        
        return False