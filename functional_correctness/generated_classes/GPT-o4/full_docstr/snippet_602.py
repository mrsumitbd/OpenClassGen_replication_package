class BaseStreamComponent:
    '''
    The Base class for Stream Components.
    '''

    def __init__(self, handler_function, args=None):
        '''
        :param handler_function: The function to execute on each message
        :param args: command line options or list representing as sys.argv
        '''
        self.handler_function = handler_function
        # if no args provided, take from sys.argv
        self.args = args if args is not None else sys.argv[1:]

    def start(self):
        '''
        Start the server and run forever.
        '''
        try:
            for line in sys.stdin:
                msg = line.rstrip('\n')
                # call handler with message and any args
                self.handler_function(msg, *self.args)
        except KeyboardInterrupt:
            pass