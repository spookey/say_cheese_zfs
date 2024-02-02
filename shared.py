from argparse import ArgumentParser
from datetime import datetime
from logging import (
    DEBUG,
    ERROR,
    INFO,
    WARNING,
    Formatter,
    StreamHandler,
    getLogger,
)
from shlex import split
from subprocess import CalledProcessError, check_call, check_output
from sys import exit as _exit

LOG = getLogger(__name__)
SNAP_FORMAT = "%Y-%m-%d_%H-%M-%S"
LOG_FORMATTER = Formatter(
    """
-- %(asctime)s\t%(levelname)s\t[%(module)s:%(lineno)s] --
%(message)s
    """.strip()
)
LOG_LEVEL_DEFAULT = "info"
LOG_LEVELS = {
    "debug": DEBUG,
    "error": ERROR,
    LOG_LEVEL_DEFAULT: INFO,
    "warn": WARNING,
    "warning": WARNING,
}


def start_parser(name):
    parser = ArgumentParser(name, add_help=True)

    parser.add_argument(
        "-d",
        "--dry",
        action="store_true",
        default=False,
        help="dry run - just print what would be done",
    )
    parser.add_argument(
        "-l",
        "--level",
        choices=LOG_LEVELS.keys(),
        default=LOG_LEVEL_DEFAULT,
        help="change logging level (default: %(default)s)",
    )

    return parser


def setup_logging(level_name):
    handler = StreamHandler(stream=None)
    handler.setFormatter(LOG_FORMATTER)
    level = LOG_LEVELS.get(level_name, INFO)

    logger = getLogger()
    logger.addHandler(handler)
    logger.setLevel(level)


def run_output(cmd, *, bailout=True):
    LOG.debug("running [%s]", cmd)
    try:
        proc = check_output(split(cmd), text=True)
        return proc.splitlines()
    except (CalledProcessError, OSError) as ex:
        LOG.error("command failed: [%s] - %s", cmd, ex)
        if bailout:
            _exit(1)
    return []


def run_result(cmd, *, bailout=True):
    LOG.debug("running [%s]", cmd)
    try:
        check_call(split(cmd))
        return True
    except (CalledProcessError, OSError) as ex:
        LOG.error("command failed: [%s] - %s", cmd, ex)
        if bailout:
            _exit(1)
    return False


def time_string(stamp=None):
    if stamp is None:
        stamp = datetime.utcnow()
    return stamp.strftime(SNAP_FORMAT)


def time_parse(number=0):
    return datetime.utcfromtimestamp(int(number))


def time_span(stamp=None):
    if stamp is None:
        stamp = datetime.utcnow()
    return int((stamp - time_parse(0)).total_seconds())
