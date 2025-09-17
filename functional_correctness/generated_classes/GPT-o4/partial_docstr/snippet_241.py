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
        self.registerables = list(registerables)
        self._registered = []

    def __enter__(self):
        '''
        Enter the runtime context related to this object.
        '''
        self.execute()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        '''
        Exit the runtime context related to this object.
        '''
        # Always attempt to unregister what was registered
        for reg in reversed(self._registered):
            try:
                reg.unregister()
                self.logger.info("Unregistered %r", reg)
            except Exception:
                self.logger.exception("Error while unregistering %r", reg)
        # Clear the list so repeated exits don't re-unregister
        self._registered.clear()
        # Do not suppress exceptions
        return False

    def execute(self):
        '''
        Executes the command.
        '''
        self._registered.clear()
        for reg in self.registerables:
            try:
                reg.register()
                self._registered.append(reg)
                self.logger.info("Registered %r", reg)
            except Exception:
                self.logger.exception("Error while registering %r", reg)
                # Roll back previously registered
                for prev in reversed(self._registered):
                    try:
                        prev.unregister()
                        self.logger.info("Rolled back unregister of %r", prev)
                    except Exception:
                        self.logger.exception("Error while rolling back %r", prev)
                self._registered.clear()
                raise
        return None