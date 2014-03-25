import unittest
from nose.tools import *
from pprint import pprint
from StringIO import StringIO

from mifasm import MBitArray
from mifasm.instructions import *
from mifasm.registers import *
from mifasm.target import Target
from mifasm.memloc import MemLoc, InstructionMemLoc
from mifasm.scanner import Scanner

class MifasmTestCase(unittest.TestCase):
    def setUp(self):
        # some immediates
        self.neg_one = MBitArray(int=-1, length=16)
        self.zero = MBitArray(int=0, length=16)
        self.one = MBitArray(int=1, length=16)


class InstructionTestCase(MifasmTestCase):
    def test_some_instructions(self):
        eq_(NAND(T0, FP, FP).hex, '04dd000c')
        eq_(ADDI(S0, S0, self.neg_one).hex, '8660ffff')
        eq_(JAL(T1, T0, self.zero).radix(), 'b5400000')

        eq_(NOP().radix('hex'), '04440004')
        eq_(NOP().hex, AND(T0, T0, T0).hex)

        eq_(NOT(R0, R0).hex, '0000000c')
        eq_(NOT(R0, R0).hex, NAND(R0, R0, R0).hex)

        eq_(CALL(R0, self.one).hex, 'bf000001')
        eq_(CALL(R0, self.one).hex, JAL(RA, R0, self.one).hex)

        eq_(RET().hex, 'b9f00000')
        eq_(RET().hex, JAL(R9, RA, self.zero).hex)

        eq_(JMP(R3, self.neg_one).hex, 'b930ffff')
        eq_(JMP(R3, self.neg_one).hex, JAL(R9, R3, self.neg_one).hex)

    def test_str(self):
        mvhi = MVHI(R0, self.zero)
        eq_(str(mvhi), "MVHI R0, 0x0000")
        eq_(mvhi.verbose_str(), "R0 := 0x0000 << 16")

        jal = JAL(R0, FP, self.zero)
        eq_(str(jal), "JAL R0, 0x0000(FP)")
        eq_(jal.verbose_str(), "R0 := PC + 4; PC := FP + sxt(0x0000)")


class TargetTestCase(MifasmTestCase):
    def setUp(self):
        t = Target('hex', 'hex', depth=128, width=32)

    def test_output(self):
        pass
        t = Target('hex', 'hex', depth=128, width=32)
        # t.place(MemLoc(BT(uint=1337, length=32)))
        # t.place(MemLoc(BT(uint=1337, length=32), comment="This is a comment"))
        # t.place(InstructionMemLoc(RET()))
        # t.place(InstructionMemLoc(NAND(T0, FP, A0), verbose=True))
        # t.place(InstructionMemLoc(JMP(R3, self.zero), verbose=True))
        # t.place(InstructionMemLoc(CALL(FP, self.neg_one)))
        # t.set_cursor(Address.from_int(12))
        # t.place(InstructionMemLoc(SW(R0, R0, self.zero)))
        # t.set_cursor(Address.from_int(5))
        # t.place(InstructionMemLoc(LW(R0, R1, self.one)))
        # t.set_cursor(Address.from_int((512)/2))
        # t.place(InstructionMemLoc(GTEZI(A0, T1, self.neg_one)))
        # print(t.out(compress=True))
        # raise Exception

    def test_compress(self):
        pass

class ScannerTestCase(MifasmTestCase):
    def setUp(self):
        super(ScannerTestCase, self).setUp()

        source = [
                NAND(R0, R1, R2),
                JAL(T1, T0, self.zero),
                BLT(A0, T1, self.zero),
                LT(R0, R1, R2),
                GTEZ(R0, R1, R2),
                SH(R0, R1, self.one),
                NOP(),
                GTEZI(R0, R1, self.one),
                LW(R0, R1, self.one),
                SUBI(SP, GP, self.neg_one)]
        source = [str(i) for i in source]
        self.cleansed_source = "\n".join(source)

        source.insert(0, "# this is a comment at the beginning of the file")
        source.insert(len(source), "# end comment")
        source[3]  = source[3] + " # comment here"
        source[7]  = source[7] + " # comment here"
        source.insert(4, "")
        source.insert(1, "")
        self.source = "\n".join(source)
        self.source_f = StringIO(self.source)

    def test_readlines(self):
        scanner = Scanner(self.source_f)
        eq_(self.cleansed_source, "\n".join(scanner.readlines()))

    def test_cleanse(self):
        line = "#comment"
        eq_(Scanner.cleanse_line(line), "")

        line = ""
        eq_(Scanner.cleanse_line(line), "")

        line = "code # comment"
        eq_(Scanner.cleanse_line(line), "code")

    def test_line_has_content(self):
        line = ""
        assert not Scanner.line_has_content(line)

        line = "code"
        assert Scanner.line_has_content(line)
