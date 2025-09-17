class WechatRequest(object):
    ''' WechatRequest 请求类

    对微信服务器的请求响应处理进行封装
    '''

    def __init__(self, conf=None):
        '''
        :param conf: WechatConf 配置类实例
        '''
        self.conf = conf

    def request(self, method, url, access_token=None, **kwargs):
        '''
        向微信服务器发送请求
        :param method: 请求方法
        :param url: 请求地址
        :param access_token: access token 值, 如果初始化时传入 conf 会自动获取, 如果没有传入则请提供此值
        :param kwargs: 附加数据
        :return: 微信服务器响应的 JSON 数据
        '''
        token = access_token or (self.conf.get_access_token() if self.conf else None)
        if not token:
            raise ValueError("Access token is required")
        method = method.upper()
        params = {"access_token": token}
        if method == "GET":
            params.update(kwargs)
            resp = requests.get(url, params=params)
        else:
            resp = requests.request(method, url, params=params, json=kwargs)
        resp.raise_for_status()
        data = resp.json()
        self._check_official_error(data)
        return data

    def get(self, url, access_token=None, **kwargs):
        '''
        使用 GET 方法向微信服务器发出请求
        :param url: 请求地址
        :param access_token: access token 值, 如果初始化时传入 conf 会自动获取, 如果没有传入则请提供此值
        :param kwargs: 附加数据
        :return: 微信服务器响应的 JSON 数据
        '''
        return self.request("GET", url, access_token=access_token, **kwargs)

    def post(self, url, access_token=None, **kwargs):
        '''
        使用 POST 方法向微信服务器发出请求
        :param url: 请求地址
        :param access_token: access token 值, 如果初始化时传入 conf 会自动获取, 如果没有传入则请提供此值
        :param kwargs: 附加数据
        :return: 微信服务器响应的 JSON 数据
        '''
        return self.request("POST", url, access_token=access_token, **kwargs)

    def _check_official_error(self, json_data):
        '''
        检测微信公众平台返回值中是否包含错误的返回码
        :raises OfficialAPIError: 如果返回码提示有错误，抛出异常；否则返回 True
        '''
        errcode = json_data.get("errcode")
        if errcode and errcode != 0:
            errmsg = json_data.get("errmsg", "")
            raise OfficialAPIError(errcode, errmsg)
        return True