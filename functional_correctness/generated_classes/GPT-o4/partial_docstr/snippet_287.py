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
        self.name = str(name)
        self._start_time = None
        self.duration = 0.0
        self._running = False

    def __del__(self):
        if self._running:
            self.stop()

    def start(self):
        '''Start timing scope for this object'''
        if self._running:
            raise RuntimeError(f"Event '{self.name}' is already running")
        self._start_time = time.perf_counter()
        self._running = True

    def stop(self):
        '''Stop timing scope for this object'''
        if not self._running:
            raise RuntimeError(f"Event '{self.name}' is not running")
        end_time = time.perf_counter()
        self.duration += end_time - self._start_time
        self._start_time = None
        self._running = False

    def __str__(self):
        state = "running" if self._running else "stopped"
        return (f"Event(name='{self.name}', state={state}, "
                f"duration={self.duration:.6f}s)")