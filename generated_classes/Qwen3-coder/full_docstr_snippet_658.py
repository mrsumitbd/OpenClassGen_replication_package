class NeedlePositionCache(object):
    '''Convert and cache needle positions.'''

    def __init__(self, get_needle_positions, machine):
        '''Create a new NeedlePositions object.'''
        self._get_needle_positions = get_needle_positions
        self.machine = machine
        self._cache = {}
        self._bytes_cache = {}

    def get(self, line_number):
        '''Return the needle positions or None.

        :param int line_number: the number of the line
        :rtype: list
        :return: the needle positions for a specific line specified by
          :paramref:`line_number` or :obj:`None` if no were given
        '''
        if line_number not in self._cache:
            self._cache[line_number] = self._get_needle_positions(line_number)
        return self._cache[line_number]

    def is_last(self, line_number):
        '''Whether the line number is has no further lines.

        :rtype: bool
        :return: is the next line above the line number are not specified
        '''
        current = self.get(line_number)
        next_line = self.get(line_number + 1)
        return current is not None and next_line is None

    def get_bytes(self, line_number):
        '''Get the bytes representing needle positions or None.

        :param int line_number: the line number to take the bytes from
        :rtype: bytes
        :return: the bytes that represent the message or :obj:`None` if no
          data is there for the line.

        Depending on the :attr:`machine`, the length and result may vary.
        '''
        if line_number not in self._bytes_cache:
            positions = self.get(line_number)
            if positions is None:
                self._bytes_cache[line_number] = None
            else:
                # Convert needle positions to bytes based on machine type
                if hasattr(self.machine, 'get_bytes_for_needle_positions'):
                    self._bytes_cache[line_number] = self.machine.get_bytes_for_needle_positions(positions)
                else:
                    # Default implementation - convert to bytes
                    self._bytes_cache[line_number] = bytes(positions)
        return self._bytes_cache[line_number]

    def get_line_configuration_message(self, line_number):
        '''Return the cnfLine content without id for the line.

        :param int line_number: the number of the line
        :rtype: bytes
        :return: a cnfLine message without id as defined in :ref:`cnfLine`
        '''
        needle_bytes = self.get_bytes(line_number)
        if needle_bytes is None:
            return None
        
        # Create cnfLine message without id
        # This is a basic implementation - in practice this would follow specific protocol
        if hasattr(self.machine, 'create_cnf_line_message'):
            return self.machine.create_cnf_line_message(needle_bytes)
        else:
            # Default implementation
            return needle_bytes