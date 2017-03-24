# -*- coding: UTF-8 -*-
"""Constants """


class Protocol(object):
    __slots__ = ['value']
    TCP = 0
    FILE = 1
    SQLS = 2


class Port(object):
    __slots__ = ['value']


class Exchange(object):
    SH = 0
    SZ = 1


class ExChangeStatus(object):
    OPEN = 0        # open
    CLOSE = 1       # close
    PRE_OPEN_BIDDING = 2    # pre_open bidding
    NOON_INTERVAL = 3       # noon interval
