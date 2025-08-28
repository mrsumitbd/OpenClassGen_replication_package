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
        url = self.base_url + request.path
        headers = self.get_headers()
        headers.update(request.headers or {})
        
        if request.method == 'GET':
            response = self.httpclient.get(url, headers=headers, params=request.params)
        elif request.method == 'POST':
            response = self.httpclient.post(url, headers=headers, data=request.data, json=request.json)
        elif request.method == 'PUT':
            response = self.httpclient.put(url, headers=headers, data=request.data, json=request.json)
        elif request.method == 'DELETE':
            response = self.httpclient.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {request.method}")
        
        return self.resource_factory.create(response.json())

    def get_headers(self):
        '''Create and return a base set of headers to be carried with all requests.

        :return: dict containing header values.
        '''
        return {
            'User-Agent': self.user_agent,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }