from .packages.bitstring import BitArray
from .run import run

MIFASM_WIDTH = 32
MIFASM_DEPTH = 2048

# map nicer radix names to mif radix names
# ours are also compatible with the bitstring package
radixes = {'hex':'HEX', 'bin':'BIN', 'int':'DEC', 'uint':'UNS'}
# im choosing not to support 'oct':'OCT'.
#   - unambiguous oct representation requires width to be a multiple of 3. 32
#     is not.
#   - who uses oct anyway?

class MBitArray(BitArray):
    @classmethod
    def from_int(cls, i):
        return cls(int=i, length=MIFASM_WIDTH)

    @classmethod
    def from_mbitarray_list(cls, mba_list):
        new = cls()
        for mba in mba_list:
            new.append(mba)
        return new

    def __add__(self, rhs):
        if isinstance(rhs, type(MBitArray)):
            length = self.length if self.length > rhs.length else rhs.length
            return MBitArray.from_int(self.int + rhs.int)
        elif isinstance(rhs, type(int)):
            return MBitArray.from_int(self.int + rhs)
        else:
            raise NotImplemented

    def __mult__(self, rhs):
        if isinstance(rhs, type(MBitArray)):
            length = self.length if self.length > rhs.length else rhs.length
            return MBitArray.from_int(self.int * rhs.int)
        elif isinstance(rhs, type(int)):
            return MBitArray.from_int(self.int * rhs)
        else:
            raise NotImplemented

    def __eq__(self, rhs):
        if isinstance(rhs, type(MBitArray)):
            return self.int == other.int
        elif isinstance(rhs, type(int)):
            return self.int == rhs

    def radix(self, radix='hex'):
        if radix in radixes.keys():
            return getattr(self, radix)
        else:
            raise NotImplemented("mifasm doesn't support that radix")
