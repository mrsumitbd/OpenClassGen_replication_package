class MleMessageFactory:
    def __init__(self, aux_sec_hdr_factory, mle_command_factory, crypto_engine):
        self._aux_sec_hdr_factory = aux_sec_hdr_factory
        self._mle_command_factory = mle_command_factory
        self._crypto_engine = crypto_engine

    def _create_mle_secured_message(self, data, message_info):
        # Parse auxiliary security header
        aux_sec_hdr, offset = self._aux_sec_hdr_factory.parse(data, message_info)
        
        # Decrypt the payload
        encrypted_payload = data[offset:]
        decrypted_payload = self._crypto_engine.decrypt(encrypted_payload, message_info)
        
        # Parse the MLE command from decrypted payload
        mle_command = self._mle_command_factory.parse(decrypted_payload, message_info)
        
        # Create and return secured MLE message
        return {
            'aux_sec_hdr': aux_sec_hdr,
            'mle_command': mle_command,
            'is_secured': True
        }

    def _create_mle_message(self, data, message_info):
        # Parse MLE command directly from data
        mle_command = self._mle_command_factory.parse(data, message_info)
        
        # Create and return unsecured MLE message
        return {
            'mle_command': mle_command,
            'is_secured': False
        }

    def parse(self, data, message_info):
        # Check if message is secured by looking at message info or data structure
        if message_info.is_secured:
            return self._create_mle_secured_message(data, message_info)
        else:
            return self._create_mle_message(data, message_info)