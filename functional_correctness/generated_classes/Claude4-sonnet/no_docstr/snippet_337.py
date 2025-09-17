class VerifierBase:
    def __init__(self, _key_type, _pubkey=None):
        self._key_type = _key_type
        self._pubkey = _pubkey

    @property
    def public_key(self) -> bytes:
        return self._pubkey

    def _verify(self, _message: bytes, _signature: bytes) -> bool:
        raise NotImplementedError("Subclasses must implement _verify method")

    def verify(self, message, signature, signature_format=None) -> bool:
        if isinstance(message, str):
            message = message.encode('utf-8')
        if isinstance(signature, str):
            signature = signature.encode('utf-8')
        return self._verify(message, signature)