class _BaseGetFeature:

    def __hash__(self):
        return hash(type(self))

    @staticmethod
    def _get_http_options():
        return {
            'method': 'GET',
            'uri': '/v1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*}',
        }

    @staticmethod
    def _get_transcoded_request(http_options, request):
        transcoded_request = {
            'uri': http_options['uri'].format(name=request.name),
            'method': http_options['method'],
            'query_params': {},
        }
        return transcoded_request

    @staticmethod
    def _get_query_params_json(transcoded_request):
        query_params = transcoded_request.get('query_params', {})
        return {key: value for key, value in query_params.items() if value is not None}