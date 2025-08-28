class PickleCodec(object):
    '''
    Basic codec using pickle (default version) for encoding. Do not use if 
    cross-language support is desired.
    '''

    @staticmethod
    def encode(obj):
        return pickle.dumps(obj)

    @staticmethod
    def decode(enc):
        return pickle.loads(enc)