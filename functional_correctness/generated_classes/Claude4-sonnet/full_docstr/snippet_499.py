class LicenseManager(object):
    '''
    @summary: handle license automata (client side)
    @see: http://msdn.microsoft.com/en-us/library/cc241890.aspx
    '''

    def __init__(self, transport):
        '''
        @param transport: layer use to send packet
        '''
        self.transport = transport
        self.state = "INITIAL"
        self.client_random = None
        self.server_random = None
        self.premaster_secret = None
        self.master_secret = None
        self.session_key_blob = None
        self.mac_salt_key = None
        self.licensing_encryption_key = None

    def recv(self, s):
        '''
        @summary: receive license packet from PDU layer
        @return true when license automata is finish
        '''
        if not s:
            return False
            
        packet_type = s[0] if len(s) > 0 else 0
        
        if packet_type == 0x01:  # LICENSE_REQUEST
            self.sendClientNewLicenseRequest(s)
            return False
        elif packet_type == 0x02:  # PLATFORM_CHALLENGE
            self.sendClientChallengeResponse(s)
            return False
        elif packet_type == 0x03:  # NEW_LICENSE
            self.state = "LICENSED"
            return True
        elif packet_type == 0x04:  # UPGRADE_LICENSE
            self.state = "LICENSED"
            return True
        elif packet_type == 0xFF:  # ERROR_ALERT
            self.state = "ERROR"
            return True
        
        return False

    def sendClientNewLicenseRequest(self, licenseRequest):
        '''
        @summary: Create new license request in response to server license request
        @param licenseRequest: {ServerLicenseRequest}
        @see: http://msdn.microsoft.com/en-us/library/cc241989.aspx
        @see: http://msdn.microsoft.com/en-us/library/cc241918.aspx
        '''
        import os
        import struct
        
        # Generate client random
        self.client_random = os.urandom(32)
        
        # Create client license info
        client_license_info = b"CLIENT_LICENSE_INFO"
        
        # Create client machine name
        machine_name = b"CLIENT_MACHINE"
        
        # Create client user name
        user_name = b"CLIENT_USER"
        
        # Build the packet
        packet = bytearray()
        packet.append(0x12)  # CLIENT_NEW_LICENSE_REQUEST
        packet.append(0x00)  # flags
        packet.extend(struct.pack('<H', len(packet) + 4))  # packet length placeholder
        
        # Add client random
        packet.extend(self.client_random)
        
        # Add client license info
        packet.extend(struct.pack('<H', len(client_license_info)))
        packet.extend(client_license_info)
        
        # Add machine name
        packet.extend(struct.pack('<H', len(machine_name)))
        packet.extend(machine_name)
        
        # Add user name
        packet.extend(struct.pack('<H', len(user_name)))
        packet.extend(user_name)
        
        # Update packet length
        struct.pack_into('<H', packet, 2, len(packet))
        
        self.transport.send(bytes(packet))
        self.state = "LICENSE_REQUEST_SENT"

    def sendClientChallengeResponse(self, platformChallenge):
        '''
        @summary: generate valid challenge response
        @param platformChallenge: {ServerPlatformChallenge}
        '''
        import os
        import struct
        import hashlib
        
        # Extract challenge data from platform challenge
        challenge_data = platformChallenge[4:] if len(platformChallenge) > 4 else b""
        
        # Generate response data
        response_data = hashlib.md5(challenge_data + self.client_random).digest()
        
        # Create hardware ID
        hardware_id = os.urandom(20)
        
        # Build the packet
        packet = bytearray()
        packet.append(0x15)  # CLIENT_PLATFORM_CHALLENGE_RESPONSE
        packet.append(0x00)  # flags
        packet.extend(struct.pack('<H', 0))  # packet length placeholder
        
        # Add response data length and data
        packet.extend(struct.pack('<H', len(response_data)))
        packet.extend(response_data)
        
        # Add hardware ID length and data
        packet.extend(struct.pack('<H', len(hardware_id)))
        packet.extend(hardware_id)
        
        # Update packet length
        struct.pack_into('<H', packet, 2, len(packet))
        
        self.transport.send(bytes(packet))
        self.state = "CHALLENGE_RESPONSE_SENT"