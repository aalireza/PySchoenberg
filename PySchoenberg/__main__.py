from PySchoenberg.core import Row, Matrix, Sheet
from PySchoenberg.atonalizer import (
    AtonalStreamer, random_serial_row_deriving_closure, atonalize
)
import argparse
import os


def input_path_verification(path):
    if not os.path.exists(path):
        return ValueError("input file does not exist")
    if not os.access(os.path.abspath, os.R_OK):
        return ValueError("input file is not readable")
    return True


def output_path_verification(path):
    if not os.access(os.path.abspath(path), os.W_OK):
        return ValueError("The path to the output file is not writable")
    return True


def row_maker(row):
    assert Row.Verification.length(row)
    try:
        if Row.Verification.numerical(row):
            return Row.parse_numerical(row)
    except:
        pass

    try:
        if Row.Verification.pretty(row):
            return Row.parse_pretty_notes(row)
    except:
        pass

    raise Exception


def argument_handler():
    parser = argparse.AgumentParser()
    parser.add_argument("-f", "--initial_file", required=True, type=str)
    row_group = parser.add_mutually_exclusive_group(required=True)
    row_group.add_argument("-r", "--row", nargs=12, type=str)
    row_group.add_argument("-R", "--random_row", action='store_true')
    parser.add_argument("-o", "--output", required=True, type=str)
    args = parser.parse_args()

    if (
            input_path_verification(args.initial_file) and
            output_path_verification(args.output_file)
    ):
        row = (Row.random() if args.random_row else row_maker(args.row))

    return args.initial_file, row, args.output_file


def Main():
    input_file, row, output_file = argument_handler()
    sheet = Sheet(input_file)
    matrix = Matrix(row)
    streamer = AtonalStreamer(random_serial_row_deriving_closure(matrix))
    atonalize(sheet, streamer)
    sheet.export(output_file)


if __name__ == '__main__':
    Main()
