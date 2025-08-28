class Topic(object):
    '''
        初始化 ``topic`` 连接的配置

    .. code:: python

        # 配置文件需要包含如下字段
        conf = {
            "hostname": "127.0.0.1",
            "port": 1883,
            "username": "",
            "password": ""
        }

    '''

    def __init__(self, conf=None):
        self.conf = conf or {}
        self.hostname = self.conf.get("hostname", "127.0.0.1")
        self.port = self.conf.get("port", 1883)
        self.username = self.conf.get("username", "")
        self.password = self.conf.get("password", "")
        self.client = mqtt.Client()
        
        if self.username:
            self.client.username_pw_set(self.username, self.password)
        
        self.handler = None

    def run(self, handler=None):
        self.handler = handler
        
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                client.subscribe("#")
        
        def on_message(client, userdata, msg):
            if self.handler:
                try:
                    payload = msg.payload.decode('utf-8')
                    self.handler(msg.topic, payload)
                except Exception as e:
                    pass
        
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        
        self.client.connect(self.hostname, self.port, 60)
        self.client.loop_forever()