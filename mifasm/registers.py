class Register(object):
    def __init__(self, name, regno):
        self.name = name
        self.regno = regno

R0 = Register('R0', 0)
R1 = Register('R1', 1)
R2 = Register('R2', 2)
R3 = Register('R3', 3)
R4 = Register('R4', 4)
R5 = Register('R5', 5)
R6 = Register('R6', 6)
R7 = Register('R7', 7)
R8 = Register('R8', 8)
R9 = Register('R9', 9)
R10 = Register('R10', 10)
R11 = Register('R11', 11)
R12 = Register('R12', 12)
R13 = Register('R13', 13)
R14 = Register('R14', 14)
R15 = Register('R15', 15)
# aliases
A0 = Register('A0', 0) # function args, caller saved
A1 = Register('A1', 1)
A2 = Register('A2', 2)
A3 = Register('A3', 3)
RV = Register('RV', 3) # return value, caller saved
T0 = Register('T0', 4) # temporaries, caller saved
T1 = Register('T1', 5)
S0 = Register('S0', 6) # callee saved
S1 = Register('S1', 7)
S2 = Register('S2', 8)
GP = Register('GP', 12) # global ptr
FP = Register('FP', 13) # frame ptr
SP = Register('SP', 14) # stack ptr
RA = Register('RA', 15) # return address
