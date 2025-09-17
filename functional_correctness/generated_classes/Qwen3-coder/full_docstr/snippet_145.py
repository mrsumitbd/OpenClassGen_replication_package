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
        self.logger = workflow.logger if hasattr(workflow, 'logger') else None

    def __enter__(self):
        '''
        Entry point - called when workflow computation starts

        :return: self
        '''
        if self.logger:
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
        if exc_type is None:
            if self.logger:
                self.logger.info(f"Workflow completed successfully: {self.workflow}")
        else:
            if self.logger:
                self.logger.error(f"Workflow failed: {self.workflow}", exc_info=(exc_type, exc_val, exc_tb))
        return self