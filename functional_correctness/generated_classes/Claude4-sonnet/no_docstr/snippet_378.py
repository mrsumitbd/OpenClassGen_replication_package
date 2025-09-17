class LabelOperatorValidator(object):

    @staticmethod
    def validate_label_operator(actual, expected, **kwargs):
        if actual is None and expected is None:
            return True
        
        if actual is None or expected is None:
            return False
        
        if isinstance(expected, str):
            return str(actual) == expected
        
        if isinstance(expected, (int, float)):
            return actual == expected
        
        if isinstance(expected, bool):
            return bool(actual) == expected
        
        if isinstance(expected, list):
            return actual in expected
        
        if isinstance(expected, dict):
            operator = expected.get('operator', 'eq')
            value = expected.get('value')
            
            if operator == 'eq':
                return actual == value
            elif operator == 'ne':
                return actual != value
            elif operator == 'gt':
                return actual > value
            elif operator == 'gte':
                return actual >= value
            elif operator == 'lt':
                return actual < value
            elif operator == 'lte':
                return actual <= value
            elif operator == 'in':
                return actual in value
            elif operator == 'not_in':
                return actual not in value
            elif operator == 'contains':
                return value in actual
            elif operator == 'startswith':
                return str(actual).startswith(str(value))
            elif operator == 'endswith':
                return str(actual).endswith(str(value))
            elif operator == 'regex':
                import re
                return bool(re.search(str(value), str(actual)))
        
        return str(actual) == str(expected)