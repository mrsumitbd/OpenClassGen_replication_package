class BaseStreamComponent:
    '''
    The Base class for Stream Components.
    '''

    def __init__(self, handler_function, args=[]):
        '''
        :param handler_function: The function to execute on each message
        :param args: command line options or list representing as sys.argv
        '''
        self.handler_function = handler_function
        self.args = args

    def start(self):
        '''
        Start the server and run forever.
        '''
        raise NotImplementedError("Subclasses must implement start() method")