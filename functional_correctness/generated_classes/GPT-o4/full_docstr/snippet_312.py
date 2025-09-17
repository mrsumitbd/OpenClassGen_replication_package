class Fixerio(object):
    ''' A client for Fixer.io. '''
    BASE_URL = 'http://data.fixer.io/api'

    def __init__(self, access_key, symbols=None):
        '''
        :param access_key: your API Key.
        :type access_key: str or unicode
        :param symbols: currency symbols to request specific exchange rates.
        :type symbols: list or tuple
        '''
        self.access_key = access_key
        if symbols is not None and not isinstance(symbols, (list, tuple)):
            raise ValueError("symbols must be a list or tuple")
        self.symbols = symbols

    def _create_payload(self, symbols):
        ''' Creates a payload with no none values.

        :param symbols: currency symbols to request specific exchange rates.
        :type symbols: list or tuple
        :return: a payload.
        :rtype: dict
        '''
        payload = {'access_key': self.access_key}
        syms = symbols if symbols is not None else self.symbols
        if syms is not None:
            if not isinstance(syms, (list, tuple)):
                raise ValueError("symbols must be a list or tuple")
            payload['symbols'] = ','.join(syms)
        return payload

    def latest(self, symbols=None):
        ''' Get the latest foreign exchange reference rates.

        :param symbols: currency symbols to request specific exchange rates.
        :type symbols: list or tuple
        :return: the latest foreign exchange reference rates.
        :rtype: dict
        :raises FixerioException: if any error making a request.
        '''
        url = f"{self.BASE_URL}/latest"
        payload = self._create_payload(symbols)
        resp = requests.get(url, params=payload)
        try:
            data = resp.json()
        except ValueError:
            raise FixerioException("Invalid JSON response")
        if not data.get('success', False):
            err = data.get('error', {})
            msg = err.get('info', 'Unknown error')
            raise FixerioException(msg)
        return data

    def historical_rates(self, date, symbols=None):
        '''
        Get historical rates for any day since `date`.

        :param date: a date
        :type date: date or str
        :param symbols: currency symbols to request specific exchange rates.
        :type symbols: list or tuple
        :return: the historical rates for any day since `date`.
        :rtype: dict
        :raises FixerioException: if any error making a request.
        '''
        if isinstance(date, datetime.date):
            date_str = date.isoformat()
        elif isinstance(date, str):
            date_str = date
        else:
            raise ValueError("date must be a datetime.date or str")
        url = f"{self.BASE_URL}/{date_str}"
        payload = self._create_payload(symbols)
        resp = requests.get(url, params=payload)
        try:
            data = resp.json()
        except ValueError:
            raise FixerioException("Invalid JSON response")
        if not data.get('success', False):
            err = data.get('error', {})
            msg = err.get('info', 'Unknown error')
            raise FixerioException(msg)
        return data