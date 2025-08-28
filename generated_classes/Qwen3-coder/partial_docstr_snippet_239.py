class toggled_prefetching(object):
    '''Context that toggles prefetching on or off depending on a flag.

    Added in 0.5.0.

    Parameters
    ----------
    enabled : bool
        Whether enabled is activated (``True``) or off (``False``).

    '''

    def __init__(self, enabled):
        self.enabled = enabled
        self.original_state = None

    def __enter__(self):
        # Store the original prefetching state
        import sys
        if 'prefetching_enabled' in sys.modules:
            self.original_state = sys.modules['prefetching_enabled']
        
        # Set the new prefetching state
        sys.modules['prefetching_enabled'] = self.enabled
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        # Restore the original prefetching state
        import sys
        if self.original_state is not None:
            sys.modules['prefetching_enabled'] = self.original_state
        else:
            # If there was no original state, remove the module attribute
            if 'prefetching_enabled' in sys.modules:
                del sys.modules['prefetching_enabled']