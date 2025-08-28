class Coin(object):
    '''
    This is a model for a Coin object.
    '''

    def __init__(self, id="", name="", website="", price_btc="", volume_btc=""):
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
        return (
            "Coin(id={!r}, name={!r}, website={!r}, "
            "price_btc={!r}, volume_btc={!r})"
        ).format(
            self.id,
            self.name,
            self.website,
            self.price_btc,
            self.volume_btc
        )

    def __str__(self):
        '''
        The string representation of a Coin.
        '''
        return (
            f"{self.name} ({self.id})\n"
            f"Website: {self.website}\n"
            f"Price (BTC): {self.price_btc}\n"
            f"Volume (BTC): {self.volume_btc}"
        )