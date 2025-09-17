class FastqEntry:
    '''A simple class to store data from FASTQ entries and write them

    Attributes:
            id (str): FASTQ ID (everything between the '@' and the first space
                of header line)

            description (str): FASTQ description (everything after the first
                space of the header line)

            sequence (str): FASTQ sequence

            quality (str): FASTQ quality csores
    '''

    def __init__(self):
        '''Initialize attributes to store FASTQ entry data'''
        self.id = ""
        self.description = ""
        self.sequence = ""
        self.quality = ""

    def write(self):
        '''Return FASTQ formatted string

        Returns:
            str: FASTQ formatted string containing entire FASTQ entry
        '''
        if self.description:
            header = f"@{self.id} {self.description}"
        else:
            header = f"@{self.id}"
        
        return f"{header}\n{self.sequence}\n+\n{self.quality}\n"