class Client(object):
    def __init__(self, url, principal=None):
        self.base_url = url.rstrip('/')
        self.session = requests.Session()
        if isinstance(principal, tuple) and len(principal) == 2:
            self.session.auth = principal
        elif isinstance(principal, str):
            self.session.headers.update({'Authorization': f'Bearer {principal}'})

    def list_all_entities(self, ent_name):
        results = []
        next_url = f"{self.base_url}/{ent_name.lstrip('/')}"
        while next_url:
            resp = self.session.get(next_url)
            resp.raise_for_status()
            data = resp.json()

            # Hydra style
            if isinstance(data, dict) and 'hydra:member' in data:
                members = data['hydra:member']
            # Generic items field
            elif isinstance(data, dict) and 'items' in data:
                members = data['items']
            # Direct list
            elif isinstance(data, list):
                members = data
            else:
                raise ValueError("Unsupported response format for listing entities")

            results.extend(members)

            # Check HTTP Link header
            link_next = resp.links.get('next', {}).get('url')
            if link_next:
                next_url = link_next
                continue

            # Check Hydra pagination
            view = data.get('hydra:view', {})
            hydra_next = view.get('hydra:next')
            if hydra_next:
                next_url = hydra_next if hydra_next.startswith('http') else self.base_url + hydra_next
            else:
                next_url = None

        return results