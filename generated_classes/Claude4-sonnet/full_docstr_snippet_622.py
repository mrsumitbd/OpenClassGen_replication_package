class JournalReader(object):
    '''Handle reading and interpretting a journal file from Autodesk Revit.'''

    def __init__(self, journal_file):
        '''Initialize the reader object with path to the target journal file.

        Args:
            journal_file (str): full path to target journal file
        '''
        self.journal_file = journal_file

    def _read_journal(self):
        '''Private method that reads the journal file contents.

        Returns:
            str: journal file contents
        '''
        with open(self.journal_file, 'r', encoding='utf-8') as f:
            return f.read()

    def endswith(self, search_str):
        '''Check whether the provided string exists in Journal file.

        Only checks the last 5 lines of the journal file. This method is
        usually used when tracking a journal from an active Revit session.

        Args:
            search_str (str): string to search for

        Returns:
            bool: if True the search string is found
        '''
        content = self._read_journal()
        lines = content.splitlines()
        last_5_lines = lines[-5:] if len(lines) >= 5 else lines
        
        for line in last_5_lines:
            if search_str in line:
                return True
        return False

    def is_stopped(self):
        '''Check whether the journal execution has stopped.

        Returns:
            bool: True if the journal execution has stopped
        '''
        return self.endswith('Jrn.Command "SystemMenu" , "Quit the application; prompts to save projects , ID_APP_EXIT"')