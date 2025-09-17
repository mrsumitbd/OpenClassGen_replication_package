class LabelOperatorValidator(object):

    @staticmethod
    def validate_label_operator(actual, expected, **kwargs):
        """
        Validate label operator based on actual and expected values.
        
        Args:
            actual: The actual value to validate
            expected: The expected value or pattern
            **kwargs: Additional validation parameters
            
        Returns:
            bool: True if validation passes, False otherwise
        """
        # Handle None values
        if actual is None and expected is None:
            return True
        if actual is None or expected is None:
            return False
            
        # Handle string comparisons
        if isinstance(actual, str) and isinstance(expected, str):
            return actual == expected
            
        # Handle numeric comparisons
        if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
            return actual == expected
            
        # Handle list/tuple comparisons
        if isinstance(actual, (list, tuple)) and isinstance(expected, (list, tuple)):
            if len(actual) != len(expected):
                return False
            return all(LabelOperatorValidator.validate_label_operator(a, e, **kwargs) 
                      for a, e in zip(actual, expected))
            
        # Handle dictionary comparisons
        if isinstance(actual, dict) and isinstance(expected, dict):
            if set(actual.keys()) != set(expected.keys()):
                return False
            return all(LabelOperatorValidator.validate_label_operator(actual[key], expected[key], **kwargs)
                      for key in actual.keys())
        
        # Default comparison
        return actual == expected