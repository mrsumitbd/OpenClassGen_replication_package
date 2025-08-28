class IntervalGovernor:
    '''
    Decorate a function to only allow it to be called once per
    min_interval. Otherwise, it returns None.

    >>> gov = IntervalGovernor(30)
    >>> gov.min_interval.total_seconds()
    30.0
    '''

    def __init__(self, min_interval) -> None:
        self.min_interval = datetime.timedelta(seconds=min_interval)
        self.last_called = None

    def decorate(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = datetime.datetime.now()
            if self.last_called is None or now - self.last_called >= self.min_interval:
                self.last_called = now
                return func(*args, **kwargs)
            return None
        return wrapper