class CpcSetAutoStartListHandler:
    '''
    Handler class for operation: Set Auto-start List.
    '''

    @staticmethod
    def post(method, hmc, uri, uri_parms, body, logon_required,
             wait_for_completion):
        '''Operation: Set Auto-start List.'''
        # Validate URI parameters
        if not isinstance(uri_parms, dict) or 'cpc-id' not in uri_parms:
            raise ValueError("Missing or invalid URI parameter: cpc-id")

        # Validate request body
        if not isinstance(body, dict) or 'auto-start-list' not in body:
            raise ValueError("Request body must be a dict containing the 'auto-start-list' property")

        # Send the request
        response = hmc.session.request(
            method,
            uri,
            uri_parms=uri_parms,
            body=body
        )

        # Handle the response (including re-login if needed)
        hmc._handle_response(response, logon_required)

        # This operation is synchronous; no job to wait on
        return None