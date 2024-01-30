from sys import version

if version.startswith("2"):
    from collections import Iterable
else:
    from collections.abc import Iterable


def is_iterable(data):
    return isinstance(data, Iterable)
