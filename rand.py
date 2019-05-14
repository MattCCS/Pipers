"""
Tool to yield random numbers in a range
"""

import argparse
import random
import sys

assert sys.version_info >= (3, 6, 0)


DESCRIPTION = """\
Generates random numbers in the specified range.

Default mode is floats in [0,1)."""


def output(text):
    sys.stdout.write(text)
    sys.stdout.flush()


def stream(iterable):
    for n in iterable:
        output(str(n) + "\n")


def ints(low, high, count):
    total = 0
    low = int(low)
    high = int(high) - 1
    while total != count:
        n = random.randint(low, high)
        yield n
        total += 1


def floats(low, high, count):
    total = 0
    span = high - low
    while total != count:
        n = random.random() * span + low
        yield n
        total += 1


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("count", type=int, default=-1, nargs="?", help="How many numbers to yield. Default -1 (infinite).")
    parser.add_argument("--range", type=float, default=(0, 1), nargs=2, metavar=("from", "to"), help="Low/high bounds for range. [from, to). Default [0, 1).")
    parser.add_argument("--type", default="float", choices=["int", "float"], help="Type of number to yield. Default float.")
    return parser.parse_args()


def main():
    args = parse_args()

    count = args.count
    (low, high) = args.range
    typ = args.type

    if (high <= low):
        raise RuntimeError("Low must be less than high")

    if (typ == "int"):
        stream(ints(low, high, count))
    elif (typ == "float"):
        stream(floats(low, high, count))
    else:
        raise RuntimeError("How did you get here??")


if __name__ == '__main__':
    main()
