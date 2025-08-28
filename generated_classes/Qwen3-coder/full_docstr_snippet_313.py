class Limit(object):
    '''
    Used internally by the Query class to set a limit and/or offset on the query.
    '''

    def __init__(self, limit=None, offset=None):
        '''
        Initializes the instance variables

        :param limit: the number of rows to return
        :type limit: int

        :param offset: the number of rows to start returning rows from
        :type limit: int
        '''
        self.limit = limit
        self.offset = offset

    def get_sql(self):
        '''
        Generates the sql used for the limit clause of a Query

        :return: the sql for the limit clause of a Query
        :rtype: str
        '''
        if self.limit is None and self.offset is None:
            return ""
        
        if self.offset is not None:
            if self.limit is not None:
                return f"LIMIT {self.offset}, {self.limit}"
            else:
                return f"LIMIT {self.offset}, 18446744073709551615"  # MySQL syntax for offset without limit
        else:
            return f"LIMIT {self.limit}"