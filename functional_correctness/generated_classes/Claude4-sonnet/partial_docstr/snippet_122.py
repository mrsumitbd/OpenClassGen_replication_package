class OperatorCompareDates:
    '''
    Compares only dates, year is not taken into account.
    Compared date value must be string in format '%m-%d'
    '''

    @staticmethod
    def apply(q, attr, v):
        try:
            target_date = datetime.strptime(v, '%m-%d')
            target_month_day = (target_date.month, target_date.day)
            
            def date_filter(obj):
                obj_date_value = getattr(obj, attr, None)
                if obj_date_value is None:
                    return False
                
                if isinstance(obj_date_value, str):
                    try:
                        obj_date = datetime.strptime(obj_date_value, '%m-%d')
                        obj_month_day = (obj_date.month, obj_date.day)
                        return obj_month_day == target_month_day
                    except ValueError:
                        return False
                elif hasattr(obj_date_value, 'month') and hasattr(obj_date_value, 'day'):
                    obj_month_day = (obj_date_value.month, obj_date_value.day)
                    return obj_month_day == target_month_day
                else:
                    return False
            
            return filter(date_filter, q)
        except ValueError:
            return q