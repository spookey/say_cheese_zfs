from datetime import datetime
from sys import stderr, stdout
from sys import exit as _exit

from compat import is_iterable

SNAP_FORMAT = '%Y-%m-%d-%H-%M-%S'


def message(entries, info=True, critical=False):
    pipe, pre = (stdout, 'info') if info else (stderr, 'error')

    if isinstance(entries, str):
        entries = entries.splitlines()
    if not is_iterable(entries):
        entries = [entries]

    for entry in entries:
        pipe.write('{}: {}\n'.format(pre, entry))
    pipe.flush()
    if critical:
        _exit(1)


def time_stamp():
    return datetime.utcnow().strftime(SNAP_FORMAT)
