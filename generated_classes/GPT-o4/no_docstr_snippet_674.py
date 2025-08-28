class _BaseGetIamPolicy:

    def __hash__(self):
        return hash(tuple(tuple(sorted(option.items())) for option in self._get_http_options()))

    @staticmethod
    def _get_http_options():
        return [
            {
                "method": "post",
                "uri": "/v1/{resource}:getIamPolicy",
                "body": "*"
            }
        ]

    @staticmethod
    def _get_transcoded_request(http_options, request):
        return path_template.transcode(http_options, **request)

    @staticmethod
    def _get_query_params_json(transcoded_request):
        return json.loads(MessageToJson(transcoded_request["query_params"]))