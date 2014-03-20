import sys
from bitstring import Bits

from .registers import *

# this some hacky shit right here, but it really reduces code size
# if you understand how the following works, you understand dynamic python

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
        'NXORI': '1110',
        'MVHI': '1011'}

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

class OP1(object):
    def __init__(self, name, code, op2_dict):
        self.name = name
        self.code = code
        self.op2_dict = op2_dict

op1_list = [
        OP1('ALUR', '0000', _ALUR_OP2),
        OP1('CMPR', '0010', _CMP_CMPI_BCOND_OP2),
        OP1('STORE', '0101', _STORE_OP2),
        OP1('BCOND', '0110', _CMP_CMPI_BCOND_OP2),
        OP1('ALUI', '1000', _ALUI_OP2),
        OP1('LOAD', '1001', _LOAD_OP2),
        OP1('CMPI', '1010', _CMP_CMPI_BCOND_OP2),
        OP1('JAL', '1011', None)]

class Instruction(object):
    def __init__(self, bits):
        # this won't be executed, but is here for completeness
        self.bits = bits

    def code(self, radix='hex'):
        if radix in ['hex', 'bin', 'oct', 'int', 'uint']:
            # NOTE: you can only make an umabiguous oct representation if the
            # width of the value is a multiple of 3, and mifasm defaults to
            # 32b which is not a multiple of 3. therefore, we append another
            # zeroed bit to make it 33. this technically isn't the same as the
            # 32b representation. also, we need to test if quartus freaks when
            # it sees width not a multiple of 3, yet oct output is chosen
            if radix == 'oct':
                return ([0] + self.bits).oct
            return getattr(self.bits, radix)
        else:
            raise ValueError("radix {radix} is not supported".format(radix=radix))

def type_1_init(op1, op2):
    # Format used when OP1 is ALUR or CMPR
    # [ 0-3: op1,
    # 4-7: rd,
    # 8-11: rs,
    # 12-15: rt,
    # 16-27: 0,
    # 28-31: op2 ]
    def init(self, rd, rs, rt):
        self.op1 = op1
        self.op2 = op2
        self.rd = rd
        self.rs = rs
        self.rt = rt
        self.bits = Bits(
                'bin:4={op1}, int:4={rd}, uint:4={rs}, uint:4={rt},'
                'int:12=0, bin:4={op2}'.format(
                    op1=op1, op2=op2, rd=rd.regno, rs=rs.regno, rt=rt.regno))
    return init

def type_2_init(op1, op2):
    # Format used when OP1 is STORE or BCOND
    # [ 0-3: op1,
    # 4-7: op2,
    # 8-11: rs,
    # 12-15: rt,
    # 16-31: imm ]
    def init(self, rs, rt, imm):
        self.op1 = op1
        self.op2 = op2
        self.rs = rs
        self.rt = rt
        self.imm =imm
        self.bits = Bits(
                'bin:4={op1}, bin:4={op2}, uint:4={rs}, uint:4={rt},'
                'int:16={imm}'.format(
                    op1=op1, op2=op2, rs=rs.regno, rt=rt.regno, imm=imm))
    return init

def type_3_init(op1, op2):
    # Format used when OP1 is ALUI, CMPI, LOAD, JAL
    # [ 0-3: op1,
    # 4-7: rd,
    # 8-11: rs,
    # 12-15: op2,
    # 16-31: imm ]
    def init(self, rd, rs, imm):
        self.op1 = op1
        self.op2 = op2
        self.rs = rs
        self.rd = rd
        self.imm = imm
        self.bits = Bits(
                'bin:4={op1}, uint:4={rd}, uint:4={rs}, bin:4={op2},'
                'int:16={imm}'.format(
                    op1=op1, op2=op2, rs=rs.regno, rd=rd.regno, imm=imm))
    return init

__all__ = []

for op1 in op1_list:
    instr_type = 0
    if op1.name != 'JAL':
        if op1.name in ['ALUR', 'CMPR']:
            init = type_1_init
            instr_type = 1
        elif op1.name in ['STORE', 'BCOND']:
            init = type_2_init
            instr_type = 2
        else:
            init = type_3_init
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
            __all__.append(instr_name)
    else:
        # JAL breaks the convention by not having an OP2, so we do it
        # specially here
        instr_name = 'JAL'
        instr_type = 3
        init = type_3_init
        instr_cls = type(instr_name, (Instruction,), {'instr_type':instr_type})
        instr_cls.__init__ = init(op1.code, '0000')
        setattr(sys.modules[__name__], instr_name, instr_cls)
        __all__.append(instr_name)


# psuedo instructions
class NOT(NAND):
    def __init__(self, rd, rs):
        super(NOT, self).__init__(rd=rd, rs=rs, rt=rs)


class CALL(JAL):
    def __init__(self, rs, imm):
        super(CALL, self).__init__(rd=RA, rs=rs, imm=imm)


class RET(JAL):
    def __init__(self):
        super(RET, self).__init__(rd=R9, rs=RA, imm=0)


class JMP(JAL):
    def __init__(self, rs, imm):
        super(JMP, self).__init__(rd=R9, rs=rs, imm=imm)

# what should a NOP be? choosing AND T0, T0, T0 for now, but might this impose
# artificial pipeline hazards if following instructions depend on T0 when all
# we really wanted is just a 1 cycle stall
class NOP(AND):
    def __init__(self):
        super(NOP, self).__init__(rd=T0, rs=T0, rt=T0)

