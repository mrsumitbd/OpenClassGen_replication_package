class _BaseListOperations:
    def __hash__(self):
        return hash(self.__class__)

    @staticmethod
    def _get_http_options():
        """
        Returns a list of HTTP option templates. Subclasses should override
        this method to provide specific method, uri, and body field names.
        """
        return []

    @staticmethod
    def _get_transcoded_request(http_options, request):
        """
        Transcode a request dict into an HTTP request description.
        Picks the first matching http_option, formats its URI with request
        values, extracts the body, and treats the rest as query parameters.
        """
        for option in http_options:
            method = option.get("method")
            uri_template = option.get("uri", "")
            body_field = option.get("body")

            # Fill URI template
            try:
                uri = uri_template.format(**request)
            except Exception:
                uri = uri_template

            # Extract body if specified
            body = None
            if body_field and body_field in request:
                body = request[body_field]

            # Determine which fields to exclude from query params
            excluded = set()
            if body_field:
                excluded.add(body_field)
            # Exclude any fields used in the URI template
            for key in request:
                if "{%s}" % key in uri_template:
                    excluded.add(key)

            # Build query params
            query_params = {
                k: v for k, v in request.items() if k not in excluded
            }

            return {
                "method": method,
                "uri": uri,
                "body": body,
                "query_params": query_params,
            }

        raise ValueError("No HTTP options provided for transcoding")

    @staticmethod
    def _get_query_params_json(transcoded_request):
        """
        Return a JSON-serializable dict of query parameters from the
        transcoded request.
        """
        qp = transcoded_request.get("query_params", {})
        try:
            # Ensure all values are JSON-serializable
            return json.loads(json.dumps(qp, default=lambda o: o.__dict__))
        except Exception:
            # Fallback to a shallow copy
            return dict(qp)