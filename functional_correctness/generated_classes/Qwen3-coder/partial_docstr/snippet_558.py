class Author(object):
    '''The blog's owner, only one
    attributes
      name      unicode     author's name
      email     unicode     author's email
    '''

    def __init__(self, name="", email=""):
        self.name = name
        self.email = email

    @property
    def gravatar_id(self):
        '''it's md5(author.email), author's gravatar_id'''
        return hashlib.md5(self.email.encode('utf-8')).hexdigest()