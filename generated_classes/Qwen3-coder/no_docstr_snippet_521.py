class Account(object):
    def __init__(self, api_version, base_url=None, creds=None):
        self.api_version = api_version
        self.base_url = base_url or "https://api.example.com"
        self.creds = creds
        self.accounts = {}
        self.available_regions = ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"]

    def create_account(self, collection_name, preferred_region):
        if preferred_region not in self.available_regions:
            raise ValueError(f"Region {preferred_region} is not available")
        
        account_id = f"acc_{len(self.accounts) + 1:04d}"
        account = {
            "id": account_id,
            "collection_name": collection_name,
            "region": preferred_region,
            "status": "active"
        }
        self.accounts[account_id] = account
        return account

    def regions(self):
        return self.available_regions