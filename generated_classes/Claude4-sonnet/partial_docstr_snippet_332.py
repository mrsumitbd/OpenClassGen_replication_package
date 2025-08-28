class StructuredDictMixin(object):
    ''' A dictionary with structure specification and validation.

    .. attribute:: structure

        The document structure specification. For details see
        :func:`monk.shortcuts.validate`.

    '''

    structure = {}

    def _insert_defaults(self):
        ''' Inserts default values from :attr:`StructuredDictMixin.structure`
            to `self` by merging the two structures
            (see :func:`monk.manipulation.merge_defaults`).
        '''
        from monk.manipulation import merge_defaults
        merge_defaults(self, self.structure)

    def validate(self):
        from monk.shortcuts import validate
        return validate(self, self.structure)