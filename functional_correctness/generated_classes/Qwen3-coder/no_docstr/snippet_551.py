class UrlMatcher:
    @classmethod
    def get_info(cls, entry, *matchers):
        """
        Get information from an entry using the provided matchers.
        
        Args:
            entry: The entry to match against (typically a URL or request object)
            *matchers: Variable number of matcher objects or functions
            
        Returns:
            dict: A dictionary containing matching information
        """
        result = {}
        
        # If no matchers provided, return empty dict
        if not matchers:
            return result
            
        # Apply each matcher to the entry
        for i, matcher in enumerate(matchers):
            try:
                # If matcher is callable, call it with the entry
                if callable(matcher):
                    match_result = matcher(entry)
                    if match_result is not None:
                        result[f'matcher_{i}'] = match_result
                # If matcher has a match method, use that
                elif hasattr(matcher, 'match'):
                    match_result = matcher.match(entry)
                    if match_result is not None:
                        result[f'matcher_{i}'] = match_result
                # Otherwise, try direct comparison or containment
                else:
                    if matcher == entry or (hasattr(entry, '__contains__') and matcher in entry):
                        result[f'matcher_{i}'] = True
                    else:
                        result[f'matcher_{i}'] = False
            except Exception:
                # If matcher fails, record the error
                result[f'matcher_{i}'] = None
                
        return result