class FIOAlerts(object):
    '''
    This class recieves an ForecastIO object and holds the alerts weather
    conditions. It has one class for this purpose.
    '''

    def __init__(self, forecast_io):
        '''
        Recieves an ForecastIO object and gets the alerts weather conditions
        if they are available in the object.
        '''
        self.alerts = None
        if hasattr(forecast_io, 'alerts'):
            self.alerts = forecast_io.alerts

    def get(self, alert=None):
        '''
        Returns a dictionary with alert weather conditions.
        Returns None is none are available.
        A day can be passed as an argument, is so function will call get_alert()
        to return that day.
        Look on function get_alert()
        '''
        if self.alerts is None:
            return None
            
        if alert is None:
            return self.alerts
        else:
            return self.get_alert(alert)

    def get_alert(self, alert):
        '''
        Recieves a day as an argument and returns the prediction for that alert
        if is available. If not, function will return None.
        '''
        if self.alerts is None:
            return None
            
        if isinstance(alert, int) and 0 <= alert < len(self.alerts):
            return self.alerts[alert]
        return None

    def alerts_count(self):
        '''
        Returns how many alerts of prediction are available.
        Returns None if none is available
        '''
        if self.alerts is None:
            return None
        return len(self.alerts)