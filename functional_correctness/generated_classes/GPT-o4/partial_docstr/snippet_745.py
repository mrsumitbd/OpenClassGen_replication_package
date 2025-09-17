class FastqEntry:
    '''A simple class to store data from FASTQ entries and write them

    Attributes:
        id (str): FASTQ ID (everything between the '@' and the first space
            of header line)
        description (str): FASTQ description (everything after the first
            space of the header line)
        sequence (str): FASTQ sequence
        quality (str): FASTQ quality scores
    '''
    def __init__(self, header, sequence, quality):
        '''Initialize attributes to store FASTQ entry data'''
        header = header.rstrip()
        if header.startswith('@'):
            header = header[1:]
        parts = header.split(' ', 1)
        self.id = parts[0]
        self.description = parts[1] if len(parts) > 1 else ''
        self.sequence = sequence.rstrip()
        self.quality = quality.rstrip()

    def write(self):
        '''Return FASTQ formatted string

        Returns:
            str: FASTQ formatted string containing entire FASTQ entry
        '''
        hdr = '@' + self.id
        if self.description:
            hdr += ' ' + self.description
        return f"{hdr}\n{self.sequence}\n+\n{self.quality}\n"