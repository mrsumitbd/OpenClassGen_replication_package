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
        # Store configuration settings
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __call__(self, o):
        # Add configuration to the decorated class
        for attr_name in dir(self):
            if not attr_name.startswith('_'):
                attr_value = getattr(self, attr_name)
                setattr(o, attr_name, attr_value)
        
        # Add name class variable if it doesn't exist
        if not hasattr(o, 'name'):
            class_name = o.__name__ if hasattr(o, '__name__') else o.__class__.__name__
            if class_name.endswith('Command'):
                name = class_name[:-7].lower()  # Remove 'Command' and convert to lowercase
            else:
                name = class_name.lower()
            o.name = name
            
        return o