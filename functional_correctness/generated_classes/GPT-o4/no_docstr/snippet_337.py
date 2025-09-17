class VerifierBase:

    def __init__(self, _key_type, _pubkey=None):
        self._key_type = _key_type
        if _pubkey is not None and not isinstance(_pubkey, (bytes, bytearray)):
            raise TypeError("public key must be bytes")
        self._pubkey = _pubkey

    @property
    def public_key(self) -> bytes:
        if self._pubkey is None:
            raise ValueError("no public key set")
        return bytes(self._pubkey)

    def _verify(self, _message: bytes, _signature: bytes) -> bool:
        raise NotImplementedError("subclasses must implement _verify")

    def verify(self, message, signature, signature_format=None) -> bool:
        if isinstance(message, str):
            message = message.encode('utf-8')
        if isinstance(signature, str):
            fmt = (signature_format or '').lower()
            if fmt in ('hex',):
                signature = bytes.fromhex(signature)
            elif fmt in ('base64', 'b64'):
                signature = base64.b64decode(signature)
            else:
                signature = signature.encode('utf-8')
        return self._verify(message, signature)