"""
Streamable scatterplot tool
"""

import argparse
import json
import math
import sys
from collections import Counter

assert sys.version_info >= (3, 6, 0)


DESCRIPTION = """\
Generates a pretty scatterplot dynamically."""

WIDTH = 200
HEIGHT = 80


def output(text):
    sys.stdout.write(text)
    sys.stdout.flush()


def parse_line(text):
    try:
        d = json.loads(text)
        return (d["x"], d["y"])
    except Exception:
        return text.split(" ", 1)


def scatterplot(data):
    counter = Counter()
    # for (x, y) in data:
    #     counter[x] += y
    for v in data:
        counter[v] += 1

    lines = ["\n"] * HEIGHT
    if not counter:
        lines.append("(No data)")
    else:
        # return vertical_histogram(counter)
        lines.extend(horizontal_histogram(counter))

    lines.append("-" * 20)
    lines.append("Histogram")
    lines.append(f"({len(data):,} data points)")

    return '\n'.join(lines)


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
    # parser.add_argument("delay", type=float, default=0, help="Seconds of delay between output lines")
    return parser.parse_args()


def main():
    # args = parse_args()
    # delay = args.delay
    # if (delay < 0.001):
    #     raise RuntimeError("Delay must be at least 0.001")

    data = []
    for line in sys.stdin:
        # datum = parse_line(line)
        datum = line.strip()
        data.append(datum)
        output(histogram(data))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
