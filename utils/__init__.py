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


class Market(object):
    A = 0
    B = 1
    ALL = 3


class MarketStatus(object):
    OPEN = 0
    CLOSE = 1
    PRE_OPEN = 2
    NOON = 3


class EquityStatus(object):
    TRADE = 0
    SUSPEND = 1
    DELIST = 2


class EquityCategory(object):
    STOCK = 0
    BOND = 1
    FUND = 2
    INDEX = 3


class QuotePeriod(object):
    SECOND = 3
    MINUTE = 60
    HOUR = 3600
    DAY = 14400
