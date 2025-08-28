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
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.is_running = False

    def __del__(self):
        if self.is_running:
            self.stop()

    def start(self):
        '''Start timing scope for this object'''
        if not self.is_running:
            self.start_time = time.time()
            self.end_time = None
            self.duration = None
            self.is_running = True

    def stop(self):
        '''Stop timing scope for this object'''
        if self.is_running:
            self.end_time = time.time()
            self.duration = self.end_time - self.start_time
            self.is_running = False

    def __str__(self):
        if self.duration is not None:
            return f"Event(name='{self.name}', duration={self.duration:.6f}s)"
        elif self.is_running:
            return f"Event(name='{self.name}', status='running')"
        else:
            return f"Event(name='{self.name}', status='not started')"