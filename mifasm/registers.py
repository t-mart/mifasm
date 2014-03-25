import sys

from . import MBitArray

class Register(MBitArray):
    def __init__(self, name, regno):
        super(Register, self).__init__(uint=regno, length=4)
        self.name = name

    def __str__(self):
        return self.name

__reg_dict = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    # aliases
    'A0': 0,
    'A1': 1,
    'A2': 2,
    'A3': 3,
    'RV': 3,
    'T0': 4,
    'T1': 5,
    'S0': 6,
    'S1': 7,
    'S2': 8,
    'GP': 12,
    'FP': 13,
    'SP': 14,
    'RA': 15}

REGISTERS = {}

for reg_name, reg_no in __reg_dict.iteritems():
    obj = Register(reg_name, reg_no)
    setattr(sys.modules[__name__], reg_name, obj)
    REGISTERS[reg_name] = obj

__all__ = ['REGISTERS', 'Register']
__all__.extend([cls_name for cls_name in REGISTERS.keys()])
