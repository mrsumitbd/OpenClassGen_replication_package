class Scheme(object):
    '''The `Scheme` specifies the expected options for a configuration.

    It provides the template for what is expected when parsing and building
    configuration state. Additionally, it allows the user to specify default
    values for various fields. The `Scheme` allows for validation across all
    specified options, to the extent that the constraints are specified on
    those options.
    '''

    def __init__(self, *args):
        self.options = {}
        for arg in args:
            if isinstance(arg, dict):
                self.options.update(arg)
            else:
                raise TypeError("Scheme arguments must be dictionaries")

    def build_defaults(self):
        '''Build a dictionary of default values from the `Scheme`.

        Returns:
            dict: The default configurations as set by the `Scheme`.

        Raises:
            errors.InvalidSchemeError: The `Scheme` does not contain
                valid options.
        '''
        try:
            from . import errors
        except ImportError:
            class errors:
                class InvalidSchemeError(Exception):
                    pass
        
        if not isinstance(self.options, dict):
            raise errors.InvalidSchemeError("Scheme options must be a dictionary")
        
        defaults = {}
        for key, option in self.options.items():
            if hasattr(option, 'default'):
                defaults[key] = option.default
            elif isinstance(option, dict) and 'default' in option:
                defaults[key] = option['default']
        return defaults

    def flatten(self):
        '''Flatten the scheme into a dictionary where the keys are
        compound 'dot' notation keys, and the values are the corresponding
        options.

        Returns:
            dict: The flattened `Scheme`.
        '''
        def _flatten_dict(d, parent_key='', sep='.'):
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict) and not hasattr(v, 'validate'):
                    items.extend(_flatten_dict(v, new_key, sep=sep).items())
                else:
                    items.append((new_key, v))
            return dict(items)
        
        return _flatten_dict(self.options)

    def validate(self, config):
        '''Validate the given config against the `Scheme`.

        Args:
            config (dict): The configuration to validate.

        Raises:
            errors.SchemeValidationError: The configuration fails
                validation against the `Schema`.
        '''
        try:
            from . import errors
        except ImportError:
            class errors:
                class SchemeValidationError(Exception):
                    pass
        
        if not isinstance(config, dict):
            raise errors.SchemeValidationError("Configuration must be a dictionary")
        
        for key, option in self.options.items():
            if key in config:
                value = config[key]
                # Check if option has a validate method (assuming it's an Option-like object)
                if hasattr(option, 'validate'):
                    try:
                        option.validate(value)
                    except Exception as e:
                        raise errors.SchemeValidationError(f"Validation failed for '{key}': {str(e)}")
                # Check if option is a dict with validation rules
                elif isinstance(option, dict):
                    if 'type' in option and not isinstance(value, option['type']):
                        raise errors.SchemeValidationError(f"Type mismatch for '{key}': expected {option['type'].__name__}")
                    if 'required' in option and option['required'] and value is None:
                        raise errors.SchemeValidationError(f"Required field '{key}' is None")
            else:
                # Check if option is required
                if isinstance(option, dict) and option.get('required', False):
                    raise errors.SchemeValidationError(f"Required field '{key}' is missing")