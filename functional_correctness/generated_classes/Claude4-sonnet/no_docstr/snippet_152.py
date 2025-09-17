class Account(object):
    def __init__(self, client, data=None):
        self.client = client
        self.data = data or {}
    
    @classmethod
    def all(cls, client):
        accounts = []
        urls = cls.all_urls(client)
        for url in urls:
            response = client.get(url)
            if response and 'accounts' in response:
                for account_data in response['accounts']:
                    accounts.append(cls(client, account_data))
        return accounts

    @classmethod
    def all_urls(cls, client):
        response = client.get('/accounts')
        if response and 'urls' in response:
            return response['urls']
        return []