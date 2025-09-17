class SumAggregation(object):
    '''Sum Aggregation describes that data collected and aggregated with this
    method will be summed

    :type sum: int or float
    :param sum: the initial sum to be used in the aggregation

    '''

    def __init__(self, sum=None):
        self.sum = sum if sum is not None else 0

    def new_aggregation_data(self, measure):
        '''Get a new AggregationData for this aggregation.'''
        return SumAggregationData(self.sum)

    @staticmethod
    def get_metric_type(measure):
        '''Get the MetricDescriptorType for the metric produced by this
        aggregation and measure.
        '''
        if hasattr(measure, 'unit') and 'int' in str(type(measure.unit)).lower():
            return 'CUMULATIVE_INT64'
        return 'CUMULATIVE_DOUBLE'