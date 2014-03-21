import unittest
from pprint import pprint
from bitstring import Bits

from mifasm.exceptions import *
from mifasm.instructions import *
from mifasm.registers import *
from mifasm.target import *

class InstructionTestCase(unittest.TestCase):
    def test_some_instructions(self):
        # some immediates
        neg_one = Bits(int=-1, length=16)
        zero = Bits(int=0, length=16)
        one = Bits(int=1, length=16)

        assert NAND(T0, FP, FP).hex == '04dd000c'
        assert ADDI(S0, S0, neg_one).hex == '8660ffff'
        assert JAL(T1, T0, zero).radix() == 'b5400000'
        assert NOP().radix('hex') == '04440004' == AND(T0, T0, T0).hex
        assert NOT(R0, R0).hex == '0000000c' == NAND(R0, R0, R0).hex
        assert CALL(R0, one).hex == 'bf000001' == JAL(RA, R0, one).hex
        assert RET().hex == 'b9f00000' == JAL(R9, RA, zero).hex
        assert JMP(R3,neg_one).hex == 'b930ffff' == JAL(R9, R3, neg_one).hex

class TargetTestCase(unittest.TestCase):
    def test_output(self):
        pass
        # t = Target(128, 32, 'hex', 'hex')
        # t.append(MemLoc(RET().bits))
        # t.append(MemLoc(RET().bits))
        # t.append(MemLoc(RET().bits))
        # print(len(t))
        # t.fill_space()
        # print(len(t))
        # t.compress()
        # print(len(t))
        # pprint(t.out())
