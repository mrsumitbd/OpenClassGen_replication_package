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
        if limit is not None:
            if not isinstance(limit, int):
                raise TypeError("limit must be an integer")
            if limit < 0:
                raise ValueError("limit must be non-negative")
        if offset is not None:
            if not isinstance(offset, int):
                raise TypeError("offset must be an integer")
            if offset < 0:
                raise ValueError("offset must be non-negative")

        self.limit = limit
        self.offset = offset

    def get_sql(self):
        '''
        Generates the sql used for the limit clause of a Query

        :return: the sql for the limit clause of a Query
        :rtype: str
        '''
        parts = []
        if self.limit is not None:
            parts.append(f"LIMIT {self.limit}")
        if self.offset is not None:
            parts.append(f"OFFSET {self.offset}")
        return " ".join(parts)