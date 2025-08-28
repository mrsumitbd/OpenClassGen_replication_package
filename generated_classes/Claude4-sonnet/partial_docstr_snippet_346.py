class InfobloxHost(object):
    '''The Infoblox class is an interface for interfacing with the Infoblox
    appliance and contains pre-defined functionality for adding and removing
    hosts and the relevant records for those hosts.

    '''

    def __init__(self, host, username=None, password=None):
        '''Create a new instance of the Infoblox class

        :param str host: The Infoblox host to communicate with
        :param str username: The user to authenticate with
        :param str password: The password to authenticate with

        '''
        self.host = host
        self.username = username
        self.password = password
        self.base_url = f"https://{host}/wapi/v2.12"
        self.session = requests.Session()
        if username and password:
            self.session.auth = HTTPBasicAuth(username, password)
        self.session.verify = False

    def delete_old_host(self, hostname):
        '''Remove all records for the host.

        :param str hostname: Hostname to remove
        :rtype: bool

        '''
        try:
            # Search for host records
            search_url = f"{self.base_url}/record:host"
            params = {"name": hostname}
            response = self.session.get(search_url, params=params)
            
            if response.status_code == 200:
                records = response.json()
                for record in records:
                    ref = record.get('_ref')
                    if ref:
                        delete_url = f"{self.base_url}/{ref}"
                        delete_response = self.session.delete(delete_url)
                        if delete_response.status_code != 200:
                            return False
                return True
            return False
        except Exception:
            return False

    def add_new_host(self, hostname, ipv4addr, comment=None):
        '''Add or update a host in the infoblox, overwriting any IP address
        entries.

        :param str hostname: Hostname to add/set
        :param str ipv4addr: IP Address to add/set
        :param str comment: The comment for the record

        '''
        try:
            # First delete existing host
            self.delete_old_host(hostname)
            
            # Create new host record
            url = f"{self.base_url}/record:host"
            data = {
                "name": hostname,
                "ipv4addrs": [{"ipv4addr": ipv4addr}]
            }
            if comment:
                data["comment"] = comment
            
            response = self.session.post(url, json=data)
            return response.status_code == 201
        except Exception:
            return False