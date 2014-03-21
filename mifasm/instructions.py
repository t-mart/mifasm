import sys
from bitstring import Bits

from .registers import *
from .util import BitsT

# this some hacky shit right here, but it really reduces code size
# if you understand how the following works, you understand dynamic python

class __OP1(object):
    def __init__(self, name, code, op2_dict):
        self.name = name
        self.code = code
        self.op2_dict = op2_dict

__LOAD_OP2 = {
        'LW': '0000',
        'LH': '0001',
        'LB': '0010'}

__STORE_OP2 = {
        'SW': '0000',
        'SH': '0001',
        'SB': '0010'}

__ALUR_OP2 = {
        'ADD': '0000',
        'SUB': '0001',
        'AND': '0100',
        'OR': '0101',
        'XOR': '0110',
        'NAND': '1100',
        'NOR': '1101',
        'NXOR': '1110'}

__ALUI_OP2 = {
        'ADDI': '0000',
        'SUBI': '0001',
        'ANDI': '0100',
        'ORI': '0101',
        'XORI': '0110',
        'NANDI': '1100',
        'NORI': '1101',
        'NXORI': '1110',
        'MVHI': '1011'}

__CMP_CMPI_BCOND_OP2 = {
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

__op1_list = [
        __OP1('ALUR', '0000', __ALUR_OP2),
        __OP1('CMPR', '0010', __CMP_CMPI_BCOND_OP2),
        __OP1('STORE', '0101', __STORE_OP2),
        __OP1('BCOND', '0110', __CMP_CMPI_BCOND_OP2),
        __OP1('ALUI', '1000', __ALUI_OP2),
        __OP1('LOAD', '1001', __LOAD_OP2),
        __OP1('CMPI', '1010', __CMP_CMPI_BCOND_OP2),
        __OP1('JAL', '1011', None)]


class Instruction(BitsT):
    def __init__(self, *args, **kwargs):
        super(Instruction, self).__init__(*args, **kwargs)

def __type_1_init(op1, op2):
    # Format used when OP1 is ALUR or CMPR
    # [ 0-3: op1,
    # 4-7: rd,
    # 8-11: rs,
    # 12-15: rt,
    # 16-27: 0(blank),
    # 28-31: op2 ]
    def init(self, rd, rs, rt):
        self._op1 = Bits(bin=op1)
        self._op2 = Bits(bin=op2)
        self._rd = rd.bits
        self._rs = rs.bits
        self._rt = rt.bits
        blank = Bits(int=0, length=12)
        self.bits = Bits(
                self._op1 + self._rd + self._rs + self._rt + \
                blank + self._op2)
    return init

def __type_2_init(op1, op2):
    # Format used when OP1 is STORE or BCOND
    # [ 0-3: op1,
    # 4-7: op2,
    # 8-11: rs,
    # 12-15: rt,
    # 16-31: imm ]
    def init(self, rs, rt, imm):
        self._op1 = Bits(bin=op1)
        self._op2 = Bits(bin=op2)
        self._rs = rs.bits
        self._rt = rt.bits
        self._imm = imm
        self.bits = Bits(
                self._op1 + self._op2 + self._rs + self._rt + \
                self._imm)
    return init

def __type_3_init(op1, op2):
    # Format used when OP1 is ALUI, CMPI, LOAD, JAL
    # [ 0-3: op1,
    # 4-7: rd,
    # 8-11: rs,
    # 12-15: op2,
    # 16-31: imm ]
    def init(self, rd, rs, imm):
        self._op1 = Bits(bin=op1)
        self._op2 = Bits(bin=op2)
        self._rd = rd.bits
        self._rs = rs.bits
        self._imm = imm
        self.bits = Bits(
                self._op1 + self._rd + self._rs + self._op2 + \
                self._imm)
    return init

INSTRUCTIONS = {}

for op1 in __op1_list:
    instr_type = 0
    if op1.name != 'JAL':
        if op1.name in ['ALUR', 'CMPR']:
            init = __type_1_init
            instr_type = 1
        elif op1.name in ['STORE', 'BCOND']:
            init = __type_2_init
            instr_type = 2
        else:
            init = __type_3_init
            instr_type = 3

        for op2_name, op2_code in op1.op2_dict.iteritems():
            if op1.name == 'BCOND':
                instr_name = 'B' + op2_name
            elif op1.name == 'CMPI':
                instr_name = op2_name + 'I'
            else:
                instr_name = op2_name

            instr_cls = type(instr_name, (Instruction,), {'instr_type':instr_type})
            instr_cls.__init__ = init(op1.code, op2_code)
            setattr(sys.modules[__name__], instr_name, instr_cls)
            INSTRUCTIONS[instr_name] = instr_cls
    else:
        # JAL breaks the convention by not having an OP2, so we build it
        # specially here
        instr_name = 'JAL'
        instr_type = 3
        init = __type_3_init
        instr_cls = type(instr_name, (Instruction,), {'instr_type':instr_type})
        instr_cls.__init__ = init(op1.code, '0000')
        setattr(sys.modules[__name__], instr_name, instr_cls)
        INSTRUCTIONS[instr_name] = instr_cls


# psuedo instructions
class NOT(NAND):
    def __init__(self, rd, rs):
        super(NOT, self).__init__(rd=rd, rs=rs, rt=rs)
INSTRUCTIONS['NOT'] = NOT


class CALL(JAL):
    def __init__(self, rs, imm):
        super(CALL, self).__init__(rd=RA, rs=rs, imm=imm)
INSTRUCTIONS['CALL'] = CALL

zero = Bits(int=0, length=16)

class RET(JAL):
    def __init__(self):
        super(RET, self).__init__(rd=R9, rs=RA, imm=zero)
INSTRUCTIONS['RET'] = RET


class JMP(JAL):
    def __init__(self, rs, imm):
        super(JMP, self).__init__(rd=R9, rs=rs, imm=imm)
INSTRUCTIONS['JMP'] = JMP

# what should a NOP be? choosing AND T0, T0, T0 for now, but might this impose
# artificial pipeline hazards if following instructions depend on T0 when all
# we really wanted is just a 1 cycle stall
class NOP(AND):
    def __init__(self):
        super(NOP, self).__init__(rd=T0, rs=T0, rt=T0)
INSTRUCTIONS['NOP'] = NOP

