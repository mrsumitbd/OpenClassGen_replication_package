class BaseCrypto(object):
    '''提供接收和推送给公众平台消息的加解密接口'''

    def __init__(self, key):
        self.key = base64.b64decode(key + '=')
        self.iv = self.key[:16]
        self.block_size = 32

    def encrypt(self, text, appid):
        # 随机填充
        random_str = self.get_random_str().encode('utf-8')
        text_bytes = text.encode('utf-8')
        appid_bytes = appid.encode('utf-8')
        msg_len = struct.pack('!I', len(text_bytes))
        raw = random_str + msg_len + text_bytes + appid_bytes
        # PKCS7 Padding
        pad_len = self.block_size - (len(raw) % self.block_size)
        raw += bytes([pad_len]) * pad_len
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted = cipher.encrypt(raw)
        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt(self, text, appid):
        cipher_data = base64.b64decode(text)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted = cipher.decrypt(cipher_data)
        # 去除填充
        pad_len = decrypted[-1]
        decrypted = decrypted[:-pad_len]
        # 提取
        content = decrypted[16:]
        msg_len = struct.unpack('!I', content[:4])[0]
        xml_msg = content[4:4+msg_len]
        recv_appid = content[4+msg_len:].decode('utf-8')
        if recv_appid != appid:
            raise ValueError("AppID mismatch")
        return xml_msg.decode('utf-8')

    def get_random_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))