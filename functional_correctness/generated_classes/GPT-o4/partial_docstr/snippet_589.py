class Scheme(object):
    '''The `Scheme` specifies the expected options for a configuration.

    It provides the template for what is expected when parsing and building
    configuration state. Additionally, it allows the user to specify default
    values for various fields. The `Scheme` allows for validation across all
    specified options, to the extent that the constraints are specified on
    those options.
    '''

    def __init__(self, *args):
        self._options = {}
        for item in args:
            if not isinstance(item, tuple) or len(item) not in (2, 3):
                raise errors.InvalidSchemeError(f"Invalid option definition: {item!r}")
            name = item[0]
            default = item[1]
            validator = item[2] if len(item) == 3 else None
            if not isinstance(name, str):
                raise errors.InvalidSchemeError(f"Option name must be a string: {name!r}")
            self._options[name] = {
                'default': default,
                'validator': validator
            }

    def build_defaults(self):
        '''Build a dictionary of default values from the `Scheme`.

        Returns:
            dict: The default configurations as set by the `Scheme`.

        Raises:
            errors.InvalidSchemeError: The `Scheme` does not contain
                valid options.
        '''
        defaults = {}
        for key, spec in self._options.items():
            default = spec['default']
            if isinstance(default, Scheme):
                defaults[key] = default.build_defaults()
            else:
                defaults[key] = default
        return defaults

    def flatten(self):
        '''Flatten the scheme into a dictionary where the keys are
        compound 'dot' notation keys, and the values are the corresponding
        options.

        Returns:
            dict: The flattened `Scheme`.
        '''
        flat = {}
        for key, spec in self._options.items():
            flat[key] = spec
            default = spec['default']
            if isinstance(default, Scheme):
                nested = default.flatten()
                for nk, ns in nested.items():
                    flat[f"{key}.{nk}"] = ns
        return flat

    def validate(self, config):
        '''Validate the given config against the `Scheme`.

        Args:
            config (dict): The configuration to validate.

        Raises:
            errors.SchemeValidationError: The configuration fails
                validation against the `Schema`.
        '''
        if not isinstance(config, dict):
            raise errors.SchemeValidationError("Config must be a dict")
        # Check for unexpected keys
        for key in config:
            if key not in self._options:
                raise errors.SchemeValidationError(f"Unexpected key: {key}")
        for key, spec in self._options.items():
            default = spec['default']
            validator = spec['validator']
            if key in config:
                value = config[key]
                if isinstance(default, Scheme):
                    if not isinstance(value, dict):
                        raise errors.SchemeValidationError(f"Expected dict at '{key}'")
                    default.validate(value)
                else:
                    if validator and not validator(value):
                        raise errors.SchemeValidationError(f"Validation failed for key '{key}'")
            else:
                # missing key
                if not isinstance(default, Scheme) and default is None:
                    raise errors.SchemeValidationError(f"Missing required key: '{key}'")