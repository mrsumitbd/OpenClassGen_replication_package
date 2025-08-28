class ValidationErrorBuilder(object):
    '''Helper class to report multiple errors.

    Example: ::

        def validate_all(data):
            builder = ValidationErrorBuilder()
            if data['foo']['bar'] >= data['baz']['bam']:
                builder.add_error('foo.bar', 'Should be less than bam')
            if data['foo']['quux'] >= data['baz']['bam']:
                builder.add_error('foo.quux', 'Should be less than bam')
            ...
            builder.raise_errors()
    '''

    def __init__(self):
        self.errors = {}

    def _make_error(self, path, error):
        parts = path.split('.')
        node = error
        for key in reversed(parts):
            node = {key: node}
        return node

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
        new_err = self._make_error(path, error)
        self.add_errors(new_err)

    def add_errors(self, errors):
        '''Add errors in dict format.

        Example: ::

            builder = ValidationErrorBuilder()
            builder.add_errors({'foo': {'bar': 'Error 1'}})
            builder.add_errors({'foo': {'baz': 'Error 2'}, 'bam': 'Error 3'})
            print builder.errors
            # => {'foo': {'bar': 'Error 1', 'baz': 'Error 2'}, 'bam': 'Error 3'}

        :param dict or list errors: Errors to merge
        '''
        if isinstance(errors, list):
            for e in errors:
                self.add_errors(e)
        elif isinstance(errors, dict):
            for key, val in errors.items():
                if key in self.errors and isinstance(self.errors[key], dict) and isinstance(val, dict):
                    # merge nested dicts
                    sub = ValidationErrorBuilder()
                    sub.errors = self.errors[key]
                    sub.add_errors(val)
                    self.errors[key] = sub.errors
                else:
                    self.errors[key] = val
        else:
            raise TypeError("add_errors requires a dict or list of dicts")

    def raise_errors(self):
        '''Raise :exc:`ValidationError` if errors are not empty;
            do nothing otherwise.
        '''
        if self.errors:
            raise ValidationError(self.errors)