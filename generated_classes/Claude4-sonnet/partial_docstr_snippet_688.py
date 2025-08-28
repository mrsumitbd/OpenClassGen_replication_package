class Progress:
    '''
    An interface for receiving events that occur during the execution of the
    TidyPy tool suite.
    '''

    def __init__(self):
        pass

    def on_start(self):
        '''
        Called when the execution of the TidyPy tool suite begins.
        '''
        pass

    def on_tool_start(self, tool):
        '''
        Called when an individual tool begins execution.

        :param tool: the name of the tool that is starting
        :type tool: str
        '''
        pass

    def on_tool_finish(self, tool):
        '''
        Called when an individual tool completes execution.

        :param tool: the name of the tool that completed
        :type tool: str
        '''
        pass

    def on_finish(self):
        '''
        Called after all tools in the suite have completed.
        '''
        pass