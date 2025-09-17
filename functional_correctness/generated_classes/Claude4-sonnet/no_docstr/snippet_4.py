class Client(object):

    def __init__(self, url, principal=None):
        self.url = url.rstrip('/')
        self.principal = principal
        self.session = requests.Session()
        if principal:
            self.session.headers.update({'Authorization': f'Bearer {principal}'})

    def list_all_entities(self, ent_name):
        endpoint = f"{self.url}/entities/{ent_name}"
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to list entities: {str(e)}")