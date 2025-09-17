class _BaseCancelOperation:

    def __hash__(self):
        return hash(self.__class__.__name__)

    @staticmethod
    def _get_http_options():
        return {
            'method': 'POST',
            'uri': '/v1/{name=operations/**}:cancel',
            'body': '*'
        }

    @staticmethod
    def _get_transcoded_request(http_options, request):
        transcoded_request = {
            'uri': http_options['uri'].format(name=request.name),
            'method': http_options['method'],
            'query_params': {},
            'body': request
        }
        return transcoded_request

    @staticmethod
    def _get_query_params_json(transcoded_request):
        query_params = transcoded_request.get('query_params', {})
        return {key: str(value) for key, value in query_params.items()}