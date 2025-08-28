class IntervalGovernor:
    '''
    Decorate a function to only allow it to be called once per
    min_interval. Otherwise, it returns None.

    >>> gov = IntervalGovernor(30)
    >>> gov.min_interval.total_seconds()
    30.0
    '''

    def __init__(self, min_interval) -> None:
        self.min_interval = timedelta(seconds=min_interval) if isinstance(min_interval, (int, float)) else min_interval
        self.last_called = None

    def decorate(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            
            if self.last_called is None or (current_time - self.last_called) >= self.min_interval.total_seconds():
                self.last_called = current_time
                return func(*args, **kwargs)
            else:
                return None
        
        return wrapper