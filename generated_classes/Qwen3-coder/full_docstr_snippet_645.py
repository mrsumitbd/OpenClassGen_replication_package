class GalpropMergedRingInfo(object):
    '''Information about a set of Merged Galprop Rings

    Parameters
    ----------

    source_name : str
        The name given to the merged component, e.g., merged_CO or merged_HI
    ring : int
        The index of the merged ring
    sourcekey : str
        Key that identifies this component, e.g., merged_CO_1, or merged_HI_3
    galkey : str
        Key that identifies how to merge the galprop rings, e.g., 'ref'
    galprop_run : str
        Key that idenfifies the galprop run used to make the input rings
    files : str
        List of files of the input gasmap files
    merged_gasmap : str
        Filename for the merged gasmap
    '''

    def __init__(self, **kwargs):
        '''C'tor: copies keyword arguments to data members
        '''
        self.source_name = kwargs.get('source_name')
        self.ring = kwargs.get('ring')
        self.sourcekey = kwargs.get('sourcekey')
        self.galkey = kwargs.get('galkey')
        self.galprop_run = kwargs.get('galprop_run')
        self.files = kwargs.get('files')
        self.merged_gasmap = kwargs.get('merged_gasmap')

    def update(self, **kwargs):
        '''Update data members from keyword arguments
        '''
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)