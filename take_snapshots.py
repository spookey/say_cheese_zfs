#!/usr/bin/env python3

from logging import getLogger
from shlex import split
from subprocess import CalledProcessError, check_call, check_output
from sys import exit as _exit

from shared import message, start_parser, time_string

LOG = getLogger(__name__)


def pool_names():
    cmd = "zfs list -H -o name"
    try:
        proc = check_output(split(cmd), universal_newlines=True)
        return proc.splitlines()
    except (CalledProcessError, OSError) as ex:
        message([cmd, str(ex)], info=False)
        _exit(1)


def pool_snapshot(pool, name, dry=False):
    cmd = f'zfs snapshot "{pool}@{name}"'
    message(cmd, info=True)
    if dry:
        return True

    try:
        check_call(split(cmd))
        return True
    except (CalledProcessError, OSError) as ex:
        message([cmd, str(ex)], info=False)
    return False


def arguments():
    parser = start_parser("take_snapshots")

    parser.add_argument(
        "-x",
        "--exact",
        action="store_true",
        default=False,
        help="do not append current date onto name of snapshot",
    )
    parser.add_argument(
        "name",
        action="store",
        help=(
            "name of snapshot"
            " (will be suffixed with current date if not exact)"
        ),
    )
    parser.add_argument(
        "pools",
        action="store",
        nargs="*",
        help="name of pools",
    )

    args = parser.parse_args()
    stamp = time_string()

    pools = pool_names()
    for pool in args.pools:
        if pool not in pools:
            parser.error(f'pool "{pool}" does not exist')
    if not args.pools:
        args.pools = pools

    if not args.exact:
        args.name = f"{args.name}_{stamp}"

    message(
        (
            f'{__file__} at "{stamp}"'
            f' name: "{args.name}",'
            f' pools: "{", ".join(pools)}"'
        ),
        info=True,
    )

    return args


def main():
    args = arguments()
    res = []
    for pool in args.pools:
        res.append(pool_snapshot(pool, args.name, dry=args.dry))

    return all(res)


if __name__ == "__main__":
    _exit(not main())
