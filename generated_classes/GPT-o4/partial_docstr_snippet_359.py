class Encoder(object):
    '''
    Base class for a encoder employing an identity function.

    Args:
        enforce_reversible (bool, optional): Check for reversibility on ``Encoder.encode`` and
          ``Encoder.decode``. Formally, reversible means:
          ``Encoder.decode(Encoder.encode(object_)) == object_``.
    '''

    def __init__(self, enforce_reversible=False):
        self.enforce_reversible = enforce_reversible

    def encode(self, object_):
        '''
        Encodes an object.

        Args:
            object_ (object): Object to encode.

        Returns:
            object: Encoding of the object.
        '''
        encoded = object_
        if self.enforce_reversible:
            decoded = self.decode(encoded)
            if decoded != object_:
                raise ValueError(f"Reversibility check failed: decode(encode(obj)) != obj (got {decoded!r} != {object_!r})")
        return encoded

    def batch_encode(self, iterator, *args, **kwargs):
        '''
        Args:
            batch (list): Batch of objects to encode.
            *args: Arguments passed to ``encode``.
            **kwargs: Keyword arguments passed to ``encode``.

        Returns:
            list: Batch of encoded objects.
        '''
        return [self.encode(item) for item in iterator]

    def decode(self, encoded):
        '''
        Decodes an object.

        Args:
            object_ (object): Encoded object.

        Returns:
            object: Object decoded.
        '''
        decoded = encoded
        if self.enforce_reversible:
            reencoded = self.encode(decoded)
            if reencoded != encoded:
                raise ValueError(f"Reversibility check failed: encode(decode(enc)) != enc (got {reencoded!r} != {encoded!r})")
        return decoded

    def batch_decode(self, iterator, *args, **kwargs):
        '''
        Args:
            iterator (list): Batch of encoded objects.
            *args: Arguments passed to ``decode``.
            **kwargs: Keyword arguments passed to ``decode``.

        Returns:
            list: Batch of decoded objects.
        '''
        return [self.decode(item) for item in iterator]