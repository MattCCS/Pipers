"""
Tool to yield Gaussian random numbers in a range
"""

import argparse
import random
import sys

assert sys.version_info >= (3, 6, 0)


DESCRIPTION = """\
Generates Gaussian random numbers in the specified range.

Default mode is floats in [0,1)."""


def output(text):
    sys.stdout.write(text)
    sys.stdout.flush()


def stream(iterable):
    for n in iterable:
        output(str(n) + "\n")


def ints(mu, sigma, count):
    for n in floats(mu, sigma, count):
        yield round(n)


def floats(mu, sigma, count):
    total = 0
    while total != count:
        n = random.gauss(mu, sigma)
        yield n
        total += 1


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("count", type=int, default=-1, nargs="?", help="How many numbers to yield. Deafult -1 (infinite).")
    parser.add_argument("--mu", type=float, default=0, nargs="?", help="Mu value (mean). Deafult 0.")
    parser.add_argument("--sigma", type=float, default=1, nargs="?", help="Sigma value (standard deviation). Default 1.")
    parser.add_argument("--type", default="float", choices=["int", "float"], help="Type of number to yield. Default float.")
    return parser.parse_args()


def main():
    args = parse_args()

    count = args.count
    mu = args.mu
    sigma = args.sigma
    typ = args.type

    if (typ == "int"):
        stream(ints(mu, sigma, count))
    elif (typ == "float"):
        stream(floats(mu, sigma, count))
    else:
        raise RuntimeError("How did you get here??")


if __name__ == '__main__':
    main()
