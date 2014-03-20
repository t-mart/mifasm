import unittest

from mifasm.exceptions import *
from mifasm.instructions import *
from mifasm.registers import *

class InstructionTestCase(unittest.TestCase):
    def test_some_instructions(self):
        assert NAND(T0, FP, FP).code() == '04dd000c'
        assert ADDI(S0, S0, 1).code() == '86600001'
        assert JAL(T1, T0, 0).code() == 'b5400000'
        assert NOP().code() == '04440004' == AND(T0, T0, T0).code()
        assert NOT(R0, R0).code() == '0000000c' == NAND(R0, R0, R0).code()
        assert CALL(R0, 5).code() == 'bf000005' == JAL(RA, R0, 5).code()
        assert RET().code() == 'b9f00000' == JAL(R9, RA, 0).code()
        assert JMP(R3,4).code() == 'b9300004' == JAL(R9, R3, 4).code()
