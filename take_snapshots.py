#!/usr/bin/env python3

from logging import getLogger
from sys import exit as _exit

from shared import (
    run_output,
    run_result,
    setup_logging,
    start_parser,
    time_string,
)

LOG = getLogger(__name__)


def pool_names():
    cmd = "zfs list -H -o name"
    return run_output(cmd, bailout=True)


def pool_snapshot(pool, name, dry=False):
    cmd = f'zfs snapshot "{pool}@{name}"'
    if dry:
        return True

    return run_result(cmd, bailout=False)


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
    setup_logging(args.level)

    pools = pool_names()
    for pool in args.pools:
        if pool not in pools:
            parser.error(f'pool "{pool}" does not exist')
    if not args.pools:
        args.pools = pools

    if not args.exact:
        stamp = time_string()
        args.name = f"{args.name}_{stamp}"

    LOG.info("name [%s] pools [%s]", args.name, args.pools)

    return args


def main():
    args = arguments()
    res = []
    for pool in args.pools:
        res.append(pool_snapshot(pool, args.name, dry=args.dry))

    return all(res)


if __name__ == "__main__":
    _exit(not main())
