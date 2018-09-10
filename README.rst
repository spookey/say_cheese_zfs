Say cheese
==========

Automatically take and/or purge ZFS snapshots.

Synopsis
--------

Beware: *work in progress*

This code is intended to be run inside the crontab.

It should work both in python 2 and python 3.
(If it does not, or on other errors, please feel free to open an issue.)

Installation
^^^^^^^^^^^^

* As long this is still work in progress, clone this repository (as non root)
  into a trusted location.

* Then symlink both scripts (as root) into a folder inside of ``$PATH``.


Take
~~~~

Take snapshots.

Please see ``./take_snapshots.py --help`` for usage::

    ./take_snapshots.py [-h] [-x] [-d] [-s] name [pools [pools ...]]


Purge
~~~~~

Purge snapshots.

tbd;


Appendix
^^^^^^^^

This project is loosely related to
`zfs-snapshot-all <ztake_>`_
and
`zfs-prune-snapshots <zprune_>`_
by bahamas10.

I just wanted to solve the same problems, but in a little different way.

The changes are different enough that forking was not really an option.

Thanks for this original awesome work - it helepd a lot!


.. _ztake: https://github.com/bahamas10/zfs-snapshot-all
.. _zprune: https://github.com/bahamas10/zfs-prune-snapshots
