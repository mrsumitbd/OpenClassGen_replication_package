class BUrl:
    def __init__(self, url):
        self._parsed = urlparse(url)
        self._params = parse_qs(self._parsed.query, keep_blank_values=True)
    
    def replace(self, name, value, only_replace=False):
        if only_replace and name not in self._params:
            return self
        
        new_burl = BUrl(self.url)
        new_burl._params[name] = [str(value)]
        return new_burl
    
    def append(self, name, value):
        new_burl = BUrl(self.url)
        if name in new_burl._params:
            new_burl._params[name].append(str(value))
        else:
            new_burl._params[name] = [str(value)]
        return new_burl
    
    def delete(self, name):
        new_burl = BUrl(self.url)
        if name in new_burl._params:
            del new_burl._params[name]
        return new_burl
    
    @property
    def url(self):
        query_string = urlencode(self._params, doseq=True)
        return urlunparse((
            self._parsed.scheme,
            self._parsed.netloc,
            self._parsed.path,
            self._parsed.params,
            query_string,
            self._parsed.fragment
        ))