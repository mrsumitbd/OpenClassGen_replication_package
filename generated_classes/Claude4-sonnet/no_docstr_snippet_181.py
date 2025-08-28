class _BaseListOperations:

    def __hash__(self):
        return hash(id(self))

    @staticmethod
    def _get_http_options():
        return {
            'method': 'GET',
            'headers': {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        }

    @staticmethod
    def _get_transcoded_request(http_options, request):
        transcoded_request = {
            'method': http_options.get('method', 'GET'),
            'headers': http_options.get('headers', {}),
            'url': getattr(request, 'url', ''),
            'params': getattr(request, 'params', {}),
            'body': getattr(request, 'body', None)
        }
        return transcoded_request

    @staticmethod
    def _get_query_params_json(transcoded_request):
        params = transcoded_request.get('params', {})
        if not params:
            return '{}'
        
        import json
        return json.dumps(params, separators=(',', ':'))