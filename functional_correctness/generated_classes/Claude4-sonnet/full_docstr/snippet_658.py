class NeedlePositionCache(object):
    '''Convert and cache needle positions.'''

    def __init__(self, get_needle_positions, machine):
        '''Create a new NeedlePositions object.'''
        self._get_needle_positions = get_needle_positions
        self._machine = machine
        self._cache = {}

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
        return self.get(line_number + 1) is None

    def get_bytes(self, line_number):
        '''Get the bytes representing needle positions or None.

        :param int line_number: the line number to take the bytes from
        :rtype: bytes
        :return: the bytes that represent the message or :obj:`None` if no
          data is there for the line.

        Depending on the :attr:`machine`, the length and result may vary.
        '''
        positions = self.get(line_number)
        if positions is None:
            return None
        return self._machine.needle_positions_to_bytes(positions)

    def get_line_configuration_message(self, line_number):
        '''Return the cnfLine content without id for the line.

        :param int line_number: the number of the line
        :rtype: bytes
        :return: a cnfLine message without id as defined in :ref:`cnfLine`
        '''
        positions = self.get(line_number)
        if positions is None:
            return b''
        return self._machine.get_line_configuration_message(positions)