class Valid(object):
    '''Alexa request validator.

    Attributes:
        app_id: str. Skill application ID.
        url: str. SignatureCertChainUrl header value sent by request.
            PEM-encoded X.509 certificate chain that Alexa used to sign the
            message. Used to cache valid url.
        cert: cryptography.hazmat.backends.openssl.x509._Certificate. The Amazon
            signing certificate. Used to cache valid cert.
    '''

    def __init__(self, app_id=None):
        '''Init validator.'''
        self.app_id = app_id
        self.url = None
        self.cert = None

    def application_id(self, app_id):
        '''Validate request application id matches true application id.

        Verifying the Application ID matches: https://goo.gl/qAdqe4.

        Args:
            app_id: str. Request application_id.

        Returns:
            bool: True if valid, False otherwise.
        '''
        if self.app_id is None:
            return True
        return self.app_id == app_id

    def _validate_certificate_url(self, url):
        '''Validate the certificate URL.'''
        parsed_url = urlparse(url)
        if parsed_url.scheme != 'https':
            return False
        if parsed_url.hostname != 's3.amazonaws.com':
            return False
        if not parsed_url.path.startswith('/echo.api/'):
            return False
        if ':' in parsed_url.netloc and not parsed_url.netloc.endswith(':443'):
            return False
        return True

    def _get_certificate(self, url):
        '''Get and cache the certificate.'''
        if self.url == url and self.cert is not None:
            return self.cert
        
        if not self._validate_certificate_url(url):
            return None
            
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return None
                
            cert_data = response.content
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            
            # Validate certificate
            if cert.not_valid_after < datetime.utcnow():
                return None
                
            # Check subject alt names
            try:
                ext = cert.extensions.get_extension_for_oid(x509.OID_SUBJECT_ALTERNATIVE_NAME)
                san = ext.value
                if 'echo-api.amazon.com' not in [name.value for name in san.get_values_for_type(x509.DNSName)]:
                    return None
            except x509.ExtensionNotFound:
                return None
            
            self.url = url
            self.cert = cert
            return cert
        except Exception:
            return None

    def _validate_signature(self, cert, signature, body):
        '''Validate the request signature.'''
        try:
            decoded_signature = base64.b64decode(signature)
            public_key = cert.public_key()
            public_key.verify(decoded_signature, body.encode('utf-8'), hashes.SHA1())
            return True
        except (InvalidSignature, ValueError, Exception):
            return False

    def _validate_timestamp(self, timestamp):
        '''Validate the request timestamp.'''
        try:
            request_time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
            current_time = datetime.utcnow()
            time_diff = abs((current_time - request_time).total_seconds())
            return time_diff <= 150  # 150 seconds = 2.5 minutes
        except ValueError:
            return False

    def sender(self, body, stamp, url, sig):
        '''Validate request is from Alexa.

        Verifying that the Request was Sent by Alexa: https://goo.gl/AcrzB5.
        Checking the Signature of the Request: https://goo.gl/FDkjBN.
        Checking the Timestamp of the Request: https://goo.gl/Z5JhqZ

        Args:
            body: str. HTTPS request body.
            stamp: str. Value of timestamp within request object of HTTPS
                request body.
            url: str. SignatureCertChainUrl header value sent
                by request.
            sig: str. Signature header value sent by request.

        Returns:
            bool: True if valid, False otherwise.
        '''
        # Validate timestamp
        if not self._validate_timestamp(stamp):
            return False
            
        # Get and validate certificate
        cert = self._get_certificate(url)
        if cert is None:
            return False
            
        # Validate signature
        if not self._validate_signature(cert, sig, body):
            return False
            
        return True

    def request(self, app_id=None, body=None, stamp=None, url=None, sig=None):
        '''Validate application ID and request is from Alexa.'''
        # Validate application ID
        if app_id is not None and not self.application_id(app_id):
            return False
            
        # Validate sender
        if body is not None and stamp is not None and url is not None and sig is not None:
            if not self.sender(body, stamp, url, sig):
                return False
        elif body is not None or stamp is not None or url is not None or sig is not None:
            # If any sender validation parameters are provided, all must be provided
            return False
            
        return True