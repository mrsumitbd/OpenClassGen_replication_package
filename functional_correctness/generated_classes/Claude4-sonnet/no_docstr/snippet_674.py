class _BaseGetIamPolicy:

    def __hash__(self):
        return hash(type(self))

    @staticmethod
    def _get_http_options():
        return [
            {
                "method": "post",
                "uri": "/v1/{resource=projects/*/locations/*/datasets/*}:getIamPolicy",
                "body": "*",
            },
            {
                "method": "post", 
                "uri": "/v1/{resource=projects/*/locations/*/datasets/*/dicomStores/*}:getIamPolicy",
                "body": "*",
            },
            {
                "method": "post",
                "uri": "/v1/{resource=projects/*/locations/*/datasets/*/fhirStores/*}:getIamPolicy", 
                "body": "*",
            },
            {
                "method": "post",
                "uri": "/v1/{resource=projects/*/locations/*/datasets/*/hl7V2Stores/*}:getIamPolicy",
                "body": "*",
            },
        ]

    @staticmethod
    def _get_transcoded_request(http_options, request):
        pb_request = request
        transcoded_request = {}
        
        if hasattr(pb_request, 'resource'):
            transcoded_request['resource'] = pb_request.resource
        
        body = {}
        if hasattr(pb_request, 'options'):
            body['options'] = pb_request.options
            
        transcoded_request['body'] = body
        transcoded_request['method'] = http_options.get('method', 'post')
        transcoded_request['uri'] = http_options.get('uri', '')
        
        return transcoded_request

    @staticmethod
    def _get_query_params_json(transcoded_request):
        query_params = {}
        body = transcoded_request.get('body', {})
        
        if 'options' in body:
            options = body['options']
            if hasattr(options, 'requested_policy_version'):
                query_params['options.requestedPolicyVersion'] = options.requested_policy_version
                
        return query_params