class ExcludeSpecificHeaders(object):

    def __init__(self, exclude_headers=None):
        self.exclude_headers = exclude_headers or []

    def __call__(self, header):
        return header not in self.exclude_headers