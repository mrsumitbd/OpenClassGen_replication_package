class MleMessageFactory:

    def __init__(self, aux_sec_hdr_factory, mle_command_factory, crypto_engine):
        self.aux_sec_hdr_factory = aux_sec_hdr_factory
        self.mle_command_factory = mle_command_factory
        self.crypto_engine = crypto_engine

    def _create_mle_secured_message(self, data, message_info):
        # first build the plaintext MLE payload
        plaintext = self.mle_command_factory.create(data, message_info)
        # build the auxiliary security header
        aux_hdr = self.aux_sec_hdr_factory.create(message_info)
        # derive encryption parameters
        key = self.crypto_engine.get_key(message_info, aux_hdr)
        nonce = aux_hdr.nonce
        aad = aux_hdr.header
        # encrypt
        ciphertext = self.crypto_engine.encrypt(plaintext, key, nonce, aad)
        # prepend AAD/header to ciphertext
        return aad + ciphertext

    def _create_mle_message(self, data, message_info):
        # build an unsecured MLE payload
        return self.mle_command_factory.create(data, message_info)

    def parse(self, data, message_info):
        # determine whether the incoming message is secured
        if getattr(message_info, 'security_enabled', False):
            # parse and strip the auxiliary security header
            aux_hdr, header_len = self.aux_sec_hdr_factory.parse(data)
            aad = data[:header_len]
            ciphertext = data[header_len:]
            # derive decryption parameters
            key = self.crypto_engine.get_key(message_info, aux_hdr)
            nonce = aux_hdr.nonce
            # decrypt
            plaintext = self.crypto_engine.decrypt(ciphertext, key, nonce, aad)
            # parse the decrypted MLE command
            command = self.mle_command_factory.parse(plaintext, message_info)
            return {'aux_sec_hdr': aux_hdr, 'command': command}
        else:
            # parse an unsecured MLE command directly
            command = self.mle_command_factory.parse(data, message_info)
            return {'command': command}