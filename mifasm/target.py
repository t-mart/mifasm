from bitstring import Bits

class Word(Bits):
    def __init__(self, address):
        pass


class MemLoc(object):
    def __init__(self, data):
        self.data = data
        self.length = 1

    def out(self, address, addr_radix='hex', data_radix='hex'):
        address = getattr(address, addr_radix)
        data = getattr(self.data, data_radix)

        s = "{address} : {data}".format(address=address, data=data)
        return s

class InstructionMemLoc(MemLoc):
    def out(self, address, addr_radix='hex', data_radix='hex'):

        s = "-- {comment}\n".format(comment='foo') + \
                super(InstructionMemLoc, self).out(addr_radix, data_radix)
        return s


class MemLocSpan(object):
    """object representing a contiguous span of memory locations with the same
    value.

    this compresses target output by replacing several memory location
    declarations with a single one. mif files support this with the
    [START..END] : DATA syntax
    """
    def __init__(self, data, length):
        self.data = data
        self.length = length

    def out(self, start_addr, addr_radix='hex', data_radix='hex'):
        end_addr = getattr(Bits("uint:{width}={val}".format(width=start_addr.length, val=start_addr.uint+self.length)), addr_radix)
        start_addr = getattr(start_addr, addr_radix)

        data = getattr(self.data, data_radix)

        s = "[{start_addr}..{end_addr}] : {data}".format(start_addr=start_addr, end_addr=end_addr, data=self.data)
        return s


class Target(list):
    def __init__(self, depth, width, addr_radix, data_radix):
        self._depth = depth
        self._width = width
        self._addr_radix = addr_radix
        self._data_radix = data_radix

    def byte_addr(addr, offset=0):
        return addr * self._width + offset

    def compress(self):
        """compress the target if possible"""
        # a list of (start, end, data) tuples that represent the beginning and
        # end of of a span of memlocs that have the same value
        runs = []

        start_addr = None
        start_memloc = None
        for addr, memloc in enumerate(self):
            addr = Bits(uint=addr, length=self._width)
            # skip the first check because start_memloc is None
            if start_memloc:
                if memloc.data != start_memloc.data:
                    runs.append((start_addr, addr, start_memloc.data))
                    start_addr = addr
                    start_memloc = memloc
            else:
                start_addr = addr
                start_memloc = memloc

        # we may have finished in a run
        if start_addr != addr:
            runs.append((start_addr, addr, start_memloc.data))

        for start, end, data in runs:
            del self[start.int:end.int+1]
            new_span = MemLocSpan(data, end.int-start.int)
            self.insert(start.int, new_span)

    def __len__(self):
        return sum([memloc.length for memloc in self])

    def fill_space(self):
        empty_space = self._depth - len(self)
        self.extend([MemLoc(Bits('uint:32=0'))] * empty_space)

    def out(self):
        return [memloc.out(Bits("uint:{width}={addr}".format(width=self._width, addr=addr)), self._addr_radix, self._data_radix) for addr, memloc in enumerate(self)]
