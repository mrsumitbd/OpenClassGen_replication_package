class ExcludeSpecificHeaders(object):
    def __init__(self, exclude_headers=None):
        if exclude_headers is None:
            exclude_headers = []
        self._exclude = set(h.lower() for h in exclude_headers)

    def __call__(self, header):
        return header.lower() not in self._exclude