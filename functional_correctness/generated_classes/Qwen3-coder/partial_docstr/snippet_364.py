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
        self.client = mqtt.Client()
        
        # 设置认证信息
        if self.conf.get("username") and self.conf.get("password"):
            self.client.username_pw_set(self.conf["username"], self.conf["password"])
        
        # 设置连接回调
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        
        self.handler = None

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            # 订阅所有topic
            client.subscribe("#")
        else:
            print(f"Failed to connect, return code {rc}")

    def _on_message(self, client, userdata, msg):
        if self.handler:
            try:
                payload = msg.payload.decode('utf-8')
                # 尝试解析JSON
                try:
                    payload = json.loads(payload)
                except:
                    pass
                self.handler(msg.topic, payload)
            except Exception as e:
                print(f"Error in message handler: {e}")

    def run(self, handler=None):
        self.handler = handler
        try:
            self.client.connect(
                self.conf.get("hostname", "127.0.0.1"),
                self.conf.get("port", 1883),
                60
            )
            self.client.loop_forever()
        except KeyboardInterrupt:
            print("Interrupted")
            self.client.disconnect()
        except Exception as e:
            print(f"Error: {e}")
            self.client.disconnect()