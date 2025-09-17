class GetGist(object):
    '''
    Main GetGist objects linking inputs from the CLI to the helpers from
    GitHubTools (to deal with the API) and LocalTools (to deal with the local
    file system.
    '''

    def __init__(self, **kwargs):
        '''
        Instantiate GitHubTools & LocalTools (if needed), and set the variables required
        to get, create or update gists (filename and public/private flag)
        :param user: (str) GitHub username
        :param filename: (str) name of file from any Gist or local file system
        :param allow_none: (bool) flag to use GitHubTools.select_gist
        differently with `getgist` and `putgist` commands (if no gist/filename
        is found it raises an error for `getgist`, or sets `putgist` to create
        a new gist).
        :param create_private: (bool) create a new gist as private
        :param assume_yes: (bool) assume yes (or first option) for all prompts
        :return: (None)
        '''
        self.user = kwargs.get('user')
        self.filename = kwargs.get('filename')
        self.allow_none = kwargs.get('allow_none', False)
        self.create_private = kwargs.get('create_private', False)
        self.assume_yes = kwargs.get('assume_yes', False)
        
        # Instantiate GitHubTools and LocalTools
        from getgist.github import GitHubTools
        from getgist.local import LocalTools
        
        self.github = GitHubTools(self.user, self.filename)
        self.local = LocalTools(self.filename)

    def get(self):
        '''Reads the remote file from Gist and save it locally'''
        # Select the appropriate gist
        gist = self.github.select_gist(allow_none=self.allow_none)
        if not gist:
            return False
            
        # Get the content from the selected gist
        content = self.github.get_gist_content(gist)
        if content is None:
            return False
            
        # Save the content locally
        return self.local.save_content(content)

    def put(self):
        ''' Reads local file & update the remote gist (or create a new one)'''
        # Read local content
        content = self.local.read_content()
        if content is None:
            return False
            
        # Select or create gist
        gist = self.github.select_gist(allow_none=self.allow_none)
        
        if gist:
            # Update existing gist
            return self.github.update_gist(gist, content)
        else:
            # Create new gist
            is_public = not self.create_private
            return self.github.create_gist(content, is_public)

    def ls(self):
        ''' Lists all gists from a github user '''
        gists = self.github.list_gists()
        if gists:
            for gist in gists:
                print(gist)
            return True
        return False