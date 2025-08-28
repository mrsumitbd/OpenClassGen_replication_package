class ACCESS_MASK(object):
    def __init__(self, mask):
        if not isinstance(mask, int):
            raise TypeError("mask must be an integer")
        self._mask = mask

    def has_priv(self, priv):
        if not isinstance(priv, int):
            raise TypeError("priv must be an integer")
        return bool(self._mask & priv)

    def set_priv(self, priv):
        if not isinstance(priv, int):
            raise TypeError("priv must be an integer")
        self._mask |= priv

    def remove_priv(self, priv):
        if not isinstance(priv, int):
            raise TypeError("priv must be an integer")
        self._mask &= ~priv

    def __repr__(self):
        return f"{self.__class__.__name__}(0x{self._mask:08X})"