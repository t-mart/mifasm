from .run import run

MIFASM_WIDTH = 32
MIFASM_DEPTH = 2048

# map nicer radix names to mif radix names
# ours are also compatible with the bitstring package
radixes = {'hex':'HEX', 'bin':'BIN', 'int':'DEC', 'uint':'UNS'}
# im choosing not to support 'oct':'OCT'.
#   - unambiguous oct representation requires width to be a multiple of 3. 32
#     is not.
#   - who uses oct anyway?

