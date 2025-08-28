class LicenseManager(object):
    """
    @summary: handle license automata (client side)
    @see: http://msdn.microsoft.com/en-us/library/cc241890.aspx
    """

    # internal states
    _STATE_INIT = 0
    _STATE_NEW_LICENSE_SENT = 1
    _STATE_CHALLENGE_RESP_SENT = 2
    _STATE_FINISHED = 3
    _STATE_ERROR = -1

    def __init__(self, transport):
        """
        @param transport: layer use to send packet
        """
        self.transport = transport
        self._state = self._STATE_INIT

    def recv(self, s):
        """
        @summary: receive license packet from PDU layer
        @return true when license automata is finish
        """
        # detect packet type by class name
        clsname = s.__class__.__name__
        if self._state == self._STATE_INIT and clsname == 'ServerLicenseRequest':
            self.sendClientNewLicenseRequest(s)
            self._state = self._STATE_NEW_LICENSE_SENT
            return False
        elif self._state == self._STATE_NEW_LICENSE_SENT and clsname == 'ServerPlatformChallenge':
            self.sendClientChallengeResponse(s)
            self._state = self._STATE_CHALLENGE_RESP_SENT
            # after challenge response, client waits no further—finished
            self._state = self._STATE_FINISHED
            return True
        else:
            self._state = self._STATE_ERROR
            return True

    def sendClientNewLicenseRequest(self, licenseRequest):
        """
        @summary: Create new license request in response to server license request
        @param licenseRequest: {ServerLicenseRequest}
        @see: http://msdn.microsoft.com/en-us/library/cc241989.aspx
        @see: http://msdn.microsoft.com/en-us/library/cc241918.aspx
        """
        # build a ClientNewLicenseRequest PDU
        pdu = {
            'type': 'ClientNewLicenseRequest',
            'version': licenseRequest.version,
            'clientRandom': licenseRequest.clientRandom,
            'requestedProductId': licenseRequest.productId,
            'platformId': licenseRequest.platformId,
            'hardwareId': licenseRequest.hardwareId,
        }
        data = self._serialize_pdu(pdu)
        self.transport.send(data)

    def sendClientChallengeResponse(self, platformChallenge):
        """
        @summary: generate valid challenge response
        @param platformChallenge: {ServerPlatformChallenge}
        """
        # build a ClientPlatformChallengeResponse PDU
        # echo back serverRandom encrypted with client secret (stubbed here)
        resp = {
            'type': 'ClientPlatformChallengeResponse',
            'serverRandom': platformChallenge.serverRandom,
            'clientSecretProof': self._compute_proof(platformChallenge.serverRandom)
        }
        data = self._serialize_pdu(resp)
        self.transport.send(data)

    def _serialize_pdu(self, pdu):
        # stub serialization to bytes
        import json
        return json.dumps(pdu).encode('utf-8')

    def _compute_proof(self, serverRandom):
        # stubbed proof computation
        # in real implementation, would use licensing keys and HMAC
        return (serverRandom[::-1] + b'PROOF')[:16]