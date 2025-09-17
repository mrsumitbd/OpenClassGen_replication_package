class BUrl:
    def __init__(self, url):
        self._url = url
        parsed = urlparse(url)
        self._scheme = parsed.scheme
        self._netloc = parsed.netloc
        self._path = parsed.path
        self._params = parsed.params
        self._query = parsed.query
        self._fragment = parsed.fragment
        self._query_params = parse_qs(parsed.query, keep_blank_values=True)

    def replace(self, name, value, only_replace=False):
        if only_replace and name not in self._query_params:
            return self
        self._query_params[name] = [str(value)]
        return self

    def append(self, name, value):
        if name in self._query_params:
            self._query_params[name].append(str(value))
        else:
            self._query_params[name] = [str(value)]
        return self

    def delete(self, name):
        if name in self._query_params:
            del self._query_params[name]
        return self

    @property
    def url(self):
        query_string = urlencode(self._query_params, doseq=True)
        return urlunparse((
            self._scheme,
            self._netloc,
            self._path,
            self._params,
            query_string,
            self._fragment
        ))