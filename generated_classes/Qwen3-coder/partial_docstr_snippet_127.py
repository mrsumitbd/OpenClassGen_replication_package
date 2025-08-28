class Witness:
    def __init__(self, verification_script=None, invocation_script=None):
        self._verification_script = verification_script
        self._invocation_script = invocation_script

    @property
    def VerificationScript(self):
        '''
        :return:
        '''
        return self._verification_script

    @property
    def InvocationScript(self):
        '''
        :return:
        '''
        return self._invocation_script

    @VerificationScript.setter
    def VerificationScript(self, value):
        self._verification_script = value

    @InvocationScript.setter
    def InvocationScript(self, value):
        self._invocation_script = value

    def __eq__(self, other):
        if not isinstance(other, Witness):
            return False
        return (self._verification_script == other._verification_script and
                self._invocation_script == other._invocation_script)

    def __hash__(self):
        return hash((self._verification_script, self._invocation_script))

    def __repr__(self):
        return f"Witness(VerificationScript={self._verification_script}, InvocationScript={self._invocation_script})"