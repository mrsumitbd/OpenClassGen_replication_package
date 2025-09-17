class Assembly:
    def __init__(self, url):
        ''' Connect to an assembly that points to the assembly specified with the url.

            Args:
                - url (str): The url of the onshape item
        '''
        self.client = Client()
        self._did, self._wvm, self._wvm_id, self._eid = self._parse_url(url)

    def insert(self, part):
        ''' Insert a part into this assembly.

            Args:
                - part (onshapepy.part.Part) A Part instance that will be inserted.

            Returns:
                - requests.Response: Onshape response data
        '''
        did2, wvm2, wvm2_id, eid2 = self._parse_url(part.url)
        path = f"assemblies/d/{self._did}/{self._wvm}/{self._wvm_id}/e/{self._eid}/instances"
        body = {
            "sourceDocumentId": did2,
            "sourceWorkspaceId": wvm2 == "w" and wvm2_id or None,
            "sourceVersionId":    wvm2 == "v" and wvm2_id or None,
            "sourceElementId":    eid2,
            "sourceMicroversion": None,
            "transformation": {
                "translation": [0, 0, 0],
                "rotation":    [0, 0, 1, 0]
            }
        }
        return self.client.post(path, body)

    def _parse_url(self, url):
        m = re.search(r"/documents/([^/]+)/([wv])/([^/]+)/e/([^/?#]+)", url)
        if not m:
            raise ValueError(f"Invalid Onshape URL: {url}")
        return m.group(1), m.group(2), m.group(3), m.group(4)