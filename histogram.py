"""
Streamable histogram tool
"""

import argparse
import math
import sys
import time
from collections import Counter

assert sys.version_info >= (3, 6, 0)


DESCRIPTION = """\
Generates a pretty histogram dynamically."""

WIDTH = 200
HEIGHT = 80

BLOCK = chr(9608)


def output(text):
    sys.stdout.write(text)
    sys.stdout.flush()


def histogram(counter, total):
    lines = ["\n"] * HEIGHT
    if not counter:
        lines.append("(No data)")
    else:
        # return vertical_histogram(counter)
        lines.extend(horizontal_histogram(counter))

    lines.append("-" * 20)
    lines.append("Histogram")
    lines.append(f"({total:,} data points)")

    return '\n'.join(lines)


def vertical_histogram(counter):
    pass
    # lines = []
    # for (k, v) in sorted(counter.items()):
    #     line = f""
    #     lines.append(line)


def horizontal_histogram(counter):
    lines = []

    max_allowed_key = 8
    max_key = len(max(counter.keys(), key=len))
    key_cutoff = min(max_allowed_key, max_key + 1)

    max_val = max(counter.values())
    val_factor = math.ceil(max_val / (WIDTH - key_cutoff - 1)) + 1

    if all(k.lstrip("-").isdecimal() for k in counter.keys()):
        sorted_keys = sorted(counter.keys(), key=lambda e: int(e))
    else:
        sorted_keys = sorted(counter.keys())

    for k in sorted_keys:
        v = counter[k]
        line = f"{str(k):.{key_cutoff}} {BLOCK * round(v / val_factor)}"
        lines.append(line)

    return lines


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("delay", type=float, default=0, nargs="?", help="Seconds of delay between output lines")
    return parser.parse_args()


def main_no_delay(source):
    counter = Counter()
    for (i, line) in enumerate(source):
        # datum = parse_line(line)
        datum = line.strip()
        counter[datum] += 1
        output(histogram(counter, i))


def main_delay(source, start, delay):
    counter = Counter()
    for (i, line) in enumerate(source):
        # datum = parse_line(line)
        datum = line.strip()
        counter[datum] += 1

        now = time.time()
        diff = now - start
        if diff >= delay:
            start = now
            output(histogram(counter, i))


def main():
    args = parse_args()
    delay = args.delay
    if (0 < delay < 0.001):
        raise RuntimeError("Non-0 delay must be at least 0.001")

    source = sys.stdin
    start = time.time()

    if not delay:
        main_no_delay(source)
    else:
        main_delay(source, start, delay)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
