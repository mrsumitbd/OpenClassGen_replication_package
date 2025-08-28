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
        self.current_coordinate = [0] * dimension

    def get_coordinate(self):
        '''!
        @brief Returns current block coordinate.

        '''
        return self.current_coordinate.copy()

    def increment(self):
        '''!
        @brief Forms logical location for next block.

        '''
        for i in range(self.dimension - 1, -1, -1):
            self.current_coordinate[i] += 1
            if self.current_coordinate[i] < self.intervals:
                break
            else:
                self.current_coordinate[i] = 0