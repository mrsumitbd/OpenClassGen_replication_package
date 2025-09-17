class Assembly:
    def __init__(self, url):
        ''' Connect to an assembly that points to the assembly specified with the url.

        Args:
            - url (str): The url of the onshape item
        '''
        self.url = url
        self._parse_url()
        
    def _parse_url(self):
        parsed = urlparse(self.url)
        path_parts = parsed.path.strip('/').split('/')
        
        if 'documents' in path_parts:
            doc_index = path_parts.index('documents')
            self.document_id = path_parts[doc_index + 1]
            
        if 'w' in path_parts:
            w_index = path_parts.index('w')
            self.workspace_id = path_parts[w_index + 1]
        elif 'v' in path_parts:
            v_index = path_parts.index('v')
            self.version_id = path_parts[v_index + 1]
            self.workspace_id = None
        elif 'm' in path_parts:
            m_index = path_parts.index('m')
            self.microversion_id = path_parts[m_index + 1]
            self.workspace_id = None
            
        if 'e' in path_parts:
            e_index = path_parts.index('e')
            self.element_id = path_parts[e_index + 1]

    def insert(self, part):
        ''' Insert a part into this assembly.

        Args:
            - part (onshapepy.part.Part) A Part instance that will be inserted.

        Returns:
            - requests.Response: Onshape response data

        '''
        base_url = "https://cad.onshape.com/api/assemblies/d"
        
        if hasattr(self, 'workspace_id') and self.workspace_id:
            url = f"{base_url}/{self.document_id}/w/{self.workspace_id}/e/{self.element_id}/instances"
        elif hasattr(self, 'version_id'):
            url = f"{base_url}/{self.document_id}/v/{self.version_id}/e/{self.element_id}/instances"
        elif hasattr(self, 'microversion_id'):
            url = f"{base_url}/{self.document_id}/m/{self.microversion_id}/e/{self.element_id}/instances"
        
        payload = {
            "documentId": part.document_id,
            "elementId": part.element_id,
            "partId": part.part_id,
            "isAssembly": False,
            "isWholePartStudio": False
        }
        
        if hasattr(part, 'workspace_id') and part.workspace_id:
            payload["versionId"] = part.workspace_id
        elif hasattr(part, 'version_id'):
            payload["versionId"] = part.version_id
        elif hasattr(part, 'microversion_id'):
            payload["microversionId"] = part.microversion_id
            
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, json=payload, headers=headers)
        return response