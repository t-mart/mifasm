import unittest

from mifasm.exceptions import *
from mifasm.instructions import *
from mifasm.registers import *

class InstructionTestCase(unittest.TestCase):
    def test_some_things(self):
        assert NAND(T0, FP, FP).code() == '04dd000c'
        assert ADDI(S0, S0, 1).code() == '86600001'
        assert JAL(T1, T0, 0).code() == 'b5400000'
