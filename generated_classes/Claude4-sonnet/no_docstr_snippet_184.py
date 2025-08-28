class MleMessageFactory:

    def __init__(self, aux_sec_hdr_factory, mle_command_factory, crypto_engine):
        self._aux_sec_hdr_factory = aux_sec_hdr_factory
        self._mle_command_factory = mle_command_factory
        self._crypto_engine = crypto_engine

    def _create_mle_secured_message(self, data, message_info):
        aux_sec_hdr = self._aux_sec_hdr_factory.parse(data, message_info)
        
        encrypted_data = data[aux_sec_hdr.get_length():]
        decrypted_data = self._crypto_engine.decrypt(encrypted_data, aux_sec_hdr, message_info)
        
        command = self._mle_command_factory.parse(decrypted_data, message_info)
        
        return MleSecuredMessage(aux_sec_hdr, command)

    def _create_mle_message(self, data, message_info):
        command = self._mle_command_factory.parse(data, message_info)
        return MleMessage(command)

    def parse(self, data, message_info):
        if len(data) == 0:
            raise ValueError("Empty data")
        
        security_suite = data[0]
        
        if security_suite == 0:
            return self._create_mle_message(data[1:], message_info)
        else:
            return self._create_mle_secured_message(data[1:], message_info)