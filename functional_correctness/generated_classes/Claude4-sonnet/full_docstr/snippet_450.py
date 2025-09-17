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
        try:
            # Check timestamp
            timestamp = datetime.datetime.fromisoformat(stamp.replace('Z', '+00:00'))
            now = datetime.datetime.now(datetime.timezone.utc)
            if abs((now - timestamp).total_seconds()) > 150:
                return False

            # Validate certificate URL
            if not self._validate_cert_url(url):
                return False

            # Get certificate
            cert = self._get_cert(url)
            if not cert:
                return False

            # Validate certificate
            if not self._validate_cert(cert):
                return False

            # Verify signature
            signature = base64.b64decode(sig)
            public_key = cert.public_key()
            public_key.verify(
                signature,
                body.encode('utf-8'),
                padding.PKCS1v15(),
                hashes.SHA1()
            )
            return True

        except Exception:
            return False

    def request(self, app_id=None, body=None, stamp=None, url=None, sig=None):
        '''Validate application ID and request is from Alexa.'''
        if app_id is not None and not self.application_id(app_id):
            return False
        if body is not None and stamp is not None and url is not None and sig is not None:
            return self.sender(body, stamp, url, sig)
        return True

    def _validate_cert_url(self, url):
        if not url.startswith('https://s3.amazonaws.com/echo.api/'):
            return False
        if '/..' in url or url.count('//') > 1:
            return False
        return True

    def _get_cert(self, url):
        if self.url == url and self.cert:
            return self.cert
        
        try:
            with urllib.request.urlopen(url) as response:
                cert_data = response.read()
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            self.url = url
            self.cert = cert
            return cert
        except Exception:
            return None

    def _validate_cert(self, cert):
        try:
            # Check if certificate is valid (not expired)
            now = datetime.datetime.now(datetime.timezone.utc)
            if cert.not_valid_after.replace(tzinfo=datetime.timezone.utc) < now:
                return False
            if cert.not_valid_before.replace(tzinfo=datetime.timezone.utc) > now:
                return False

            # Check subject alternative names
            try:
                san_ext = cert.extensions.get_extension_for_oid(x509.oid.ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
                dns_names = san_ext.value.get_values_for_type(x509.DNSName)
                if 'echo-api.amazon.com' not in dns_names:
                    return False
            except x509.ExtensionNotFound:
                return False

            return True
        except Exception:
            return False