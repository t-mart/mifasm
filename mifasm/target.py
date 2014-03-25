from collections import namedtuple
from warnings import warn

from . import MIFASM_WIDTH, MIFASM_DEPTH, radixes, MBitArray
from .exceptions import FullTargetException, OverwriteWarning
from .memloc import MemLoc

DEADMEMLOC = MemLoc(MBitArray(hex='0000dead'))

class Target(object):
    def __init__(self, addr_radix, data_radix, depth=MIFASM_DEPTH, width=MIFASM_WIDTH):
        self.depth = depth
        self.width = width
        self._addr_radix = addr_radix
        self._data_radix = data_radix
        self._cursor = MBitArray.from_int(0)
        self._memlocs = []

    def _current_depth(self):
        return sum([memloc.length for memloc in self._memlocs])

    def _fill_to(self, length, value=DEADMEMLOC):
        """fill the target with value until target depth = length"""
        if self._cursor.uint < length.uint:
            while self._current_depth() != length.uint:
                self._memlocs.append(value)

    def _fill_to_depth(self, value=DEADMEMLOC):
        self._fill_to(length=MBitArray.from_int(self.depth), value=value)

    def set_cursor(self, where):
        if where.uint > self.depth:
            raise IndexError("Can't set cursor beyond prescribed depth")
        if where.uint < 0:
            raise IndexError("Can't set cursor to less than 0")

        if where.uint > self._current_depth():
            self._fill_to(length=where)
        self._cursor = where

    def cursor_memloc(self):
        return self._memlocs[self._cursor.uint]

    def place(self, memloc):
        """place memloc at cursor and increment cursor"""
        if self._cursor.uint == self.depth:
            raise FullTargetException()
        if self._cursor.uint < self._current_depth():
            if self.cursor_memloc() != DEADMEMLOC:
                warn("Attempting to write to a memloc that's already been placed", OverwriteWarning)
            self._memlocs[self._cursor.uint] = memloc

        self._memlocs.append(memloc)
        self.set_cursor(MBitArray.from_int(self._cursor.uint + 1))

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

        return new_memlocs

    def out(self, compress=True):
        target_items = []
        self._fill_to_depth()

        target_items.append(self.preamble())

        if compress:
            memlocs = self._compress()
        else:
            memlocs = self._memlocs

        next_address = MBitArray.from_int(0)
        for i, memloc in enumerate(memlocs):
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
