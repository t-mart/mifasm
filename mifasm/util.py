from bitstring import Bits

class BitsT(object):
    """i suspect the bitstring.Bits class does some voodoo with __new__, making
    it difficult to subclass with a custom __init__ method."""

    def __getattr__(self, name):
        return getattr(self.bits, name)

    def radix(self, radix='hex'):
        if radix in ['hex', 'bin', 'oct', 'int', 'uint']:
            return getattr(self, radix)
        else:
            raise ValueError("radix {radix} is not supported".format(radix=radix))

