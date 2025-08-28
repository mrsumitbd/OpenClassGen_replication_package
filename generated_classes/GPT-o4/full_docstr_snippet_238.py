class IApi:
    '''Interface to an Api implementation'''

    def __init__(self, base_url, timeout=30, headers=None):
        """
        :param base_url: Base URL for REST API endpoints
        :param timeout:  Request timeout in seconds
        :param headers:  Optional dict of HTTP headers
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)
        self._logger = logging.getLogger(self.__class__.__name__)

    def shutdown(self):
        """Override to perform any shutdown necessary"""
        try:
            self.session.close()
            self._logger.debug("HTTP session closed")
        except Exception as e:
            self._logger.warning(f"Error shutting down session: {e}")

    def call(self, method, data=None, **args):
        """
        Generic interface to REST api
        :param method:  query name (appended to base_url)
        :param data:    dictionary of inputs
        :param args:    keyword arguments added to the payload
        :return:        parsed JSON response
        """
        url = f"{self.base_url}/{method.lstrip('/')}"
        payload = {}
        if data:
            if not isinstance(data, dict):
                raise ValueError("data must be a dict")
            payload.update(data)
        payload.update(args)
        try:
            resp = self.session.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            self._logger.error(f"API call error {method}: {e}")
            raise

    def on_ws_connect(self):
        """
        Called by the websocket mixin
        """
        self._logger.info("WebSocket connection established")