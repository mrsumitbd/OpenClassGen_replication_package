class ExcludeSpecificHeaders(object):

    def __init__(self, exclude_headers=None):
        if exclude_headers is None:
            exclude_headers = []
        self.exclude_headers = [header.lower() for header in exclude_headers]

    def __call__(self, header):
        return header.lower() not in self.exclude_headers