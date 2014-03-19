from .exceptions import *

class Value(object):

    radix_names = ['bin', 'oct', 'hex', 'dec', 'udec']

    @staticmethod
    def parse_bin(value):
        return int(value, 2)

    @staticmethod
    def parse_oct(value):
        return int(value, 8)

    @staticmethod
    def parse_hex(value):
        return int(value, 16)

    @staticmethod
    def parse_dec(value):
        return int(value)

    @staticmethod
    def parse_udec(value):
        return int(value)

    @staticmethod
    def _width_mask(width):
        width_mask = int(''.join(['1' for i in range(width)]),2)
        return width_mask

    @staticmethod
    def unparse_bin(i, width):
        return ("{0:0>%db}" % (width)).format(i & Value._width_mask(width))

    @staticmethod
    def unparse_oct(i, width):
        return ("{0:0>%do}" % (width//3)).format(i & Value._width_mask(width))

    @staticmethod
    def unparse_hex(i, width):
        return ("{0:0>%dx}" % (width//4)).format(i & Value._width_mask(width)).upper()

    @staticmethod
    def unparse_dec(i, width):
        if i > 2**(width-1):
            i = -((2**width)-i)
        return "{0:0>d}".format(i)

    @staticmethod
    def unparse_udec(i, width):
        return "{0:0>d}".format(i & Value._width_mask(width))


    def __init__(self, value, width):

        self.width = width

        value = str(value)

        if value[0:1] == '-':
            try:
                self.value = Value.parse_dec(value)
            except ValueError:
                raise BadValueError(value)

            if self.value < -(2**(width-1)):
                raise WidthError(self.value, 'dec', self.width)
        else:
            try:
                if value[0:2] == '0b':
                    self.value = Value.parse_bin(value[2:])
                    type = 'bin'
                elif value[0:2] == '0x':
                    self.value = Value.parse_hex(value[2:])
                    type = 'hex'
                elif value[0:1] == '0':
                    # note that binary and hex also start with 0, but we've already
                    # checked those
                    self.value = Value.parse_oct(value[1:])
                    type = 'oct'
                else:
                    self.value = Value.parse_udec(value)
                    type = 'udec'
            except ValueError:
                raise BadValueError(value)

            if self.value > (2**(width))-1:
                raise WidthError(self.value, type, self.width)

    @property
    def bin(self):
        return Value.unparse_bin(self.value, self.width)

    @property
    def oct(self):
        return Value.unparse_oct(self.value, self.width)

    @property
    def hex(self):
        return Value.unparse_hex(self.value, self.width)

    @property
    def dec(self):
        return Value.unparse_dec(self.value, self.width)

    @property
    def udec(self):
        return Value.unparse_udec(self.value, self.width)
