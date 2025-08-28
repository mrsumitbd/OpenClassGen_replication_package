class _BaseGetFeature:

    def __hash__(self):
        return object.__hash__(self)

    @staticmethod
    def _get_http_options():
        return [
            {
                "method": "get",
                "uri": "/v1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*}",
            }
        ]

    @staticmethod
    def _get_transcoded_request(http_options, request):
        return transcode(http_options, request)

    @staticmethod
    def _get_query_params_json(transcoded_request):
        params = transcoded_request.get("query_params", {})
        # Filter out None values
        filtered = {k: v for k, v in params.items() if v is not None}
        return json.loads(
            json.dumps(
                filtered,
                default=lambda o: o.value if hasattr(o, "value") else o,
            )
        )