class OPCinfo:
    '''Class to retrieve stats from APC from Web Server.'''

    def __init__(self, host=None, port=None, user=None, password=None,
                 monpath=None, ssl=False, extras=False, autoInit=True):
        '''Initialize URL for APC stats access.
        
        @param host:     Web Server Host. (Default: 127.0.0.1)
        @param port:     Web Server Port. (Default: 80, SSL: 443)
        @param user:     Username. (Not needed unless authentication is required 
                         to access status page.
        @param password: Password. (Not needed unless authentication is required 
                         to access status page.
        @param monpath:  APC status script path relative to Document Root.
                         (Default: apcinfo.php)
        @param ssl:      Use SSL if True. (Default: False)
        @param extras:   Include extra metrics, which can be computationally more 
                         expensive.
        @param autoInit: If True connect to Web Server on instantiation.
            
        '''
        self.host = host or '127.0.0.1'
        self.ssl = bool(ssl)
        if port is None:
            self.port = 443 if self.ssl else 80
        else:
            self.port = int(port)
        self.user = user
        self.password = password
        self.monpath = monpath or 'apcinfo.php'
        # ensure leading slash
        if not self.monpath.startswith('/'):
            self.monpath = '/' + self.monpath
        self.extras = bool(extras)
        self.stats = {}
        # build base URL
        scheme = 'https' if self.ssl else 'http'
        self.url = f"{scheme}://{self.host}:{self.port}{self.monpath}"
        if autoInit:
            self.initStats()

    def initStats(self, extras=None):
        '''Query and parse Web Server Status Page.
        
        @param extras: Include extra metrics, which can be computationally more 
                       expensive.
        
        '''
        if extras is not None:
            self.extras = bool(extras)
        headers = {}
        if self.user and self.password:
            auth = f"{self.user}:{self.password}"
            token = base64.b64encode(auth.encode('utf-8')).decode('ascii')
            headers['Authorization'] = f"Basic {token}"
        req = urllib.request.Request(self.url, headers=headers)
        ctx = None
        if self.ssl:
            ctx = _ssl._create_unverified_context()
        try:
            with urllib.request.urlopen(req, context=ctx) as resp:
                content = resp.read().decode('utf-8', errors='ignore')
        except urllib.error.URLError as e:
            raise RuntimeError(f"Failed to retrieve data: {e}")
        self._parseStats(content)

    def getAllStats(self):
        '''Return All Stats for APC.
        
        @return: Nested dictionary of stats.
        
        '''
        return self.stats

    def _parseStats(self, html_text):
        # find the main table with id="apcinfo"
        table_match = re.search(r'<table[^>]+id=["\']?apcinfo["\']?[^>]*>(.*?)</table>', html_text, re.S | re.I)
        target = table_match.group(1) if table_match else html_text
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', target, re.S | re.I)
        data = {}
        for row in rows:
            cols = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, re.S | re.I)
            if len(cols) >= 2:
                key = html.unescape(re.sub(r'<[^>]+>', '', cols[0])).strip().rstrip(':')
                val = html.unescape(re.sub(r'<[^>]+>', '', cols[1])).strip()
                # optionally skip extras if flag is False (not implemented filtering here)
                data[key] = val
        self.stats = data