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
            if hasattr(arg, 'key'):
                self.options[arg.key] = arg
            else:
                # Handle nested schemes or other objects
                if hasattr(arg, '__dict__'):
                    for key, value in arg.__dict__.items():
                        if hasattr(value, 'key'):
                            self.options[value.key] = value

    def build_defaults(self):
        '''Build a dictionary of default values from the `Scheme`.

        Returns:
            dict: The default configurations as set by the `Scheme`.

        Raises:
            errors.InvalidSchemeError: The `Scheme` does not contain
                valid options.
        '''
        defaults = {}
        
        for key, option in self.options.items():
            if hasattr(option, 'default') and option.default is not None:
                # Handle nested keys with dot notation
                if '.' in key:
                    keys = key.split('.')
                    current = defaults
                    for k in keys[:-1]:
                        if k not in current:
                            current[k] = {}
                        current = current[k]
                    current[keys[-1]] = option.default
                else:
                    defaults[key] = option.default
        
        return defaults

    def flatten(self):
        '''Flatten the scheme into a dictionary where the keys are
        compound 'dot' notation keys, and the values are the corresponding
        options.

        Returns:
            dict: The flattened `Scheme`.
        '''
        return dict(self.options)

    def validate(self, config):
        '''Validate the given config against the `Scheme`.

        Args:
            config (dict): The configuration to validate.

        Raises:
            errors.SchemeValidationError: The configuration fails
                validation against the `Schema`.
        '''
        def _get_nested_value(data, key):
            if '.' in key:
                keys = key.split('.')
                current = data
                for k in keys:
                    if isinstance(current, dict) and k in current:
                        current = current[k]
                    else:
                        return None
                return current
            else:
                return data.get(key)

        for key, option in self.options.items():
            value = _get_nested_value(config, key)
            
            # Check if required option is present
            if hasattr(option, 'required') and option.required and value is None:
                raise errors.SchemeValidationError(f"Required option '{key}' is missing")
            
            # Validate the value if present
            if value is not None and hasattr(option, 'validate'):
                try:
                    option.validate(value)
                except Exception as e:
                    raise errors.SchemeValidationError(f"Validation failed for option '{key}': {str(e)}")