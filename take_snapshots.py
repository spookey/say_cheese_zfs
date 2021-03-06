#!/usr/bin/env python2

from argparse import ArgumentParser
from shlex import split
from subprocess import CalledProcessError, check_call, check_output
from sys import exit as _exit

from shared import message, time_string


def pool_names():
    cmd = 'zfs list -H -o name'
    try:
        proc = check_output(split(cmd), universal_newlines=True)
        return proc.splitlines()
    except (CalledProcessError, OSError) as ex:
        message([cmd, str(ex)], info=False, critical=True)


def pool_snapshot(pool, name, dry=False):
    cmd = 'zfs snapshot "{}@{}"'.format(pool, name)
    message(cmd, info=True, critical=False)
    if dry:
        return True

    try:
        check_call(split(cmd))
        return True
    except (CalledProcessError, OSError) as ex:
        message([cmd, str(ex)], info=False)
    return False


def arg_parser():
    parser = ArgumentParser(__file__, add_help=True)

    parser.add_argument(
        '-x', '--exact',
        action='store_true', default=False,
        help='do not append current date onto name of snapshot'
    )
    parser.add_argument(
        '-d', '--dry',
        action='store_true', default=False,
        help='dry run - just print what would be done'
    )

    parser.add_argument(
        'name',
        action='store',
        help='name of snapshot'
        '(will be suffixed with current date if not exact)'
    )
    parser.add_argument(
        'pools',
        action='store', nargs='*',
        help='name of pools'
    )

    return parser


def arguments():
    parser = arg_parser()
    args = parser.parse_args()

    pools = pool_names()
    for pool in args.pools:
        if pool not in pools:
            parser.error('pool "{}" does not exist'.format(pool))
    if not args.pools:
        args.pools = pools

    if not args.exact:
        args.name = '{}_{}'.format(args.name, time_string())

    message('{} at "{}" name: "{}", pools: "{}"'.format(
        __file__, time_string(),
        args.name, ', '.join(pools)
    ), info=True, critical=False)

    return args


def main():
    args = arguments()
    res = []
    for pool in args.pools:
        res.append(
            pool_snapshot(pool, args.name, dry=args.dry)
        )

    return all(res)


if __name__ == '__main__':
    _exit(not main())
