from .exceptions import *

class Assembler(object):

    radix_names = ['bin', 'oct', 'hex', 'dec', 'udec']

    @staticmethod
    def _radix_function(radix_name, width):
        """creates a single-argument function that converts an integer
        to a string representation of that integer in a particular base"""
        # there's some crazy magic that happens in here
        width_mask = int(''.join(['1' for i in range(width)]),2)
        if radix_name == 'hex':
            l = lambda i: ("{0:0>%dx}" % (width//4)).format(i & width_mask)
        elif radix_name == 'oct':
            l = lambda i: ("{0:0>%do}" % (width//3)).format(i & width_mask)
        elif radix_name == 'bin':
            l = lambda i: ("{0:0>%db}" % (width)).format(i & width_mask)
        elif radix_name == 'udec':
            l = lambda i: "{0:0>d}".format(i & width_mask)
        elif radix_name == 'dec':
            l = lambda i: "{0:0>d}".format(i)
        else:
            raise ValueError("Unknown radix name %s" % radix_name)

        def func(i):
            upper_bound = 2**(width)
            if i >= upper_bound:
                raise WidthError(i, width)
            return l(i)

        return func

    def __init__(self, input, output, addr_radix, data_radix, width, depth, comments, **kwargs):
        self._input = input
        self._output = output
        self._addr_radix_f = Assembler._radix_function(addr_radix, width)
        self._data_radix_f = Assembler._radix_function(data_radix, width)
        self._width = width
        self._depth = depth
        self._comments = comments

