import argparse

from parser import LunaParser
from util import file_io as fio


def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("input", type=str, help='input .fa file to compile')
    arg_parser.add_argument("-o", "--output", type=str, default="", help="output .ja file")

    args = arg_parser.parse_args()
    if not args.output:
        if ".fa" not in args.input:
            args.output = args.input + ".ja"
        else:
            args.output = args.input.replace(".fa", ".ja")
    return args


def main():
    args = parse_args()
    parser = LunaParser()
    try:
        code = fio.read_file(args.input)
        program = parser.parse(code)
        if program:
            fio.write_json(args.output, program.to_json())
            print("Output is written to {0}".format(args.output))
    except Exception as e:
        print("Error: {0}".format(e))


if __name__ == "__main__":
    main()
