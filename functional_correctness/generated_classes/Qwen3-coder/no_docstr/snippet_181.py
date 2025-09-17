class _BaseListOperations:
    def __hash__(self):
        return hash(id(self))

    @staticmethod
    def _get_http_options():
        return {}

    @staticmethod
    def _get_transcoded_request(http_options, request):
        return request

    @staticmethod
    def _get_query_params_json(transcoded_request):
        return {}