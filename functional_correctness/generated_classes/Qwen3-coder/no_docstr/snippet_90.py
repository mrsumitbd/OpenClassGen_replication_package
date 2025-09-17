class Split(object):
    def read_split_file(self):
        pass

    def __init__(self, allele_file, extension='.fasta', number=True):
        self.allele_file = allele_file
        self.extension = extension
        self.number = number
        self.data = self.read_split_file()