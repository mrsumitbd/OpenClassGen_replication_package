class ArgumentGroup(object):
    '''
    A class to declare argument groups at a class

    Usage:
        class MyParser(Parser):
            cmd1 = OptionalArgument()
            cmd2 = OptionalArgument()

            group = ArgumentGroup(title="group of possible commands",
                                  argument_names=["cmd1", "cmd2"])
    '''

    def __init__(self, title=None, description=None, argument_names=None):
        '''
        Constructs a ArgumentGroup instance

        @param title The title of the group displayed as headline
        @param description A detailed description of the argument group
        @param argument_names A list of strings containing the Arguments to be
                              grouped
        '''
        self.title = title
        self.description = description
        self.argument_names = list(argument_names) if argument_names is not None else []
        self.name = None
        self._arguments = []

    def add_to_parser(self, parser):
        '''
        Adds the group and its arguments to a argparse.ArgumentParser instance

        @param parser A argparse.ArgumentParser instance
        '''
        arg_group = parser.add_argument_group(self.title, self.description)
        # Add by name
        for arg_name in self.argument_names:
            if hasattr(parser, arg_name):
                arg = getattr(parser, arg_name)
                arg.add_to_parser(arg_group)
        # Add by direct argument instances
        for arg in self._arguments:
            arg.add_to_parser(arg_group)

    def set_name(self, name):
        '''
        Sets the name of this group. Normally this method should not be called
        directly. It is used by the ArgumentsCollectorMetaClass.

        @param name A string for a name
        '''
        self.name = name

    def add_argument(self, arg):
        '''
        Adds a Argument to this group.
        Normally this method should not be called directly.
        It is used by the ArgumentsCollectorMetaClass.

        @param arg An Argument instance to be added to this group.
        '''
        self._arguments.append(arg)