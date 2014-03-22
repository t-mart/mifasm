class Assembler(object):
    def __init__(self, input_f, output_f, addr_radix, data_radix, comments, **kwargs):
        self._input_f = input_f
        self._output_f = output_f
        self._addr_radix = addr_radix
        self._data_radix = data_radix
        self._comments = comments

