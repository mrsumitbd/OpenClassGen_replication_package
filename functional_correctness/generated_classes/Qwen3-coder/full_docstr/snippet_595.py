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
        if access_token is None and self.conf is not None:
            access_token = self.conf.access_token
            
        if access_token:
            if '?' in url:
                url = '{}&access_token={}'.format(url, access_token)
            else:
                url = '{}?access_token={}'.format(url, access_token)
        
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        
        json_data = response.json()
        self._check_official_error(json_data)
        
        return json_data

    def get(self, url, access_token=None, **kwargs):
        '''
        使用 GET 方法向微信服务器发出请求
        :param url: 请求地址
        :param access_token: access token 值, 如果初始化时传入 conf 会自动获取, 如果没有传入则请提供此值
        :param kwargs: 附加数据
        :return: 微信服务器响应的 JSON 数据
        '''
        return self.request('GET', url, access_token, **kwargs)

    def post(self, url, access_token=None, **kwargs):
        '''
        使用 POST 方法向微信服务器发出请求
        :param url: 请求地址
        :param access_token: access token 值, 如果初始化时传入 conf 会自动获取, 如果没有传入则请提供此值
        :param kwargs: 附加数据
        :return: 微信服务器响应的 JSON 数据
        '''
        return self.request('POST', url, access_token, **kwargs)

    def _check_official_error(self, json_data):
        '''
        检测微信公众平台返回值中是否包含错误的返回码
        :raises OfficialAPIError: 如果返回码提示有错误，抛出异常；否则返回 True
        '''
        if 'errcode' in json_data and json_data['errcode'] != 0:
            errcode = json_data['errcode']
            errmsg = json_data.get('errmsg', '未知错误')
            raise OfficialAPIError('微信API错误: errcode={}, errmsg={}'.format(errcode, errmsg))
        return True