class CommandDispatcher:
    '''
    A simple class for command dictionary. A command is a function
    which can take named parameters.
    '''

    def __init__(self):
        '''
        Create command dictionary
        '''
        self.commands = {}

    def command(self, fn):
        '''
        Add method or function to dispatcher. Can be use as a nice
        decorator.

        :param fn: function or method
        :type fn: function
        :return: the same function
        :rtype: function
        '''
        self.commands[fn.__name__] = fn
        return fn

    def execute_command(self, command, args=None):
        '''
        Execute a command

        :param command: name of the command
        :type command: str
        :param args: optional named arguments for command
        :type args: dict
        :return: the result of command
        :raises KeyError: if command is not found
        '''
        if command not in self.commands:
            raise KeyError(f"Command '{command}' not found")
        
        fn = self.commands[command]
        if args is None:
            args = {}
        
        return fn(**args)

    def bound(self, instance):
        '''
        Return a new dispatcher, which will switch all command functions
        with bounded methods of given instance matched by name. It will
        match only regular methods.

        :param instance: object instance
        :type instance: object
        :return: new Dispatcher
        :rtype: CommandDispatcher
        '''
        new_dispatcher = CommandDispatcher()
        
        for command_name, command_fn in self.commands.items():
            if hasattr(instance, command_name):
                method = getattr(instance, command_name)
                if callable(method) and not command_name.startswith('_'):
                    new_dispatcher.commands[command_name] = method
                else:
                    new_dispatcher.commands[command_name] = command_fn
            else:
                new_dispatcher.commands[command_name] = command_fn
        
        return new_dispatcher