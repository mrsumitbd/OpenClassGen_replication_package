class FIOCurrently(object):
    '''
    This class recieves an ForecastIO object and holds the currently weather
    conditions.
    '''

    def __init__(self, forecast_io):
        '''
        Construct a new 'FIOCurrently' object.
        Recieves an ForecastIO object and gets the currently weather conditions
        if they are available in the object.

        Args:
            forecast_io (ForecastIO): The ForecastIO object
        '''
        self.forecast_io = forecast_io
        self.currently = None
        if hasattr(forecast_io, 'json') and forecast_io.json:
            self.currently = forecast_io.json.get('currently')

    def get(self):
        '''
        Returns a dictionary with current weather conditions.
        Returns None is none are available.

        Returns:
            Dictionary with current weather conditions.
            None is none are available.
        '''
        return self.currently