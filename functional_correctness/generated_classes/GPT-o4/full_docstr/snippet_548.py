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
        self.httpclient = httpclient
        self.resource_factory = getattr(config, 'resource_factory', None)
        self.base_url = getattr(config, 'base_url', '').rstrip('/')
        self.user_agent = getattr(config, 'user_agent', 'python-dispatcher/1.0')

    def invoke(self, request):
        '''Invoke the given :class:`.Request` instance using the associated :class:`.Dispatcher`.

        :param request: :class:`.Request` instance to invoke.
        :return: :class:`.Resource` subclass.
        '''
        # Build URL
        path = request.path.lstrip('/')
        url = urljoin(self.base_url + '/', path)

        # Build headers
        headers = self.get_headers()
        if hasattr(request, 'headers') and request.headers:
            headers.update(request.headers)

        # Prepare request arguments
        method = request.method.upper()
        params = getattr(request, 'params', None)
        data = getattr(request, 'data', None)
        json_body = getattr(request, 'json', None)

        # Dispatch HTTP request
        response = self.httpclient.request(
            method,
            url,
            headers=headers,
            params=params,
            data=data,
            json=json_body,
            timeout=getattr(self.config, 'timeout', None)
        )
        # Raise for HTTP errors
        try:
            response.raise_for_status()
        except AttributeError:
            # Fallback if httpclient.request returns a tuple or custom response
            if not (200 <= response.status_code < 300):
                raise

        # Process empty responses
        content = getattr(response, 'content', None)
        if content is None or (isinstance(content, (bytes, str)) and len(content) == 0):
            return None

        # Parse JSON
        try:
            payload = response.json()
        except (ValueError, AttributeError):
            payload = None

        # Delegate to resource factory
        if self.resource_factory and hasattr(request, 'resource_class'):
            return self.resource_factory.create(request.resource_class, payload)
        return payload

    def get_headers(self):
        '''Create and return a base set of headers to be carried with all requests.

        :return: dict containing header values.
        '''
        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'application/json'
        }
        # Allow additional default headers from config
        extra = getattr(self.config, 'default_headers', {})
        if isinstance(extra, dict):
            headers.update(extra)
        return headers