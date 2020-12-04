"""
Tool to slow piped input with an arbitrary delay
"""

import argparse
import sched
import sys
import time

assert sys.version_info >= (3, 6, 0)


DESCRIPTION = """\
Bottlenecks a piped process to output a line every N seconds (>= 0.001).

Guarantees the delay to be at least N seconds."""


def output(text):
    sys.stdout.write(text)
    sys.stdout.flush()


def slow(source, start, delay):
    scheduler = sched.scheduler(time.time, time.sleep)
    for (i, line) in enumerate(source):
        time_abs = start + (i * delay)
        scheduler.enterabs(time_abs, 0, output, argument=(line,))
        scheduler.run()


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("delay", type=float, default=0, help="Seconds of delay between output lines")
    return parser.parse_args()


def main():
    args = parse_args()
    delay = args.delay
    if (delay < 0.001):
        raise RuntimeError("Delay must be at least 0.001")

    source = sys.stdin
    start = time.time()

    slow(source, start, delay)


if __name__ == '__main__':
    main()
