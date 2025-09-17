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
        self._currently = None
        try:
            data = getattr(forecast_io, 'json', None)
            if isinstance(data, dict):
                self._currently = data.get('currently')
        except Exception:
            self._currently = None

    def get(self):
        '''
        Returns a dictionary with current weather conditions.
        Returns None is none are available.

        Returns:
            Dictionary with current weather conditions.
            None is none are available.
        '''
        return self._currently