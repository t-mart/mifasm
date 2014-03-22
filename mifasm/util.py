from bitstring import Bits

from . import MIFASM_WIDTH, radixes

class BitsT(object):
    """i suspect the bitstring.Bits class does some voodoo with __new__, making
    it difficult to subclass with a custom __init__ method."""
    def __init__(self, bits):
        self.bits = bits

    def __getattr__(self, name):
        if hasattr(self.bits, name):
            return getattr(self.bits, name)

    def radix(self, radix='hex'):
        if radix in radixes.keys():
            return getattr(self, radix)
        else:
            raise ValueError("radix {radix} is not supported".format(radix=radix))

    def __eq__(self, other):
        return self.bits == other.bits

class Address(BitsT):
    @classmethod
    def from_int(cls, i):
        b = Bits(uint=i, length=MIFASM_WIDTH)
        return cls(b)

