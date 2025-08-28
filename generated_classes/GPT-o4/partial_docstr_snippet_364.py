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
        if not isinstance(conf, dict):
            raise ValueError("conf must be a dict")
        for key in ("hostname", "port", "username", "password"):
            if key not in conf:
                raise KeyError(f"missing required conf field: {key}")
        self._conf = conf
        self._handler = None
        self._client = mqtt.Client()
        user = conf.get("username") or None
        pwd = conf.get("password") or None
        if user is not None:
            self._client.username_pw_set(user, pwd)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        # 连接建立后订阅所有主题，可根据需要改为特定主题
        client.subscribe("#")

    def _on_message(self, client, userdata, msg):
        if self._handler:
            try:
                self._handler(msg.topic, msg.payload)
            except Exception:
                pass

    def run(self, handler=None):
        '''
        开始运行，handler 为回调函数，签名为 func(topic, payload)
        '''
        self._handler = handler
        self._client.connect(self._conf["hostname"], self._conf["port"])
        self._client.loop_forever()