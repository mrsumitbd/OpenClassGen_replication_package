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
        self.__dimension = dimension
        self.__intervals = intervals
        self.__coordinate = [0] * dimension

    def get_coordinate(self):
        '''!
        @brief Returns current block coordinate.

        '''
        return self.__coordinate[:]

    def increment(self):
        '''!
        @brief Forms logical location for next block.

        '''
        index = self.__dimension - 1
        
        while index >= 0:
            self.__coordinate[index] += 1
            if self.__coordinate[index] < self.__intervals:
                return True
            else:
                self.__coordinate[index] = 0
                index -= 1
        
        return False