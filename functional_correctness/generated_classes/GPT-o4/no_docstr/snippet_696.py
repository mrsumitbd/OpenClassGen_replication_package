class _BaseCancelOperation:

    def __hash__(self):
        return id(self)

    @staticmethod
    def _get_http_options():
        return [
            {
                "method": "post",
                "uri": "/v1/{name=projects/*/operations/*}:cancel",
                "body": "*",
            },
        ]

    @staticmethod
    def _get_transcoded_request(http_options, request):
        # Convert protobuf Message to dict if necessary
        if not isinstance(request, dict):
            try:
                request_dict = json_format.MessageToDict(
                    request,
                    including_default_value_fields=False,
                    preserving_proto_field_name=True,
                )
            except Exception:
                # Fallback for simple dataclasses or mappings
                request_dict = dict(request)
        else:
            request_dict = request
        return path_template.transcode(http_options, request_dict)

    @staticmethod
    def _get_query_params_json(transcoded_request):
        query_params = transcoded_request.get("query_params", {})
        return json.dumps(query_params)