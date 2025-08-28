class MavenRepository:
    '''
    A Maven repository
    '''

    def __init__(self, rootPath):
        '''
        Initializes the repository.

        --rootPath: the path of the repository itself
        '''
        self.rootPath = rootPath

    def getRootPath(self):
        '''
        Returns the root path of the repository
        '''
        return self.rootPath

    def getArtifactPath(self, artifact, suffix=None, extension="jar"):
        '''
        Joins the root path of the repository with the relative path returned
        by the artifact's getPath() method
        '''
        artifact_path = artifact.getPath(suffix=suffix, extension=extension)
        return os.path.join(self.rootPath, artifact_path)

    def getLatestArtifactVersion(self, groupId, artifactId):
        '''
        Returns the latest version of the given artifact,
        given its groupId and its artifactId.

        Returns None if no version is available for that artifact.
        '''
        group_path = groupId.replace('.', os.sep)
        artifact_dir = os.path.join(self.rootPath, group_path, artifactId)
        
        if not os.path.exists(artifact_dir) or not os.path.isdir(artifact_dir):
            return None
        
        versions = []
        for item in os.listdir(artifact_dir):
            item_path = os.path.join(artifact_dir, item)
            if os.path.isdir(item_path):
                try:
                    versions.append(version.parse(item))
                except:
                    continue
        
        if not versions:
            return None
        
        return str(max(versions))