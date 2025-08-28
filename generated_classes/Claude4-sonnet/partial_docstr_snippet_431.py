class Table(object):
    '''
        Allows the following:

        
        incident = Table(incident)
        criterion = incident.company.eq('3dasd3')
        
    '''

    def __init__(self, name):
        self.name = name

    def field(self, name):
        return Field(self.name, name)

    def __getattr__(self, name):
        return Field(self.name, name)

    def __getitem__(self, name):
        return Field(self.name, name)