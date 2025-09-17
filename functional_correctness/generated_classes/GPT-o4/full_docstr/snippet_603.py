class FIOAlerts(object):
    '''
    This class receives a ForecastIO object and holds the alerts weather
    conditions. It has one class for this purpose.
    '''

    def __init__(self, forecast_io):
        '''
        Receives a ForecastIO object and gets the alerts weather conditions
        if they are available in the object.
        '''
        self._alerts = None
        data = None
        # Try to get JSON dict from forecast_io
        if hasattr(forecast_io, 'json'):
            try:
                j = forecast_io.json
                data = j() if callable(j) else j
            except Exception:
                data = None
        if data is None and hasattr(forecast_io, '_json'):
            data = forecast_io._json
        if isinstance(data, dict):
            self._alerts = data.get('alerts')
        else:
            self._alerts = None

    def get(self, alert=None):
        '''
        Returns a dictionary with alert weather conditions.
        Returns None if none are available.
        A day can be passed as an argument; in so doing the function will call get_alert()
        to return that day.
        '''
        if self._alerts is None:
            return None
        if alert is None:
            return self._alerts
        return self.get_alert(alert)

    def get_alert(self, alert):
        '''
        Receives a day (index or title) as an argument and returns the prediction for that alert
        if it is available. If not, function will return None.
        '''
        if not self._alerts:
            return None
        # If alert is integer index
        if isinstance(alert, int):
            if 0 <= alert < len(self._alerts):
                return self._alerts[alert]
            return None
        # Otherwise, try match by title
        for a in self._alerts:
            if isinstance(a, dict) and a.get('title') == alert:
                return a
        return None

    def alerts_count(self):
        '''
        Returns how many alerts of prediction are available.
        Returns None if none is available.
        '''
        if self._alerts is None:
            return None
        return len(self._alerts)