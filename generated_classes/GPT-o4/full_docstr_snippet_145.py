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
        self.logger = logging.getLogger(workflow.__class__.__name__)
        self.start_time = None

    def __enter__(self):
        '''
        Entry point - called when workflow computation starts

        :return: self
        '''
        self.start_time = time.time()
        name = getattr(self.workflow, 'name', repr(self.workflow))
        self.logger.info(f"Starting workflow: {name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        Exit point - called when workflow computation ends

        :param exc_type: exception type
        :param exc_val: exception value
        :param exc_tb: exception traceback
        :return: False (so exceptions are propagated)
        '''
        elapsed = time.time() - (self.start_time or time.time())
        name = getattr(self.workflow, 'name', repr(self.workflow))
        if exc_type:
            self.logger.exception(f"Workflow {name} failed after {elapsed:.2f}s")
        else:
            self.logger.info(f"Workflow {name} completed in {elapsed:.2f}s")
        return False