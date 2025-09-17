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
        return bool(self.app_id and app_id == self.app_id)

    def _validate_timestamp(self, stamp):
        try:
            ts = datetime.fromisoformat(stamp.replace('Z', '+00:00'))
        except Exception:
            return False
        now = datetime.now(timezone.utc)
        diff = abs((now - ts).total_seconds())
        return diff <= 150

    def _validate_url(self, url):
        p = urlparse(url)
        if p.scheme != 'https':
            return False
        host = p.hostname or ''
        valid_hosts = (
            's3.amazonaws.com',
            's3.dualstack.us-east-1.amazonaws.com'
        )
        if host not in valid_hosts:
            return False
        if not p.path.startswith('/echo.api/'):
            return False
        return True

    def _fetch_cert(self, url):
        resp = requests.get(url)
        resp.raise_for_status()
        pem_data = resp.content
        certs = []
        for chunk in pem_data.split(b'-----END CERTIFICATE-----'):
            if b'-----BEGIN CERTIFICATE-----' in chunk:
                chunk = chunk + b'-----END CERTIFICATE-----'
                certs.append(x509.load_pem_x509_certificate(chunk))
        if not certs:
            raise ValueError('No certificates found')
        leaf = certs[0]
        # validity period
        now = datetime.now(timezone.utc)
        if leaf.not_valid_before > now or leaf.not_valid_after < now:
            raise ValueError('Certificate not valid now')
        # SAN check
        try:
            ext = leaf.extensions.get_extension_for_oid(
                ExtensionOID.SUBJECT_ALTERNATIVE_NAME
            )
            dns = ext.value.get_values_for_type(x509.DNSName)
        except x509.ExtensionNotFound:
            dns = []
        if 'echo-api.amazon.com' not in dns:
            raise ValueError('SAN mismatch')
        return leaf

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
        if not all((body, stamp, url, sig)):
            return False
        if not self._validate_timestamp(stamp):
            return False
        if not self._validate_url(url):
            return False
        if url != self.url or self.cert is None:
            try:
                self.cert = self._fetch_cert(url)
                self.url = url
            except Exception:
                return False
        try:
            signature = base64.b64decode(sig)
            pub = self.cert.public_key()
            pub.verify(
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
        if not self.application_id(app_id):
            return False
        return self.sender(body, stamp, url, sig)