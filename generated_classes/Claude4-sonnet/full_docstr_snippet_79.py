class DirectFormat(object):
    '''The direct format (pointed straight at the field we want)'''

    def getCount(self, _):
        '''The count'''
        return 1

    def getValue(self, data):
        '''The value'''
        return data