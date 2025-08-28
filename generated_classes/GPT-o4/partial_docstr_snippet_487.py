class MixedRealityAccountKeyCredential(object):
    ''' Represents an object used for Mixed Reality account key authentication.

    :param str account_id: The Mixed Reality service account identifier.
    :param AzureKeyCredential account_key: The Mixed Reality service account primary or secondary key credential.
    '''

    def __init__(self, account_id, account_key):
        if not isinstance(account_id, str):
            raise TypeError("account_id must be a string")
        if not isinstance(account_key, AzureKeyCredential):
            raise TypeError("account_key must be an AzureKeyCredential")
        self._account_id = account_id
        self._account_key = account_key

    def get_token(self, *scopes, **kwargs):
        # Token valid for 24 hours
        expiry = int(time.time()) + 24 * 60 * 60

        # JWT header and payload
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {"aud": self._account_id, "exp": expiry}

        def _b64url_encode(data):
            raw = data if isinstance(data, bytes) else data.encode("utf-8")
            enc = base64.urlsafe_b64encode(raw)
            return enc.rstrip(b"=").decode("utf-8")

        header_b64 = _b64url_encode(json.dumps(header))
        payload_b64 = _b64url_encode(json.dumps(payload))
        signing_input = f"{header_b64}.{payload_b64}"

        # Decode the account key and sign
        key_bytes = base64.b64decode(self._account_key.key)
        signature = hmac.new(key_bytes, signing_input.encode("utf-8"), hashlib.sha256).digest()
        signature_b64 = _b64url_encode(signature)

        token = f"{signing_input}.{signature_b64}"
        return AccessToken(token, expiry)