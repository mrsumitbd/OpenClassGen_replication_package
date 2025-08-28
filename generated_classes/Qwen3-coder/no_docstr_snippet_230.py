class ExecutionListener(object):
    def __init__(self, cfg):
        self.cfg = cfg

    def context_changed(self, context):
        # Handle context change event
        pass

    def response_returned(self, context, response):
        # Handle response returned event
        pass