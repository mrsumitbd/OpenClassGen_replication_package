class WorkItem(object):
    def __init__(self, future, fn, args, kwargs):
        self.future = future
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        if not self.future.set_running_or_notify_cancel():
            return
        
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.future.set_result(result)
        except Exception as exc:
            self.future.set_exception(exc)