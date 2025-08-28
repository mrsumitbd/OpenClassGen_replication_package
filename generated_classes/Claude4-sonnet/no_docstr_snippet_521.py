class Account(object):
    def __init__(self, api_version, base_url=None, creds=None):
        self.api_version = api_version
        self.base_url = base_url or "https://api.example.com"
        self.creds = creds or {}
        self._regions_cache = None

    def create_account(self, collection_name, preferred_region):
        account_data = {
            'collection_name': collection_name,
            'preferred_region': preferred_region,
            'api_version': self.api_version,
            'created_at': self._get_timestamp(),
            'status': 'active'
        }
        return account_data

    def regions(self):
        if self._regions_cache is None:
            self._regions_cache = [
                'us-east-1',
                'us-west-2',
                'eu-west-1',
                'ap-southeast-1',
                'ap-northeast-1'
            ]
        return self._regions_cache

    def _get_timestamp(self):
        import datetime
        return datetime.datetime.utcnow().isoformat()