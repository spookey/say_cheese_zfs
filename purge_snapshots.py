#!/usr/bin/env python3

from argparse import ArgumentParser
from shlex import split
from subprocess import CalledProcessError, check_call, check_output
from sys import exit as _exit

from shared import message, time_parse, time_span, time_string

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
        if key == sml or key == lng:
            return val * num
    return 0


def snapshot_data():
    def _get():
        cmd = "zfs list -H -p -o creation,name -t snapshot"
        try:
            proc = check_output(split(cmd), universal_newlines=True)
            return proc.splitlines()
        except (CalledProcessError, OSError) as ex:
            message([cmd, str(ex)], info=False, critical=True)

    result = []
    for snap in _get():
        stamp, full_name = snap.split()
        _, prefix = full_name.split("@")
        result.append((int(stamp), full_name, prefix))
    return result


def snapshot_destroy(name, dry=False):
    cmd = f'zfs destroy "{name}"'
    message(cmd, info=True, critical=False)
    if dry:
        return True

    try:
        check_call(split(cmd))
        return True
    except (CalledProcessError, OSError) as ex:
        message([cmd, str(ex)], info=False, critical=True)
    return False


def arguments():
    parser = ArgumentParser(__file__, add_help=True)

    def positive(value):
        try:
            value = int(value)
            if value <= 0:
                raise ValueError()
        except ValueError:
            parser.error(f'"{value}" should be a positive number')
        return value

    parser.add_argument(
        "-d",
        "--dry",
        action="store_true",
        default=False,
        help="dry run - just print what would be done",
    )
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
        choices=[fl for at in ((un[1], un[2]) for un in UNITS) for fl in at],
        help="textual unit value",
    )

    args = parser.parse_args()
    message(
        (
            f'{__file__} at "{time_string()}"'
            f' time: "{args.time}",'
            f' unit: "{args.unit}",'
            f' prefix: "{args.prefix}"'
        ),
        info=True,
        critical=False,
    )

    return args


def consider(s_name, a_prefix, s_prefix, a_time, s_time):
    if a_prefix is not None and not s_prefix.startswith(a_prefix):
        message(
            (
                f'"{a_prefix}" does not match on "{s_prefix}"'
                f' - skipping "{s_name}"'
            ),
            info=True,
            critical=False,
        )
        return False

    if s_time > a_time:
        a_span = time_string(time_parse(a_time))
        s_span = time_string(time_parse(s_time))
        message(
            (
                f'"{a_span}" is smaller than "{s_span}"'
                f'- skipping "{s_name}"'
            ),
            info=True,
            critical=False,
        )
        return False

    return True


def main():
    args = arguments()
    span = time_span() - unit(args.time, args.unit)
    res = []

    for stamp, name, prefix in snapshot_data():
        if consider(name, args.prefix, prefix, span, stamp):
            res.append(snapshot_destroy(name, dry=args.dry))

    return all(res)


if __name__ == "__main__":
    _exit(not main())
