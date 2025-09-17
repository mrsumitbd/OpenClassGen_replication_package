class LabelOperatorValidator(object):

    @staticmethod
    def validate_label_operator(actual, expected, **kwargs):
        # Handle None values
        if actual is None and expected is None:
            return True
        if actual is None or expected is None:
            if not kwargs.get('allow_none', False):
                raise AssertionError(f"Actual or expected operator is None: actual={actual}, expected={expected}")
            return True

        # Normalize synonyms
        _synonyms = {
            '=': '==', 'equals': '==', '==': '==',
            '!=': '!=', 'not_equals': '!=',
            'in': 'in', 'notin': 'notin',
            'exists': 'exists', 'has': 'exists'
        }
        def _norm(op):
            return _synonyms.get(op, op)

        actual_norm = _norm(actual)

        # Compare against single or multiple expected values
        if isinstance(expected, (list, tuple, set)):
            expected_norms = {_norm(e) for e in expected}
            if actual_norm not in expected_norms:
                raise AssertionError(f"Operator '{actual}' not in expected set {expected}")
        else:
            expected_norm = _norm(expected)
            if actual_norm != expected_norm:
                raise AssertionError(f"Operator '{actual}' does not match expected '{expected}'")

        return True