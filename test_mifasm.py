import unittest

from mifasm.exceptions import *
from mifasm.value import Value

class ValueTestCase(unittest.TestCase):

    def test_value_limits(self):
        w = 8

        with self.assertRaises(WidthError):
            Value('-129',w)
        Value('-128',w)

        with self.assertRaises(WidthError):
            Value('256',w)
        Value('255',w)

        with self.assertRaises(WidthError):
            Value('100000000',w)
        Value('0b11111111',w)

        with self.assertRaises(WidthError):
            Value('0x100',w)
        Value('0xFF',w)

        with self.assertRaises(WidthError):
            Value('0400',w)
        Value('0377',w)


    def test_negative_dec_value(self):
        i = -19
        s = str(i)
        w = 8
        v = Value(s, w)

        assert v.value == i

        assert v.bin == '11101101'
        assert v.oct == '355'
        assert v.hex == 'ED'
        assert v.udec == '237'
        assert v.dec == '-19'

    def test_positive_dec_value(self):
        i = 19
        s = str(i)
        w = 8
        v = Value(s, w)

        assert v.value == i

        assert v.bin == '00010011'
        assert v.oct == '23'
        assert v.hex == '13'
        assert v.udec == '19'
        assert v.dec == '19'

    def test_negative_bin_value(self):
        b = '0b10011001'
        v = Value(b, 8)

        assert v.value == 153

        assert v.bin == b[2:]
        assert v.oct == '231'
        assert v.hex == '99'
        assert v.dec == '-103'
        assert v.udec == '153'

    def test_positive_bin_value(self):
        b = '0b00011001'
        v = Value(b, 8)

        assert v.value == 25

        assert v.bin == b[2:]
        assert v.oct == '31'
        assert v.hex == '19'
        assert v.dec == '25'
        assert v.udec == '25'

    def test_upper_udec_value(self):
        i = '182'
        v = Value(i, 8)

        assert v.value == 182

        assert v.bin == '10110110'
        assert v.oct == '266'
        assert v.hex == 'B6'
        assert v.dec == '-74'
        assert v.udec == '182'

    def test_lower_udec_value(self):
        i = '4'
        v = Value(i, 8)

        assert v.value == 4

        assert v.bin == '00000100'
        assert v.oct == '04'
        assert v.hex == '04'
        assert v.dec == '4'
        assert v.udec == '4'

    def test_positive_octal(self):
        i = '077'
        v = Value(i, 8)

        assert v.value == 63

        assert v.bin == '00111111'
        assert v.oct == i[1:]
        assert v.hex == '3F'
        assert v.dec == '63'
        assert v.udec == '63'


    def test_negative_octal(self):
        i = '0277'
        v = Value(i, 8)

        assert v.value == 191

        assert v.bin == '10111111'
        assert v.oct == i[1:]
        assert v.hex == 'BF'
        assert v.dec == '-65'
        assert v.udec == '191'

    def test_positive_hex(self):
        i = '0x20'
        v = Value(i, 8)

        assert v.value == 32

        assert v.bin == '00100000'
        assert v.oct == '40'
        assert v.hex == i[2:]
        assert v.dec == '32'
        assert v.udec == '32'

    def test_negative_hex(self):
        i = '0xA7'
        v = Value(i, 8)

        assert v.value == 167

        assert v.bin == '10100111'
        assert v.oct == '247'
        assert v.hex == i[2:]
        assert v.dec == '-89'
        assert v.udec == '167'

    def test_bad_value(self):
        with self.assertRaises(BadValueError):
            Value('',8)
        with self.assertRaises(BadValueError):
            Value('not a number', 8)
