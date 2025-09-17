class UnicodeMixin(object):
    '''Portable label mixin.'''

    def __unicode__(self):
        '''a human readable label for the object.'''
        raise NotImplementedError(
            '%s must implement __unicode__()' % self.__class__.__name__
        )

    def __str__(self):
        '''a human readable label for the object, appropriately encoded (or not).'''
        text = self.__unicode__()
        if sys.version_info[0] < 3:
            return text.encode('utf-8')
        return text.decode('utf-8') if isinstance(text, bytes) else text