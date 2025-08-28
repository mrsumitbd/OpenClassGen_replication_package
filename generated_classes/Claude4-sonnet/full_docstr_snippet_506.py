class UnicodeMixin(object):
    '''Portable label mixin.'''

    def __unicode__(self):
        '''a human readable label for the object.'''
        return str(self)

    def __str__(self):
        '''a human readable label for the object, appropriately encoded (or not).'''
        return '<%s: %s>' % (self.__class__.__name__, id(self))