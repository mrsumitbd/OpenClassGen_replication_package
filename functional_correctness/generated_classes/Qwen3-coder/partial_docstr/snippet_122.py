class OperatorCompareDates:
    '''
    Compares only dates, year is not taken into account.
    Compared date value must be string in format '%m-%d'
    '''

    @staticmethod
    def apply(q, attr, v):
        # Extract month and day from the query value
        query_month, query_day = map(int, q.split('-'))
        # Extract month and day from the attribute value
        attr_month, attr_day = map(int, attr.split('-'))
        
        # Compare months first
        if query_month < attr_month:
            return True
        elif query_month > attr_month:
            return False
        else:
            # If months are equal, compare days
            return query_day < attr_day