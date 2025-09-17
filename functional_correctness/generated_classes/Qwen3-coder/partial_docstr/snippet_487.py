class MixedRealityAccountKeyCredential(object):
    ''' Represents an object used for Mixed Reality account key authentication.

    :param str account_id: The Mixed Reality service account identifier.
    :param AzureKeyCredential account_key: The Mixed Reality service account primary or secondary key credential.
    '''

    def __init__(self, account_id, account_key):
        self.account_id = account_id
        self.account_key = account_key

    def get_token(self, *scopes, **kwargs):
        import base64
        import hashlib
        import hmac
        from datetime import datetime, timezone
        
        # Get current UTC time
        now = datetime.now(timezone.utc)
        expiry = int(now.timestamp() + 3600)  # 1 hour from now
        
        # Create the string to sign
        scope = scopes[0] if scopes else ""
        string_to_sign = f"{self.account_id}\n{scope}\n{expiry}"
        
        # Sign the string with the account key
        key = base64.b64decode(self.account_key.key)
        signature = hmac.new(key, string_to_sign.encode('utf-8'), hashlib.sha256).digest()
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        
        # Create the token
        token = f"Bearer {signature_b64}"
        
        return {
            'token': token,
            'expires_on': expiry
        }