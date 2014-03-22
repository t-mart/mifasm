import unittest
from pprint import pprint
from bitstring import Bits

from mifasm.instructions import *
from mifasm.registers import *
from mifasm.target import Target
from mifasm.memloc import MemLoc, InstructionMemLoc
from mifasm.util import BitsT

class MifasmTestCase(unittest.TestCase):
    def setUp(self):
        # some immediates
        self.neg_one = Bits(int=-1, length=16)
        self.zero = Bits(int=0, length=16)
        self.one = Bits(int=1, length=16)

class InstructionTestCase(MifasmTestCase):
    def test_some_instructions(self):
        assert NAND(T0, FP, FP).hex == '04dd000c'
        assert ADDI(S0, S0, self.neg_one).hex == '8660ffff'
        assert JAL(T1, T0, self.zero).radix() == 'b5400000'
        assert NOP().radix('hex') == '04440004' == AND(T0, T0, T0).hex
        assert NOT(R0, R0).hex == '0000000c' == NAND(R0, R0, R0).hex
        assert CALL(R0, self.one).hex == 'bf000001' == JAL(RA, R0, self.one).hex
        assert RET().hex == 'b9f00000' == JAL(R9, RA, self.zero).hex
        assert JMP(R3, self.neg_one).hex == 'b930ffff' == JAL(R9, R3, self.neg_one).hex

    def test_str(self):
        mvhi = MVHI(R0, self.zero)
        assert str(mvhi) == "MVHI R0, 0x0000"
        assert mvhi.verbose_str() == "R0 := 0x0000 << 16"

        jal = JAL(R0, FP, self.zero)
        assert str(jal) == "JAL R0, 0x0000(FP)"
        assert jal.verbose_str() == "R0 := PC + 4; PC := FP + sxt(0x0000)"

class TargetTestCase(MifasmTestCase):
    def test_output(self):
        t = Target('hex', 'hex', depth=8, width=32)
        t.append(MemLoc(BitsT(Bits(uint=1337, length=32))))
        t.append(MemLoc(BitsT(Bits(uint=1337, length=32)), comment="This is a comment"))
        t.append(InstructionMemLoc(RET()))
        t.append(InstructionMemLoc(NAND(T0, FP, A0), verbose=True))
        t.append(InstructionMemLoc(JMP(R3, self.zero), verbose=True))
        t.append(InstructionMemLoc(CALL(FP, self.neg_one)))
        print(t.out(compress=True))
        raise Exception()
