class MixedRealityAccountKeyCredential(object):
    ''' Represents an object used for Mixed Reality account key authentication.

    :param str account_id: The Mixed Reality service account identifier.
    :param AzureKeyCredential account_key: The Mixed Reality service account primary or secondary key credential.
    '''

    def __init__(self, account_id, account_key):
        self._account_id = account_id
        self._account_key = account_key

    def get_token(self, *scopes, **kwargs):
        current_time = datetime.now(timezone.utc)
        expires_on = int((current_time.timestamp() + 3600))  # 1 hour from now
        
        # Create the token payload
        payload = f"{self._account_id}\n{expires_on}"
        
        # Sign the payload with HMAC-SHA256
        key_bytes = base64.b64decode(self._account_key.key)
        signature = hmac.new(
            key_bytes,
            payload.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        # Encode the signature
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        
        # Create the access token
        token = f"{self._account_id}:{signature_b64}"
        
        return AccessToken(token, expires_on)