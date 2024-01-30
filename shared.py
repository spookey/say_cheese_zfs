from datetime import datetime
from sys import exit as _exit
from sys import stderr, stdout

from compat import is_iterable

SNAP_FORMAT = "%Y-%m-%d_%H-%M-%S"


def message(entries, info=True, critical=False):
    pipe, pre = (stdout, "info") if info else (stderr, "error")

    if isinstance(entries, str):
        entries = entries.splitlines()
    if not is_iterable(entries):
        entries = [entries]

    for entry in entries:
        pipe.write("{}: {}\n".format(pre, entry))
    pipe.flush()
    if critical:
        _exit(1)


def time_string(stamp=None):
    if stamp is None:
        stamp = datetime.utcnow()
    return stamp.strftime(SNAP_FORMAT)


def time_parse(number=0):
    return datetime.utcfromtimestamp(int(number))


def time_span(stamp=None):
    if stamp is None:
        stamp = datetime.utcnow()
    return int((stamp - time_parse()).total_seconds())
