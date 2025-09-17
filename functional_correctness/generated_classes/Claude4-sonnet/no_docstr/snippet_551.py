class UrlMatcher:
    def __init__(self, pattern, **kwargs):
        self.pattern = pattern
        self.regex = re.compile(pattern)
        self.kwargs = kwargs
    
    def match(self, url):
        match = self.regex.search(url)
        if match:
            result = self.kwargs.copy()
            result.update(match.groupdict())
            return result
        return None

    @classmethod
    def get_info(cls, entry, *matchers):
        for matcher in matchers:
            result = matcher.match(entry)
            if result:
                return result
        return None