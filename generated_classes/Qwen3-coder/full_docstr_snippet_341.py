class NullFernet:
    '''
    A "Null" encryptor class that doesn't encrypt or decrypt but that presents a similar interface to Fernet.

    The purpose of this is to make the rest of the code not have to know the
    difference, and to only display the message once, not 20 times when
    `airflow db migrate` is run.
    '''

    def decrypt(self, b):
        '''Decrypt with Fernet.'''
        return b

    def encrypt(self, b):
        '''Encrypt with Fernet.'''
        return b