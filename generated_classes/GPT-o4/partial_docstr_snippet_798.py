class SumAggregation(object):
    '''Sum Aggregation describes that data collected and aggregated with this
    method will be summed

    :type sum: int or float
    :param sum: the initial sum to be used in the aggregation
    '''

    def __init__(self, sum=None):
        self._initial_sum = sum if sum is not None else 0

    def new_aggregation_data(self, measure):
        '''Get a new AggregationData for this aggregation.'''
        return SumData(self._initial_sum)

    @staticmethod
    def get_metric_type(measure):
        '''Get the MetricDescriptorType for the metric produced by this
        aggregation and measure.
        '''
        if measure.value_type == MeasureType.DOUBLE:
            return MetricDescriptorType.CUMULATIVE_DOUBLE
        return MetricDescriptorType.CUMULATIVE_INT64