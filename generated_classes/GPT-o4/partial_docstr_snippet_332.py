class StructuredDictMixin(object):
    ''' A dictionary with structure specification and validation.

    .. attribute:: structure

        The document structure specification. For details see
        :func:`monk.shortcuts.validate`.
    '''

    def _insert_defaults(self):
        merged = merge_defaults(self.structure, dict(self))
        self.clear()
        self.update(merged)

    def validate(self):
        validated = _validate(dict(self), self.structure)
        self.clear()
        self.update(validated)
        return validated