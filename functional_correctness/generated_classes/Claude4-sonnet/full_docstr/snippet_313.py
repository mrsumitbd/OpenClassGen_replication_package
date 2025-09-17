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
        sql_parts = []
        
        if self.limit is not None:
            sql_parts.append(f"LIMIT {self.limit}")
        
        if self.offset is not None:
            sql_parts.append(f"OFFSET {self.offset}")
        
        return " ".join(sql_parts)