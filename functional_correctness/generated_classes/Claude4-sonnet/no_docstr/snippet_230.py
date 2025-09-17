class ExecutionListener(object):

    def __init__(self, cfg):
        self.cfg = cfg

    def context_changed(self, context):
        pass

    def response_returned(self, context, response):
        pass