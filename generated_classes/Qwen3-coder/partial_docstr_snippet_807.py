class Handle(object):
    '''

    * `initialize`

    initial resource, e.g: database handle

    * `__enter__`

    get next data to do,you can fetch one or more data.

    * `slot`

    user custom code

    * `__exit__`

    when slot finished, call this method

    '''

    def __init__(self, component):
        '''
        Don't override this method unless you know what you're doing.
        :param component:
        :return:
        '''
        self.component = component


    def initialize(self):
        '''
        Hook for subclass initialization.

        This block is execute before thread initial
        '''
        pass


    def __enter__(self):
        '''
        ...note::
            You **MUST** return False when no data to do.

        The return value will be used in `Slot.slot`
        '''
        return False


    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        When slot done, will call this method.
        '''
        pass


    def slot(self, msg):
        '''
        Add your custom code at here.
        '''
        pass