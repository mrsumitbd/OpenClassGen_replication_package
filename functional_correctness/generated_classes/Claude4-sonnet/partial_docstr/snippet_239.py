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
        self.previous_state = None

    def __enter__(self):
        import torch
        self.previous_state = torch.is_inference_mode_enabled() if hasattr(torch, 'is_inference_mode_enabled') else False
        if hasattr(torch.utils.data, '_utils'):
            if hasattr(torch.utils.data._utils.fetch, '_HAS_NUMPY'):
                self.previous_prefetch_state = getattr(torch.utils.data._utils.fetch, '_prefetch_enabled', True)
                torch.utils.data._utils.fetch._prefetch_enabled = self.enabled
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if hasattr(torch.utils.data, '_utils'):
            if hasattr(torch.utils.data._utils.fetch, '_HAS_NUMPY'):
                torch.utils.data._utils.fetch._prefetch_enabled = self.previous_prefetch_state