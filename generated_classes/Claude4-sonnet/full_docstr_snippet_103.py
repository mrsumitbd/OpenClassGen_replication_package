class Coin(object):
    '''
    This is a model for a Coin object.
    '''

    def __init__(self, id = "", name = "", website = "", price_btc = "", volume_btc = ""):
        '''
        Simple constructor for a Coin.
        '''
        self.id = id
        self.name = name
        self.website = website
        self.price_btc = price_btc
        self.volume_btc = volume_btc

    def __repr__(self):
        '''
        The typ representation of a Coin.
        '''
        return f"Coin(id='{self.id}', name='{self.name}', website='{self.website}', price_btc='{self.price_btc}', volume_btc='{self.volume_btc}')"

    def __str__(self):
        '''
        The string representation of a Coin.
        '''
        return f"Coin: {self.name} ({self.id})"