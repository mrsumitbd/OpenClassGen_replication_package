class Witness:
    def __init__(self, verification_script: bytes = b''):
        self._verification_script = verification_script

    @property
    def VerificationScript(self) -> bytes:
        '''
        :return: the verification script as bytes
        '''
        return self._verification_script

    @VerificationScript.setter
    def VerificationScript(self, value: bytes):
        '''
        :param value: the new verification script as bytes
        '''
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError("VerificationScript must be bytes or bytearray")
        self._verification_script = bytes(value)