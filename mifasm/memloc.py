from bitstring import Bits

from .util import Address

class MemLoc(object):
    def __init__(self, data, length=1, comment=""):
        self.data = data
        self.length = length
        self.comment = comment

    def __eq__(self, other):
        return self.data == other.data

    def end_address(self, start_address):
        """given an address, return the last address this memloc consumes"""
        end_addr = Address.from_int(start_address.bits.uint + self.length - 1)
        return end_addr

    def next_address(self, start_address):
        """given a starting address, return the next address that would be
        after this memloc"""
        end_addr = Address.from_int(start_address.bits.uint + self.length)
        return end_addr

    def comment_line(self):
        if len(self.comment) == 0:
            return ""
        else:
            comment_line = "-- {comment}".format(comment=self.comment)
            return comment_line

    def out(self, address, addr_radix='hex', data_radix='hex'):
        s = self.comment_line()
        if self.length == 1:
            s = self._single_loc_out(address, addr_radix, data_radix)
        else:
            s = self._spanning_loc_out(address, addr_radix, data_radix)
        s = s.ljust(40)
        s += self.comment_line()
        return s

    def _single_loc_out(self, address, addr_radix='hex', data_radix='hex'):
        s = "{address} : {data};".format(
                address=address.radix(addr_radix),
                data=self.data.radix(data_radix))
        return s

    def _spanning_loc_out(self, address, addr_radix='hex', data_radix='hex'):
        start_addr = address.radix(addr_radix)
        end_addr = self.end_address(address).radix(addr_radix)
        s = "[{start_addr}..{end_addr}] : {data};".format(
                start_addr=start_addr,
                end_addr=end_addr,
                data=self.data.radix(data_radix))
        return s

    def __repr__(self):
        return "MemLoc(data={data}, length={length})".format(
                data=self.data, length=self.length)

    __str__ = __repr__


class InstructionMemLoc(MemLoc):
    def __init__(self, instruction, verbose=False, *args, **kwargs):
        self.instruction = instruction
        comment = InstructionMemLoc.instr_comment(instruction, verbose)
        super(InstructionMemLoc, self).__init__(instruction, comment=comment)

    @staticmethod
    def instr_comment(instruction, verbose):
        if not verbose:
            return str(instruction)
        else:
            return instruction.verbose_str()

    def __repr__(self):
        return "InstructionMemLoc(instruction=<{instruction}>, length={length}".format(
                instruction=self.instruction, length=self.length)

    __str__ = __repr__

