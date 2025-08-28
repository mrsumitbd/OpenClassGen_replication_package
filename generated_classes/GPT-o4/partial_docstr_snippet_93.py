class IntervalGovernor:
    '''
    Decorate a function to only allow it to be called once per
    min_interval. Otherwise, it returns None.

    >>> gov = IntervalGovernor(30)
    >>> gov.min_interval.total_seconds()
    30.0
    '''

    def __init__(self, min_interval) -> None:
        if isinstance(min_interval, datetime.timedelta):
            self.min_interval = min_interval
        elif isinstance(min_interval, (int, float)):
            self.min_interval = datetime.timedelta(seconds=min_interval)
        else:
            raise ValueError("min_interval must be a timedelta or number of seconds")

    def decorate(self, func):
        last_call = None

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_call
            now = datetime.datetime.now()
            if last_call is None or (now - last_call) >= self.min_interval:
                last_call = now
                return func(*args, **kwargs)
            return None

        return wrapper