Say cheese
==========

Automatically take and/or purge ZFS snapshots.


Synopsis
--------

This code is intended to be run inside the crontab.

It should work both in python 2 and python 3.
(If it does not, or on other errors, please feel free to open an issue.)


Installation
^^^^^^^^^^^^

* As long this is still work in progress, clone this repository (as non root)
  into a trusted location.

* Then symlink both scripts (as root) into a folder inside of ``$PATH``.


Crontab
^^^^^^^

My crontab looks more or less like this::

    # say cheese
    3   0   *   *   *   /usr/local/bin/python /location/of/take_snapshots.py         auto_daily    >> /var/log/say_cheese.log 2>&1
    13  0   *   *   *   /usr/local/bin/python /location/of/purge_snapshots.py 1 d -p auto_daily    >> /var/log/say_cheese.log 2>&1

    5   0   *   *   0   /usr/local/bin/python /location/of/take_snapshots.py         auto_weekly   >> /var/log/say_cheese.log 2>&1
    15  0   *   *   0   /usr/local/bin/python /location/of/purge_snapshots.py 1 w -p auto_weekly   >> /var/log/say_cheese.log 2>&1

    7   0   1   *   *   /usr/local/bin/python /location/of/take_snapshots.py         auto_monthly  >> /var/log/say_cheese.log 2>&1
    17  0   1   *   *   /usr/local/bin/python /location/of/purge_snapshots.py 1 m -p auto_monthly  >> /var/log/say_cheese.log 2>&1

    9   0   1   1   *   /usr/local/bin/python /location/of/take_snapshots.py         auto_yearly   >> /var/log/say_cheese.log 2>&1
    19  0   1   1   *   /usr/local/bin/python /location/of/purge_snapshots.py 1 y -p auto_yearly   >> /var/log/say_cheese.log 2>&1



Scripts
-------


Take
^^^^

Take snapshots.

Please see ``./take_snapshots.py --help`` for usage::

    ./take_snapshots.py [-h] [-x] [-d] name [pools [pools ...]]


Purge
^^^^^

Purge snapshots.

Please see ``./purge_snapshots.py --help`` for usage::

    ./purge_snapshots.py  [-h] [-d] [-p PREFIX]
                          time
                          {S,sec,M,min,H,hour,d,day,w,week,m,month,y,year}


Appendix
--------

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
