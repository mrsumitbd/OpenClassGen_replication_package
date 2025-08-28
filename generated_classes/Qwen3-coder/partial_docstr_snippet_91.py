class SearchEngineResult:
    '''Result of general search engine'''

    def __init__(self, title, link, description=""):
        '''
        :param title: title of result
        :param link: search query url
        :param description: description of result
        '''
        self.title = title
        self.link = link
        self.description = description

    def __str__(self):
        return f"{self.title}\n{self.link}\n{self.description}"