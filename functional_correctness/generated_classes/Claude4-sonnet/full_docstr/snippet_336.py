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
        self._host = host or '127.0.0.1'
        self._ssl = ssl
        self._port = port or (443 if ssl else 80)
        self._user = user
        self._password = password
        self._monpath = monpath or 'apcinfo.php'
        self._extras = extras
        self._stats = {}
        
        if autoInit:
            self.initStats(extras)

    def initStats(self, extras=None):
        '''Query and parse Web Server Status Page.
        
        @param extras: Include extra metrics, which can be computationally more 
                       expensive.
        
        '''
        if extras is not None:
            self._extras = extras
            
        protocol = 'https' if self._ssl else 'http'
        url = f"{protocol}://{self._host}:{self._port}/{self._monpath}"
        
        if self._extras:
            url += "?extras=1"
            
        request = urllib.request.Request(url)
        
        if self._user and self._password:
            credentials = base64.b64encode(f"{self._user}:{self._password}".encode()).decode()
            request.add_header('Authorization', f'Basic {credentials}')
            
        try:
            if self._ssl:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                response = urllib.request.urlopen(request, context=context)
            else:
                response = urllib.request.urlopen(request)
                
            data = response.read().decode('utf-8')
            self._stats = json.loads(data)
            
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
            self._stats = {}

    def getAllStats(self):
        '''Return All Stats for APC.
        
        @return: Nested dictionary of stats.
        
        '''
        return self._stats