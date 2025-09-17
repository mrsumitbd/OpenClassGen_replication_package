class OperatorCompareDates:
    '''
    Compares only dates, year is not taken into account.
    Compared date value must be string in format '%m-%d'
    '''

    @staticmethod
    def apply(q, attr, v):
        try:
            month_str, day_str = v.split('-')
            month, day = int(month_str), int(day_str)
        except Exception:
            raise ValueError(f"Invalid date format '{v}', expected '%m-%d'")
        return q.filter(
            extract('month', attr) == month,
            extract('day', attr) == day
        )