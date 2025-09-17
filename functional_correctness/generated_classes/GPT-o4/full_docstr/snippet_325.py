class coordinate_iterator:
    '''!
    @brief Coordinate iterator is used to generate logical location description for each CLIQUE block.
    @details This class is used by CLIQUE algorithm for clustering process.
    '''

    def __init__(self, dimension, intervals):
        '''!
        @brief Initializes coordinate iterator for CLIQUE algorithm.

        @param[in] dimension (uint): Amount of dimensions in input data space.
        @param[in] intervals (uint): Amount of intervals in each dimension.
        '''
        self.dimension = dimension
        self.intervals = intervals
        self._coord = [0] * dimension
        self._done = False

    def get_coordinate(self):
        '''!
        @brief Returns current block coordinate.
        '''
        return tuple(self._coord)

    def increment(self):
        '''!
        @brief Forms logical location for next block.
        '''
        if self._done:
            return False
        # if already at last coordinate, mark done
        if all(x == self.intervals - 1 for x in self._coord):
            self._done = True
            return False
        # otherwise carry increment
        for i in reversed(range(self.dimension)):
            if self._coord[i] < self.intervals - 1:
                self._coord[i] += 1
                return True
            self._coord[i] = 0
        return True