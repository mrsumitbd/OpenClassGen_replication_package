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
        self.base_url = f"https://{host}/wapi/v2.7/"
        self.session = requests.Session()
        self.session.verify = False
        if username and password:
            self.session.auth = HTTPBasicAuth(username, password)
        self.session.headers.update({"Content-Type": "application/json"})

    def delete_old_host(self, hostname):
        '''Remove all records for the host.

        :param str hostname: Hostname to remove
        :rtype: bool
        '''
        url = self.base_url + "record:host"
        params = {"name": hostname}
        r = self.session.get(url, params=params)
        if not r.ok:
            return False
        records = r.json()
        for rec in records:
            ref = rec.get("_ref")
            if not ref:
                continue
            del_url = self.base_url + ref
            dr = self.session.delete(del_url)
            if not dr.ok:
                return False
        return True

    def add_new_host(self, hostname, ipv4addr, comment=None):
        '''Add or update a host in the infoblox, overwriting any IP address
        entries.

        :param str hostname: Hostname to add/set
        :param str ipv4addr: IP Address to add/set
        :param str comment: The comment for the record
        '''
        # Remove existing records first
        if not self.delete_old_host(hostname):
            return False

        url = self.base_url + "record:host"
        payload = {
            "name": hostname,
            "ipv4addrs": [{"ipv4addr": ipv4addr}]
        }
        if comment:
            payload["comment"] = comment

        r = self.session.post(url, json=payload)
        return r.ok