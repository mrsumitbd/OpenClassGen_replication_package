class MavenRepository:
    '''
    A Maven repository
    '''

    def __init__(self, rootPath):
        '''
        Initializes the repository.

        --rootPath: the path of the repository itself
        '''
        self._rootPath = rootPath

    def getRootPath(self):
        '''
        Returns the root path of the repository
        '''
        return self._rootPath

    def getArtifactPath(self, artifact, suffix=None, extension="jar"):
        '''
        Joins the root path of the repository with the relative path returned
        by the artifact's getPath() method
        '''
        base_path = os.path.join(self._rootPath, artifact.getPath())
        if suffix:
            base_path = f"{base_path}-{suffix}"
        return f"{base_path}.{extension}"

    def getLatestArtifactVersion(self, groupId, artifactId):
        '''
        Returns the latest version of the given artifact,
        given its groupId and its artifactId.

        Returns None if no version is available for that artifact.
        '''
        group_path = os.path.join(self._rootPath, *groupId.split('.'))
        artifact_path = os.path.join(group_path, artifactId)
        if not os.path.isdir(artifact_path):
            return None
        versions = [
            name for name in os.listdir(artifact_path)
            if os.path.isdir(os.path.join(artifact_path, name))
        ]
        if not versions:
            return None

        def version_key(ver):
            parts = ver.split('.')
            nums = []
            for part in parts:
                m = re.match(r'(\d+)', part)
                nums.append(int(m.group(1)) if m else 0)
            return tuple(nums)

        return max(versions, key=version_key)