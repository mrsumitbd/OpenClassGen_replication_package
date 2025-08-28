class _BaseGetIamPolicy:

    def __hash__(self):
        return hash(type(self).__name__)

    @staticmethod
    def _get_http_options():
        return [
            {
                "method": "GET",
                "uri": "/v1/{resource=**}:getIamPolicy",
            },
        ]

    @staticmethod
    def _get_transcoded_request(http_options, request):
        transcoded_request = http_options[0].copy()
        uri = transcoded_request["uri"]
        
        # Extract resource from request
        resource = getattr(request, "resource", "")
        if resource:
            uri = uri.replace("{resource=**}", resource)
        
        transcoded_request["uri"] = uri
        return transcoded_request

    @staticmethod
    def _get_query_params_json(transcoded_request):
        query_params = {}
        
        # Extract query parameters from URI if present
        uri = transcoded_request.get("uri", "")
        if "?" in uri:
            query_string = uri.split("?", 1)[1]
            for param in query_string.split("&"):
                if "=" in param:
                    key, value = param.split("=", 1)
                    query_params[key] = value
        
        return query_params