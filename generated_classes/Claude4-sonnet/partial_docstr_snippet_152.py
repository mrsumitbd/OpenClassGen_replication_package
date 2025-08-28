class ValidationErrorBuilder(object):
    '''Helper class to report multiple errors.

    Example: ::

        def validate_all(data):
            builder = ValidationErrorBuilder()
            if data['foo']['bar'] >= data['baz']['bam']:
                builder.add_error('foo.bar', 'Should be less than bam')
            if data['foo']['quux'] >= data['baz']['bam']:
                builder.add_fields('foo.quux', 'Should be less than bam')
            ...
            builder.raise_errors()
    '''

    def __init__(self):
        self.errors = {}

    def _make_error(self, path, error):
        parts = path.split('.')
        result = {}
        current = result
        
        for part in parts[:-1]:
            current[part] = {}
            current = current[part]
        
        current[parts[-1]] = error
        return result

    def add_error(self, path, error):
        '''Add error message for given field path.

        Example: ::

            builder = ValidationErrorBuilder()
            builder.add_error('foo.bar.baz', 'Some error')
            print builder.errors
            # => {'foo': {'bar': {'baz': 'Some error'}}}

        :param str path: '.'-separated list of field names
        :param str error: Error message
        '''
        error_dict = self._make_error(path, error)
        self.add_errors(error_dict)

    def add_errors(self, errors):
        '''Add errors in dict format.

        Example: ::

            builder = ValidationErrorBuilder()
            builder.add_errors({'foo': {'bar': 'Error 1'}})
            builder.add_errors({'foo': {'baz': 'Error 2'}, 'bam': 'Error 3'})
            print builder.errors
            # => {'foo': {'bar': 'Error 1', 'baz': 'Error 2'}, 'bam': 'Error 3'}

        :param str, list or dict errors: Errors to merge
        '''
        def merge_dicts(dict1, dict2):
            for key, value in dict2.items():
                if key in dict1:
                    if isinstance(dict1[key], dict) and isinstance(value, dict):
                        merge_dicts(dict1[key], value)
                    else:
                        dict1[key] = value
                else:
                    dict1[key] = value
        
        merge_dicts(self.errors, errors)

    def raise_errors(self):
        '''Raise :exc:`ValidationError` if errors are not empty;
        do nothing otherwise.
        '''
        if self.errors:
            raise ValidationError(self.errors)