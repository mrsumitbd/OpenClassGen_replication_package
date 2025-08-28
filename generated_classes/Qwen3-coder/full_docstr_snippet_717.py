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
        relative_path = artifact.getPath(suffix=suffix, extension=extension)
        return os.path.join(self.rootPath, relative_path)

    def getLatestArtifactVersion(self, groupId, artifactId):
        '''
        Returns the latest version of the given artifact,
        given its groupId and its artifactId.

        Returns None if no version is available for that artifact.
        '''
        # Convert groupId to directory structure
        group_path = groupId.replace('.', '/')
        artifact_dir = os.path.join(self.rootPath, group_path, artifactId)
        
        # Check if artifact directory exists
        if not os.path.exists(artifact_dir):
            return None
            
        # Get all version directories
        try:
            versions = [v for v in os.listdir(artifact_dir) 
                       if os.path.isdir(os.path.join(artifact_dir, v))]
        except OSError:
            return None
            
        if not versions:
            return None
            
        # Return the "latest" version (lexicographically largest for simplicity)
        # In a real implementation, you might want to implement proper version comparison
        return sorted(versions)[-1]