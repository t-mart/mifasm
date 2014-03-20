from .exceptions import *

class Assembler(object):

    # map nicer radix names to mif radix names
    # ours are also compatible with the bitstring package
    radixes = {'hex':'HEX', 'bin':'BIN', 'oct':'OCT', 'int':'DEC', 'uint':'UNS'}

    def __init__(self, input_f, output_f, addr_radix, data_radix, comments, **kwargs):
        self._input_f = input_f
        self._output_f = output_f
        self._addr_radix = addr_radix
        self._data_radix = data_radix
        self._width = 32
        self._depth = 2048
        self._comments = comments

