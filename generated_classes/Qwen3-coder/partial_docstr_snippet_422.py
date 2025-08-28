class BulkUserRetirement:
    '''
    API client for interacting with user retirement API
    '''

    def __init__(self, requester, base_url):
        self.requester = requester
        self.base_url = base_url.rstrip('/')

    def retire_users(self, payload):
        '''
        Execute the client request to edX endpoint

        Args:
            payload (dict): request payload

        Returns:
            JSON response (dict)
        '''
        url = f"{self.base_url}/api/bulk_user_retirement/"
        response = self.requester.post(url, json=payload)
        return response.json()