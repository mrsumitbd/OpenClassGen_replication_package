class Parser:
    '''Mother of all data-files parsers'''

    def __init__(self, file_path):
        '''
        :param file_path: path to file
        '''
        self.file_path = file_path

    def get_lines(self):
        '''Gets lines in file

        :return: Lines in file
        '''
        with open(self.file_path, 'r') as file:
            return file.readlines()