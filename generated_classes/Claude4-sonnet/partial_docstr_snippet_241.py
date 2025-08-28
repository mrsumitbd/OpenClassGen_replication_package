class VSGRegisterCommand(object):
    '''
    The VSGRegisterCommand class presents a simple command object to execute the register methods of a collection of VSGRegisterable objects.
    '''

    def __init__(self, logname, registerables):
        '''
        Initializes the instance with an collection of registerables.

        :param str logname:  The python logger log name.
        :param list registerables:  The list of VSGRegisterable class instances.
        '''
        self.logger = logging.getLogger(logname)
        self.registerables = registerables if registerables is not None else []

    def __enter__(self):
        '''
        Enter the runtime context related to this object.
        '''
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        '''
        Exit the runtime context related to this object.
        '''
        return False

    def execute(self):
        '''
        Executes the command.
        '''
        for registerable in self.registerables:
            try:
                registerable.register()
            except Exception as e:
                self.logger.error(f"Failed to register {registerable}: {e}")