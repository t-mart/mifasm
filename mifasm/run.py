import argparse
import sys
import os

from .assembler import Assembler

def run():
    parser = argparse.ArgumentParser(description='Assemble cs3220 assembly into a quartus mif.')

    parser.add_argument('input', help='path to assembly file')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-o','--output',
            help='path to output (changes extension of input to .mif by default)')
    group.add_argument('--stdout', action='store_true', help="output to stdout")

    radixes = Assembler.radix_names
    parser.add_argument('--addr-radix', choices=radixes, default='hex',
            help='radix of addresses in output')
    parser.add_argument('--data-radix', choices=radixes, default='hex',
            help='radix of data in output')

    parser.add_argument('-w', '--width', default=32, type=int,
            help='size of word in bits')
    parser.add_argument('-d', '--depth', default=2048, type=int,
            help='number of words in memory')

    parser.add_argument('-C', '--no-comment', action='store_false',
            dest='comments', help='generate output without debug comments')

    args = parser.parse_args()

    if args.stdout:
        # --stdout specified
        args.output = sys.stdout
    else:
        if not args.output:
            # no --stdout, but also no -o/--output specified
            output_filename = filename_with_mif_ext(args.input)

        if args.input == output_filename:
            parser.error("output path not allowed to be same as input path")

        args.output = open(output_filename, 'w')

    args.input = open(args.input, 'r')

    print vars(args)

    assembler = Assembler(**vars(args))

    print Assembler._radix_function('hex', 4)(9)

def filename_with_mif_ext(path):
    mif_ext = '.mif'
    return os.path.splitext(path)[0] + mif_ext

if __name__ == '__main__':
    run()
