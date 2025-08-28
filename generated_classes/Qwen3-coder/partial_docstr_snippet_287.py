class Event(object):
    '''Profiling Event class.

    The event API is used to observe when demarcated events occur in your application, or to
    identify how long it takes to execute demarcated regions of code. Set annotations in the
    application to demarcate areas where events of interest occur.
    After running analysis, you can see the events marked in the Timeline pane.
    Event API is a per-thread function that works in resumed state.
    This function does not work in paused state.

    Parameters
    ----------
    name : string
        Name of the event
    '''

    def __init__(self, name):
        self.name = name
        self._start_time = None
        self._end_time = None
        self._active = False

    def __del__(self):
        if self._active:
            self.stop()

    def start(self):
        '''Start timing scope for this object'''
        import time
        if not self._active:
            self._start_time = time.time()
            self._end_time = None
            self._active = True

    def stop(self):
        '''Stop timing scope for this object'''
        import time
        if self._active:
            self._end_time = time.time()
            self._active = False

    def __str__(self):
        if self._start_time is None:
            return f"Event('{self.name}') - not started"
        elif self._active:
            return f"Event('{self.name}') - active since {self._start_time}"
        else:
            duration = self._end_time - self._start_time
            return f"Event('{self.name}') - duration: {duration:.6f}s"