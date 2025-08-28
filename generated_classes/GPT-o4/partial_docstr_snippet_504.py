class UnicodeMixin(object):
    '''Portable label mixin.'''

    def __unicode__(self):
        '''a human readable label for the object.'''
        raise NotImplementedError('Subclasses must implement __unicode__()')

    def __str__(self):
        '''a human readable label for the object, appropriately encoded (or not).'''
        try:
            # Python 2: unicode() exists, __str__ must return bytes
            return unicode(self).encode('utf-8')
        except NameError:
            # Python 3: unicode() is NameError, __str__ should return str
            result = self.__unicode__()
            if isinstance(result, bytes):
                return result.decode('utf-8')
            return result