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
        self.port = port or (443 if ssl else 80)
        self.user = user
        self.password = password
        self.monpath = monpath or 'apcinfo.php'
        self.ssl = ssl
        self.extras = extras
        self.stats = {}
        
        protocol = 'https' if ssl else 'http'
        self.url = f"{protocol}://{self.host}:{self.port}/{self.monpath}"
        
        if autoInit:
            self.initStats()

    def initStats(self, extras=None):
        '''Query and parse Web Server Status Page.
        
        @param extras: Include extra metrics, which can be computationally more 
                       expensive.
        
        '''
        if extras is None:
            extras = self.extras
            
        try:
            # Create request
            request = urllib.request.Request(self.url)
            
            # Add authentication if provided
            if self.user and self.password:
                import base64
                credentials = f"{self.user}:{self.password}"
                encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
                request.add_header('Authorization', f'Basic {encoded_credentials}')
            
            # Handle SSL context
            context = None
            if self.ssl:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
            
            # Make request
            response = urllib.request.urlopen(request, context=context)
            content = response.read().decode('utf-8')
            
            # Parse content
            self.stats = self._parseStats(content, extras)
            
        except Exception as e:
            self.stats = {'error': str(e)}

    def _parseStats(self, content, extras):
        '''Parse the HTML content to extract APC stats.'''
        stats = {}
        
        # Simple parsing for common APC info patterns
        # Look for key: value patterns
        lines = content.split('\n')
        current_section = 'general'
        stats[current_section] = {}
        
        for line in lines:
            # Look for patterns like "APC Version: 3.1.13"
            match = re.search(r'([^:]+):\s*(.+)', line)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                stats[current_section][key] = value
            
            # Look for section headers
            if '<h2>' in line.lower() or '<h1>' in line.lower():
                section_match = re.search(r'<h[12]>([^<]+)', line, re.IGNORECASE)
                if section_match:
                    current_section = section_match.group(1).strip().lower().replace(' ', '_')
                    stats[current_section] = {}
        
        # Try to extract structured data if available
        # Look for table data
        table_parser = APCTableParser()
        table_parser.feed(content)
        if table_parser.data:
            for section, data in table_parser.data.items():
                if section not in stats:
                    stats[section] = {}
                stats[section].update(data)
        
        return stats

    def getAllStats(self):
        '''Return All Stats for APC.
        
        @return: Nested dictionary of stats.
        
        '''
        return self.stats