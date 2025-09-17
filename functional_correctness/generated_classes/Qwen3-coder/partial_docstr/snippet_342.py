class BaseCrypto(object):
    '''提供接收和推送给公众平台消息的加解密接口'''

    def __init__(self, key):
        # 将key进行base64解码，得到AES密钥
        self.key = base64.b64decode(key + "=")
        self.iv = self.key[:16]

    def encrypt(self, text, appid):
        '''对明文进行加密

        @param text: 需要加密的明文
        @return: 加密得到的字符串
        '''
        # 生成16位随机字符串
        random_str = self.get_random_str()
        
        # 获取文本长度
        text_length = len(text)
        
        # 拼接明文字符串
        plaintext = random_str + str(text_length).zfill(8) + text + appid
        
        # 补位操作
        amount_to_pad = AES.block_size - (len(plaintext) % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad_chr = chr(amount_to_pad)
        plaintext += pad_chr * amount_to_pad
        
        # AES加密
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        ciphertext = cipher.encrypt(plaintext.encode('utf-8'))
        
        # base64编码
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, text, appid):
        '''对解密后的明文进行补位删除

        @param text: 密文
        @return: 删除填充补位后的明文
        '''
        # base64解码
        ciphertext = base64.b64decode(text)
        
        # AES解密
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        plaintext = cipher.decrypt(ciphertext).decode('utf-8')
        
        # 去除补位
        pad = ord(plaintext[-1])
        plaintext = plaintext[:-pad]
        
        # 提取信息
        random_str = plaintext[:16]
        msg_len = int(plaintext[16:24])
        msg = plaintext[24:24+msg_len]
        appid_from_msg = plaintext[24+msg_len:]
        
        # 验证appid
        if appid_from_msg != appid:
            raise Exception("Invalid appid")
        
        return msg

    def get_random_str(self):
        ''' 随机生成16位字符串

        @return: 16位字符串
        '''
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))