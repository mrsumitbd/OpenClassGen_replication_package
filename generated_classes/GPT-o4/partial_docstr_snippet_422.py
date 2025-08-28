class BulkUserRetirement:
    """
    API client for interacting with user retirement API
    """

    def __init__(self, requester, base_url):
        """
        Args:
            requester: an HTTP client with a .post() method
            base_url (str): full URL of the bulk retirement endpoint
        """
        self.requester = requester
        self.base_url = base_url.rstrip("/")

    def retire_users(self, payload):
        """
        Execute the client request to edX endpoint

        Args:
            payload (dict): request payload

        Returns:
            JSON response (dict)
        """
        url = self.base_url
        response = self.requester.post(url, json=payload)
        response.raise_for_status()
        return response.json()