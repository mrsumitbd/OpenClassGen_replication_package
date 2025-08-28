class Fixerio(object):
    ''' A client for Fixer.io. '''

    def __init__(self, access_key, symbols=None):
        '''
        :param access_key: your API Key.
        :type access_key: str or unicode
        :param symbols: currency symbols to request specific exchange rates.
        :type symbols: list or tuple
        '''
        self.access_key = access_key
        self.symbols = symbols
        self.base_url = 'http://data.fixer.io/api'

    def _create_payload(self, symbols):
        ''' Creates a payload with no none values.

        :param symbols: currency symbols to request specific exchange rates.
        :type symbols: list or tuple
        :return: a payload.
        :rtype: dict
        '''
        payload = {'access_key': self.access_key}
        if symbols:
            payload['symbols'] = ','.join(symbols)
        elif self.symbols:
            payload['symbols'] = ','.join(self.symbols)
        return payload

    def latest(self, symbols=None):
        ''' Get the latest foreign exchange reference rates.

        :param symbols: currency symbols to request specific exchange rates.
        :type symbols: list or tuple
        :return: the latest foreign exchange reference rates.
        :rtype: dict
        :raises FixerioException: if any error making a request.
        '''
        url = f'{self.base_url}/latest'
        payload = self._create_payload(symbols)
        
        try:
            response = requests.get(url, params=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise FixerioException(f"Error making request: {e}")
        except ValueError as e:
            raise FixerioException(f"Error parsing JSON response: {e}")

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
        if isinstance(date, date):
            date_str = date.strftime('%Y-%m-%d')
        else:
            date_str = str(date)
            
        url = f'{self.base_url}/{date_str}'
        payload = self._create_payload(symbols)
        
        try:
            response = requests.get(url, params=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise FixerioException(f"Error making request: {e}")
        except ValueError as e:
            raise FixerioException(f"Error parsing JSON response: {e}")