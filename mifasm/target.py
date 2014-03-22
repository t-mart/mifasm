from collections import namedtuple

from bitstring import Bits

from . import MIFASM_WIDTH, MIFASM_DEPTH, radixes
from .util import BitsT, Address
from .exceptions import FullTargetException
from .memloc import MemLoc

DEADMEMLOC = MemLoc(BitsT(Bits(hex='0000dead')))

class Target(object):
    def __init__(self, addr_radix, data_radix, depth=MIFASM_DEPTH, width=MIFASM_WIDTH):
        self.depth = depth
        self.width = width
        self._addr_radix = addr_radix
        self._data_radix = data_radix
        self._memlocs = []

    def _current_depth(self):
        return sum([memloc.length for memloc in self._memlocs])

    def _fill_to_depth(self, value=DEADMEMLOC):
        empty_space = self.depth - self._current_depth()
        self._memlocs.extend([value] * empty_space)

    def append(self, memloc):
        if self._current_depth() == self.depth:
            raise FullTargetException()
        self._memlocs.append(memloc)

    def _compress(self):
        """compress the target if possible, with run length encoding"""
        new_memlocs = []

        for memloc in self._memlocs:
            if len(new_memlocs) == 0:
                new_memlocs.append(memloc)
            else:
                if memloc == new_memlocs[-1]:
                    new_memlocs[-1].length += 1
                else:
                    new_memlocs.append(memloc)

        self._memlocs = new_memlocs

    def out(self, compress=True):
        target_items = []
        self._fill_to_depth()

        target_items.append(self.preamble())

        if compress:
            self._compress()

        next_address = Address.from_int(0)
        for i, memloc in enumerate(self._memlocs):
            target_items.append(memloc.out(next_address, self._addr_radix, self._data_radix))
            next_address = memloc.next_address(next_address)

        target_items.append(Target.end_string())
        return "\n".join(target_items)

    def preamble(self):
        mif_addr_radix = radixes[self._addr_radix]
        mif_data_radix = radixes[self._data_radix]
        s = (
                "WIDTH={width};\n"
                "DEPTH={depth};\n"
                "ADDRESS_RADIX={mif_addr_radix};\n"
                "DATA_RADIX={mif_addr_radix};\n"
                "CONTENT BEGIN"
                ).format(width=self.width, depth=self.depth,
                        mif_addr_radix=mif_addr_radix,
                        mif_data_radix=mif_data_radix)
        return s

    @staticmethod
    def end_string():
        return "END;"
