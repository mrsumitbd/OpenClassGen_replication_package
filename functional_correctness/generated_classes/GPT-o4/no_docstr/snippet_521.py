class Account(object):
    DEFAULT_BASE_URL = "https://api.example.com"
    SUPPORTED_REGIONS = ["us-east-1", "us-west-1", "eu-central-1", "ap-southeast-1"]

    def __init__(self, api_version, base_url=None, creds=None):
        self.api_version = api_version
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.creds = creds or {}
        self._accounts = {}

    def create_account(self, collection_name, preferred_region):
        if preferred_region not in self.SUPPORTED_REGIONS:
            raise ValueError(f"Region '{preferred_region}' is not supported.")
        account_id = str(uuid.uuid4())
        account = {
            "id": account_id,
            "collection_name": collection_name,
            "preferred_region": preferred_region,
            "api_version": self.api_version,
        }
        self._accounts[account_id] = account
        return account

    def regions(self):
        return list(self.SUPPORTED_REGIONS)