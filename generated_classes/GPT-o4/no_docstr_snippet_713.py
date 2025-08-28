class BUrl:
    def __init__(self, url):
        self._parsed = urlparse(url)
        self._params = parse_qsl(self._parsed.query, keep_blank_values=True)

    def replace(self, name, value, only_replace=False):
        value = str(value)
        found = False
        new_params = []
        for k, v in self._params:
            if k == name:
                if not found:
                    new_params.append((name, value))
                    found = True
            else:
                new_params.append((k, v))
        self._params = new_params
        if not found and not only_replace:
            self._params.append((name, value))

    def append(self, name, value):
        self._params.append((name, str(value)))

    def delete(self, name):
        self._params = [(k, v) for k, v in self._params if k != name]

    @property
    def url(self):
        query = urlencode(self._params, doseq=True)
        parts = (
            self._parsed.scheme,
            self._parsed.netloc,
            self._parsed.path,
            self._parsed.params,
            query,
            self._parsed.fragment
        )
        return urlunparse(parts)