class Configuration(object):
    ''' Defines the configuration settings for a search command.

    Documents, validates, and ensures that only relevant configuration settings
    are applied. Adds a :code:`name` class variable to search command classes
    that don't have one. The :code:`name` is derived from the name of the class.
    By convention command class names end with the word "Command". To derive
    :code:`name` the word "Command" is removed from the end of the class name
    and then converted to lower case for conformance with the `Search command
    style guide <http://docs.splunk.com/Documentation/Splunk/6.0/Search/Searchcommandstyleguide>`_

    '''

    def __init__(self, **kwargs):
        self.settings = kwargs

    def __call__(self, o):
        if hasattr(o, '__name__'):
            # It's a class
            cls = o
        else:
            # It's an instance
            cls = o.__class__
        
        # Apply configuration settings to the class
        for key, value in self.settings.items():
            setattr(cls, key, value)
        
        # Add name if it doesn't exist
        if not hasattr(cls, 'name'):
            class_name = cls.__name__
            if class_name.endswith('Command'):
                name = class_name[:-7].lower()  # Remove 'Command' and convert to lowercase
            else:
                name = class_name.lower()
            cls.name = name
        
        return o