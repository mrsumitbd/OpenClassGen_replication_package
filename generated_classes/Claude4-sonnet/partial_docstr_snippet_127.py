class Witness:
    def __init__(self, invocation_script=None, verification_script=None):
        self._invocation_script = invocation_script or b''
        self._verification_script = verification_script or b''

    @property
    def VerificationScript(self):
        return self._verification_script

    @VerificationScript.setter
    def VerificationScript(self, value):
        self._verification_script = value

    @property
    def InvocationScript(self):
        return self._invocation_script

    @InvocationScript.setter
    def InvocationScript(self, value):
        self._invocation_script = value