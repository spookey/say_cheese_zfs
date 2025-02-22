#!/usr/bin/env python3

from logging import getLogger
from sys import exit as _exit

from shared import (
    run_output,
    run_result,
    setup_logging,
    start_parser,
    time_parse,
    time_span,
    time_string,
)

LOG = getLogger(__name__)
UNITS = (
    (1, "S", "sec"),
    (60, "M", "min"),
    (60 * 60, "H", "hour"),
    (60 * 60 * 24, "d", "day"),
    (60 * 60 * 24 * 7, "w", "week"),
    (60 * 60 * 24 * 30, "m", "month"),
    (60 * 60 * 24 * 365, "y", "year"),
)


def unit(num, key):
    for val, sml, lng in UNITS:
        if key in (sml, lng):
            return val * num
    return 0


def snapshot_data():
    cmd = "zfs list -H -p -o creation,name -t snapshot"

    result = []
    for snap in run_output(cmd, bailout=True):
        stamp, full_name = snap.split()
        _, suffix = full_name.split("@")
        result.append((int(stamp), full_name, suffix))
    return result


def snapshot_destroy(name, dry=False):
    cmd = f'zfs destroy "{name}"'
    if dry:
        return True

    LOG.info("destroy snapshot [%s]", name)
    return run_result(cmd, bailout=True)


def arguments():
    parser = start_parser("purge_snapshots")

    def positive(value):
        try:
            value = int(value)
            if value <= 0:
                raise ValueError()
        except ValueError:
            parser.error(f"[{value}] should be a positive number")
        return value

    def units():
        for _, sml, lng in UNITS:
            yield sml
            yield lng

    parser.add_argument(
        "-p",
        "--prefix",
        action="store",
        help="snapshot prefix string to match",
    )
    parser.add_argument(
        "time",
        type=positive,
        action="store",
        help="numeric time value",
    )
    parser.add_argument(
        "unit",
        action="store",
        choices=list(units()),
        help="textual unit value",
    )

    args = parser.parse_args()
    setup_logging(args.level)

    LOG.info(
        "time [%s] unit [%s] prefix [%s]",
        args.time,
        args.unit,
        args.prefix,
    )

    return args


def consider(full_name, prefix, suffix, span_time, snap_time):
    if prefix is not None and not suffix.startswith(prefix):
        LOG.debug(
            "[%s] does not match on [%s] - skipping [%s]",
            prefix,
            suffix,
            full_name,
        )
        return False

    if snap_time > span_time:
        span_stamp = time_string(time_parse(span_time))
        snap_stamp = time_string(time_parse(snap_time))
        LOG.debug(
            "[%s] is smaller than [%s] - skipping [%s]",
            span_stamp,
            snap_stamp,
            full_name,
        )
        return False

    return True


def main():
    args = arguments()
    span_time = time_span() - unit(args.time, args.unit)
    result = []

    for snap_time, full_name, suffix in snapshot_data():
        if consider(full_name, args.prefix, suffix, span_time, snap_time):
            result.append(snapshot_destroy(full_name, dry=args.dry))

    return all(result)


if __name__ == "__main__":
    _exit(not main())
