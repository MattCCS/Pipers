"""
Tool to slow piped input with an arbitrary delay
"""

import argparse
import sched
import sys
import time

assert sys.version_info >= (3, 6, 0)


DESCRIPTION = """\
Bottlenecks a piped process to output X bytes every N seconds (>= 0.001).

Guarantees the delay to be at least N seconds."""


def output(bytez):
    sys.stdout.buffer.write(bytez)
    sys.stdout.buffer.flush()


def slow(source, delay, chunksize):
    start = time.time()
    scheduler = sched.scheduler(time.time, time.sleep)
    i = 0
    while True:
        data = source.buffer.read(chunksize)
        if not data:
            break
        time_abs = start + (i * delay)
        scheduler.enterabs(time_abs, 0, output, argument=(data,))
        scheduler.run()
        i += 1


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("delay", type=float, default=0, help="Seconds of delay between output writes")
    parser.add_argument("chunksize", type=int, default=1, help="Maximum output write size in bytes")
    return parser.parse_args()


def main():
    args = parse_args()
    delay = args.delay
    chunksize = args.chunksize
    if (delay < 0.001):
        raise RuntimeError("Delay must be at least 0.001")
    if (chunksize < 1):
        raise RuntimeError("Chunksize must be at least 1")

    source = sys.stdin

    slow(source, delay, chunksize)


if __name__ == '__main__':
    main()
