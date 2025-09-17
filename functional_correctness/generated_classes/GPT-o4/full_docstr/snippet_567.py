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

        self.github = GitHubTools()
        self.local = LocalTools()

    def get(self):
        '''Reads the remote file from Gist and save it locally'''
        gist = self.github.select_gist(
            user=self.user,
            filename=self.filename,
            allow_none=self.allow_none,
            assume_yes=self.assume_yes
        )
        content = self.github.download_file(gist_id=gist['id'], filename=self.filename)
        self.local.save_file(self.filename, content)

    def put(self):
        ''' Reads local file & update the remote gist (or create a new one)'''
        content = self.local.read_file(self.filename)
        gist = self.github.select_gist(
            user=self.user,
            filename=self.filename,
            allow_none=self.allow_none,
            assume_yes=self.assume_yes
        )
        files = {self.filename: content}
        if gist:
            self.github.update_gist(gist_id=gist['id'], files=files)
        else:
            public_flag = not self.create_private
            self.github.create_gist(files=files, public=public_flag)

    def ls(self):
        ''' Lists all gists from a github user '''
        return self.github.list_gists(user=self.user)