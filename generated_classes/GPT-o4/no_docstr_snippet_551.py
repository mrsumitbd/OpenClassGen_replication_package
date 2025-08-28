class UrlMatcher:
    _regex_type = type(re.compile(''))

    @classmethod
    def get_info(cls, entry, *matchers):
        for matcher in matchers:
            if isinstance(matcher, cls._regex_type):
                m = matcher.match(entry)
                if m:
                    gd = m.groupdict()
                    return gd if gd else m.groups()
            elif isinstance(matcher, str):
                m = re.match(matcher, entry)
                if m:
                    gd = m.groupdict()
                    return gd if gd else m.groups()
            elif callable(matcher):
                res = matcher(entry)
                if res:
                    return res
        return None