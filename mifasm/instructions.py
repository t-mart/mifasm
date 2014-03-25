import sys

from . import MBitArray
from .registers import *

# this some hacky shit right here, but it really reduces code size
# if you understand how the following works, you understand dynamic python
# frankly, i hope i never have to look at this again because its really hard to
# read, but the mindlessness of writing it the non-dynamic way would have
# killed me.

class _OP1(object):
    def __init__(self, name, code, op2_dict):
        self.name = name
        self.code = code
        self.op2_dict = op2_dict

_LOAD_OP2 = {
        'LW': '0000',
        'LH': '0001',
        'LB': '0010'}

_STORE_OP2 = {
        'SW': '0000',
        'SH': '0001',
        'SB': '0010'}

_ALUR_OP2 = {
        'ADD': '0000',
        'SUB': '0001',
        'AND': '0100',
        'OR': '0101',
        'XOR': '0110',
        'NAND': '1100',
        'NOR': '1101',
        'NXOR': '1110'}

_ALUI_OP2 = {
        'ADDI': '0000',
        'SUBI': '0001',
        'ANDI': '0100',
        'ORI': '0101',
        'XORI': '0110',
        'NANDI': '1100',
        'NORI': '1101',
        'NXORI': '1110'}

_CMP_CMPI_BCOND_OP2 = {
        'F': '0000',
        'EQ': '0001',
        'LT': '0010',
        'LTE': '0011',
        'EQZ': '0101',
        'LTZ': '0110',
        'LTEZ': '0111',
        'T': '1000',
        'NE': '1001',
        'GTE': '1010',
        'GT': '1011',
        'NEZ': '1101',
        'GTEZ': '1110',
        'GTZ': '1111'}

_ALUI = _OP1('ALUI', '1000', _ALUI_OP2)
_ALUR = _OP1('ALUR', '0000', _ALUR_OP2)
_CMPR = _OP1('CMPR', '0010', _CMP_CMPI_BCOND_OP2)
_CMPI = _OP1('CMPI', '1010', _CMP_CMPI_BCOND_OP2)
_BCOND = _OP1('BCOND', '0110', _CMP_CMPI_BCOND_OP2)
_LOAD = _OP1('LOAD', '1001', _LOAD_OP2)
_STORE = _OP1('STORE', '0101', _STORE_OP2)

_op1_list = [
        _ALUI, _ALUR, _CMPR, _CMPI, _BCOND, _LOAD, _STORE]

class Instruction(MBitArray):
    def __init__(self, *args, **kwargs):
        super(Instruction, self).__init__(*args, **kwargs)

def _all_init(self, op1, op2):
    self._op1 = MBitArray(bin=op1)
    self._op2 = MBitArray(bin=op2)
    self.name = self.__class__.__name__

def _type_1_init(cls, op1, op2):
    # Format used when OP1 is ALUR or CMPR
    # [ 0-3: op1,
    # 4-7: rd,
    # 8-11: rs,
    # 12-15: rt,
    # 16-27: 0(blank),
    # 28-31: op2 ]
    def init(self, rd, rs, rt):
        _all_init(self, op1, op2)
        self._rd = rd
        self._rs = rs
        self._rt = rt
        blank = MBitArray(int=0, length=12)

        whole = MBitArray.from_mbitarray_list([self._op1, self._rd, self._rs, self._rt, blank, self._op2])
        # super(type(self), self).__init__(whole)
        super(cls, self).__init__(whole)
    return init

def _type_1_str(self):
    return "{name} {rd}, {rs}, {rt}".format(name=self.name, rd=self._rd,
            rs=self._rs, rt=self._rt)

def _type_1_verbose_str(self):
    return "{rd} := {rs} {name} {rt}".format(name=self.name, rd=self._rd,
            rs=self._rs, rt=self._rt)

def _type_2_init(cls, op1, op2):
    # Format used when OP1 is STORE or BCOND
    # [ 0-3: op1,
    # 4-7: op2,
    # 8-11: rs,
    # 12-15: rt,
    # 16-31: imm ]
    def init(self, rs, rt, imm):
        # _all_init(self, op1, op2)
        # self._rs = rs
        # self._rt = rt
        # self._imm = imm
        # self.bits = MBitArray(
                # self._op1 + self._op2 + self._rs.bits + self._rt.bits + self._imm)

        _all_init(self, op1, op2)
        self._rs = rs
        self._rt = rt
        self._imm = imm

        whole = MBitArray.from_mbitarray_list([self._op1, self._op2, self._rs, self._rt, self._imm])
        super(cls, self).__init__(whole)
    return init

def _type_2_str(self):
    if self.name.startswith('B'):
        return "{name} {rs}, {rt}, {imm}".format(
                name=self.name,
                rs=self._rs, rt=self._rt, imm=self._imm)
    else:
        return "{name} {rs}, {imm}({rt})".format(
                name=self.name,
                rs=self._rs, rt=self._rt, imm=self._imm)

def _type_2_verbose_str(self):
    if self.name.startswith('B'):
        return ("if ({rs} {name} {rt}) " \
                "then PC := PC + 4 + (sxt({imm}) * 4)").format(
                        name=self.name, rd=self._rd,
                        rs=self._rs, rt=self._rt, imm=self._imm)
    else:
        return "mem[{rs + sxt({imm}] := {rt}".format(
                name=self.name, rd=self._rd,
                rs=self._rs, rt=self._rt, imm=self._imm)

def _type_3_init(cls, op1, op2):
    # Format used when OP1 is ALUI, CMPI, LOAD
    # [ 0-3: op1,
    # 4-7: rd,
    # 8-11: rs,
    # 12-15: op2,
    # 16-31: imm ]
    # MVHI is defined explicitly later because its doesn't need an rs
    # JAL is defined later because it doesn't use op2
    def init(self, rd, rs, imm):
        # _all_init(self, op1, op2)
        # self._rd = rd
        # self._rs = rs
        # self._imm = imm
        # self.bits = MBitArray(
                # self._op1 + self._rd.bits + self._rs.bits + self._op2 + self._imm)
    # return init
        _all_init(self, op1, op2)
        self._rd = rd
        self._rs = rs
        self._imm = imm

        whole = MBitArray.from_mbitarray_list([self._op1, self._rd, self._rs, self._op2, self._imm])
        super(cls, self).__init__(whole)
    return init

def _type_3_str(self):
    if self.name.startswith('L'):
        return "{name} {rd}, {imm}({rs})".format(
                name=self.name, rd=self._rd, imm=self._imm, rs=self._rs)
    else:
        return "{name} {rd}, {rs}, {imm}".format(
                name=self.name, rd=self._rd, imm=self._imm, rs=self._rs)

def _type_3_verbose_str(self):
    if self.name.startswith('L'):
        return "{name} {rd}, {imm}({rs})".format(
                name=self._name, rd=self._rd, imm=self._imm, rs=self._rs)
    else:
        return "{rd} := {rs} {name} {imm}".format(
                name=self._name, rd=self._rd, imm=self._imm, rs=self._rs)

INSTRUCTIONS = {}

for op1 in _op1_list:
    if op1.name in ['ALUR', 'CMPR']:
        initf = _type_1_init
        strf = _type_1_str
        verbose_strf = _type_1_verbose_str
    elif op1.name in ['STORE', 'BCOND']:
        initf = _type_2_init
        strf = _type_2_str
        verbose_strf = _type_2_verbose_str
    else:
        initf = _type_3_init
        strf = _type_3_str
        verbose_strf = _type_3_verbose_str

    for op2_name, op2_code in op1.op2_dict.iteritems():
        if op1.name == 'BCOND':
            instr_name = 'B' + op2_name
        elif op1.name == 'CMPI':
            instr_name = op2_name + 'I'
        else:
            instr_name = op2_name

        instr_cls = type(instr_name, (Instruction,), {'__str__':strf, 'verbose_str':verbose_strf})
        instr_cls.__init__ = initf(instr_cls, op1.code, op2_code)
        setattr(sys.modules[__name__], instr_name, instr_cls)
        INSTRUCTIONS[instr_name] = instr_cls

# Convention breaking instructions
# MVHI breaks the form of typical ALUI instructions (no rs needed)
class MVHI(Instruction):
    def __init__(self, rd, imm):
        _type_3_init(MVHI, _ALUI.code, '1011')(self, rd=rd, rs=T0, imm=imm)
        print('here')

    def __str__(self):
        return "MVHI {rd}, {imm}".format(rd=self._rd, imm=self._imm)

    def verbose_str(self):
        return "{rd} := {imm} << 16".format(rd=self._rd, imm=self._imm)
INSTRUCTIONS['MVHI'] = MVHI

# JAL breaks form of not having OP2
class JAL(Instruction):
    def __init__(self, rd, rs, imm):
        _type_3_init(JAL, '1011', '0000')(self, rd=rd, rs=rs, imm=imm)

    def __str__(self):
        return "{name} {rd}, {imm}({rs})".format(
                name=self.name, rd=self._rd, imm=self._imm, rs=self._rs)

    def verbose_str(self):
        return "{rd} := PC + 4; PC := {rs} + sxt({imm})".format(
                name=self.name, rd=self._rd, imm=self._imm, rs=self._rs)
INSTRUCTIONS['JAL'] = JAL

# psuedo instructions
class NOT(NAND):
    def __init__(self, rd, rs):
        super(NOT, self).__init__(rd=rd, rs=rs, rt=rs)

    def __str__(self):
        return "NOT {rd}, {rs}".format(
                name=self.name, rd=self._rd, rs=self._rs)

    def verbose_str(self):
        return "{rd} := NOT {rs}".format(
                name=self.name, rd=self._rd, rs=self._rs)
INSTRUCTIONS['NOT'] = NOT


class CALL(JAL):
    def __init__(self, rs, imm):
        super(CALL, self).__init__(rd=RA, rs=rs, imm=imm)

    def __str__(self):
        return "CALL {imm}({rs})".format( imm=self._imm, rs=self._rs)
INSTRUCTIONS['CALL'] = CALL

zero = MBitArray(int=0, length=16)

class RET(JAL):
    def __init__(self):
        super(RET, self).__init__(rd=R9, rs=RA, imm=zero)

    def __str__(self):
        return "RET"
INSTRUCTIONS['RET'] = RET


class JMP(JAL):
    def __init__(self, rs, imm):
        super(JMP, self).__init__(rd=R9, rs=rs, imm=imm)

    def __str__(self):
        return "JMP {imm}({rs})".format( imm=self._imm, rs=self._rs)
INSTRUCTIONS['JMP'] = JMP

# what should a NOP be? choosing AND T0, T0, T0 for now, but might this impose
# artificial pipeline hazards if following instructions depend on T0 when all
# we really wanted is just a 1 cycle stall
class NOP(AND):
    def __init__(self):
        super(NOP, self).__init__(rd=T0, rs=T0, rt=T0)

    def __str__(self):
        return "NOP"

    verbose_str = __str__
INSTRUCTIONS['NOP'] = NOP

__all__ = ['INSTRUCTIONS', 'Instruction']
__all__.extend([cls_name for cls_name in INSTRUCTIONS.keys()])
