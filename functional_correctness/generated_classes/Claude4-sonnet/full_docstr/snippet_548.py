class Dispatcher(object):
    '''Responsible for invoking :class:`.Request` instances and delegating result processing.

    **Attributes**:

    - config (:class:`.Config`): Configuration settings.
    - resource_factory (:class:`.ResourceFactory`): Factory to use for generating resources out of JSON responses.
    - httpclient (module): HTTP client module.
    - base_url (str): Base URL of the remote endpoint.
    - user_agent (str): ``User-Agent`` header to pass with requests.
    '''

    def __init__(self, config, httpclient):
        '''Dispatcher constructor.

        :param config: Configuration container.
        :param httpclient: HTTP client.
        :return: :class:`.Dispatcher` instance.
        '''
        self.config = config
        self.resource_factory = config.resource_factory
        self.httpclient = httpclient
        self.base_url = config.base_url
        self.user_agent = config.user_agent

    def invoke(self, request):
        '''Invoke the given :class:`.Request` instance using the associated :class:`.Dispatcher`.

        :param request: :class:`.Request` instance to invoke.
        :return: :class:`.Resource` subclass.
        '''
        headers = self.get_headers()
        headers.update(request.headers or {})
        
        url = self.base_url + request.path
        
        response = self.httpclient.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.data,
            params=request.params
        )
        
        return self.resource_factory.create(response.json(), response.status_code, response.headers)

    def get_headers(self):
        '''Create and return a base set of headers to be carried with all requests.

        :return: dict containing header values.
        '''
        return {
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }