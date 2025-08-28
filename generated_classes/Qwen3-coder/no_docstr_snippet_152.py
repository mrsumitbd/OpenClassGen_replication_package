class Account(object):

    @classmethod
    def all(cls, client):
        """
        Retrieve all accounts for the given client.
        
        Args:
            client: The client object used to make the API request
            
        Returns:
            A list of Account objects
        """
        # Assuming there's an endpoint to fetch all accounts
        response = client.get('/accounts')
        accounts = []
        for account_data in response.get('data', []):
            accounts.append(cls(**account_data))
        return accounts

    @classmethod
    def all_urls(cls, client):
        """
        Retrieve all account URLs for the given client.
        
        Args:
            client: The client object used to make the API request
            
        Returns:
            A list of URLs for all accounts
        """
        # Assuming there's an endpoint to fetch account URLs
        response = client.get('/accounts/urls')
        return response.get('urls', [])