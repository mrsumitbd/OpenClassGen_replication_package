class NeedlePositionCache(object):
    '''Convert and cache needle positions.'''

    def __init__(self, get_needle_positions, machine):
        '''Create a new NeedlePositions object.'''
        self._get_callback = get_needle_positions
        self.machine = machine
        self._cache = {}
        self._bytes_cache = {}
        self._msg_cache = {}

    def get(self, line_number):
        '''Return the needle positions or None.

            :param int line_number: the number of the line
            :rtype: list
            :return: the needle positions for a specific line specified by
              :paramref:`line_number` or :obj:`None` if none were given
        '''
        if line_number in self._cache:
            return self._cache[line_number]
        pos = self._get_callback(line_number)
        if pos is not None:
            pos = list(pos)
        self._cache[line_number] = pos
        return pos

    def is_last(self, line_number):
        '''Whether the line number has no further lines.

            :rtype: bool
            :return: is the next line above the line number not specified
        '''
        # If the very next line has no positions, we consider this the last
        return self.get(line_number + 1) is None

    def get_bytes(self, line_number):
        '''Get the bytes representing needle positions or None.

            :param int line_number: the line number to take the bytes from
            :rtype: bytes
            :return: the bytes that represent the message or :obj:`None` if no
              data is there for the line.

            Depending on the :attr:`machine`, the length and result may vary.
        '''
        if line_number in self._bytes_cache:
            return self._bytes_cache[line_number]

        positions = self.get(line_number)
        if positions is None:
            self._bytes_cache[line_number] = None
            return None

        # Determine byte-array length
        if hasattr(self.machine, 'needle_byte_size'):
            size = self.machine.needle_byte_size
        elif hasattr(self.machine, 'needle_array_length'):
            size = self.machine.needle_array_length
        elif hasattr(self.machine, 'needle_count'):
            size = math.ceil(self.machine.needle_count / 8)
        else:
            max_needle = max(positions) if positions else -1
            size = math.ceil((max_needle + 1) / 8)

        ba = bytearray(size)
        for n in positions:
            if n < 0:
                continue
            idx = n // 8
            bit = n % 8
            if idx < size:
                ba[idx] |= (1 << bit)

        data = bytes(ba)
        self._bytes_cache[line_number] = data
        return data

    def get_line_configuration_message(self, line_number):
        '''Return the cnfLine content without id for the line.

            :param int line_number: the number of the line
            :rtype: bytes
            :return: a cnfLine message without id as defined in :ref:`cnfLine`
        '''
        if line_number in self._msg_cache:
            return self._msg_cache[line_number]

        bts = self.get_bytes(line_number)
        if bts is None:
            self._msg_cache[line_number] = None
            return None

        # pack line number as little-endian unsigned short, then data
        msg = struct.pack('<H', line_number) + bts
        self._msg_cache[line_number] = msg
        return msg