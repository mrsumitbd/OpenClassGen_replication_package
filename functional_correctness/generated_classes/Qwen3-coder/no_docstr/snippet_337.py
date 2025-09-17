class VerifierBase:
    def __init__(self, _key_type, _pubkey=None):
        self._key_type = _key_type
        self._pubkey = _pubkey

    @property
    def public_key(self) -> bytes:
        return self._pubkey

    def _verify(self, _message: bytes, _signature: bytes) -> bool:
        # This is a base implementation that should be overridden by subclasses
        raise NotImplementedError("_verify method must be implemented by subclass")

    def verify(self, message, signature, signature_format=None) -> bool:
        # Convert message to bytes if it isn't already
        if not isinstance(message, bytes):
            message = str(message).encode('utf-8')
        
        # Convert signature to bytes if it isn't already
        if not isinstance(signature, bytes):
            signature = bytes(signature)
            
        return self._verify(message, signature)