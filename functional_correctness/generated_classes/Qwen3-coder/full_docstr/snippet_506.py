class UnicodeMixin(object):
    '''Portable label mixin.'''

    def __unicode__(self):
        '''a human readable label for the object.'''
        raise NotImplementedError

    def __str__(self):
        '''a human readable label for the object, appropriately encoded (or not).'''
        return str(self.__unicode__())