class BaseCrypto(object):
    '''提供接收和推送给公众平台消息的加解密接口'''

    def __init__(self, key):
        self.key = base64.b64decode(key + "=")
        self.mode = AES.MODE_CBC

    def encrypt(self, text, appid):
        '''对明文进行加密

        @param text: 需要加密的明文
        @return: 加密得到的字符串
        '''
        text = text.encode('utf-8')
        random_str = self.get_random_str().encode('utf-8')
        text_length = struct.pack("I", socket.htonl(len(text)))
        appid = appid.encode('utf-8')
        
        content = random_str + text_length + text + appid
        content_length = len(content)
        
        # PKCS7 padding
        pad_length = 32 - (content_length % 32)
        if pad_length == 0:
            pad_length = 32
        
        padded_content = content + (chr(pad_length) * pad_length).encode('utf-8')
        
        iv = self.key[:16]
        cipher = AES.new(self.key, self.mode, iv)
        encrypted = cipher.encrypt(padded_content)
        
        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt(self, text, appid):
        '''对解密后的明文进行补位删除

        @param text: 密文
        @return: 删除填充补位后的明文
        '''
        cipher_text = base64.b64decode(text)
        iv = self.key[:16]
        cipher = AES.new(self.key, self.mode, iv)
        decrypted = cipher.decrypt(cipher_text)
        
        # Remove padding
        pad_length = decrypted[-1]
        if isinstance(pad_length, str):
            pad_length = ord(pad_length)
        
        content = decrypted[:-pad_length]
        
        # Extract components
        random_str = content[:16]
        text_length = struct.unpack("I", socket.ntohl(struct.unpack("I", content[16:20])[0]).to_bytes(4, 'big'))[0]
        text = content[20:20+text_length]
        from_appid = content[20+text_length:]
        
        return text.decode('utf-8')

    def get_random_str(self):
        ''' 随机生成16位字符串

        @return: 16位字符串
        '''
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))