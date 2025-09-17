class Account(object):
    def __init__(self, **data):
        for k, v in data.items():
            setattr(self, k, v)

    @classmethod
    def all(cls, client):
        accounts = client.paginate('/accounts', 'accounts')
        return [cls(**acct) for acct in accounts]

    @classmethod
    def all_urls(cls, client):
        accounts = client.paginate('/accounts', 'accounts')
        return [acct.get('url') for acct in accounts]