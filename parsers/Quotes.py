# -*- coding: UTF-8 -*-
"""Define the data structure of quotes."""
from collections import defaultdict
from utils import QuotePeriod
import time


class Quote(object):
    """Base class of Quotes"""

    def __init__(self,
                 exchange,
                 market,
                 equity,
                 symbol,
                 category,
                 status,
                 dt,
                 volume,
                 amount,
                 last,
                 open_price,
                 high,
                 low,
                 price,
                 close_price,
                 timestamp,
                 period=QuotePeriod.SECOND,
                 buy_bids=defaultdict(dict),
                 sell_bids=defaultdict(dict)
                 ):
        self._exchange = exchange
        self._market = market
        self._equity = equity
        self._symbol = symbol
        self._category = category
        self._status = status
        self._dt = dt
        self._volume = volume
        self._amount = amount
        self._last = last
        self._open = open_price
        self._high = high
        self._low = low
        self._price = price
        self._close = close_price
        self._timestamp = timestamp
        self._period = period
        self._buy_bids = buy_bids
        self._sell_bids = sell_bids

    @property
    def exchange(self):
        return self._exchange

    @property
    def market(self):
        return self._market

    @property
    def equity(self):
        return self._equity

    @property
    def symbol(self):
        return self._symbol

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, val):
        self._category = val

    @property
    def status(self):
        return self._status

    @property
    def dt(self):
        return self._dt

    @property
    def volume(self):
        return self._volume

    @property
    def amount(self):
        return self._amount

    @property
    def last(self):
        return self._last

    @property
    def open(self):
        return self._open

    @property
    def high(self):
        return self._high

    @property
    def low(self):
        return self._low

    @property
    def price(self):
        return self._price

    @property
    def close(self):
        return self._close

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def period(self):
        return self._period

    @property
    def buy_bids(self):
        return self._buy_bids

    @property
    def sell_bids(self):
        return self._sell_bids


class QuoteSnapshot(object):
    """A quote snapshot of a exchange including all it's market's equity"""

    def __init__(self,
                 exchange,
                 dt,
                 status,
                 seq,
                 volume=0,
                 amount=0,
                 timestamp=time.time(),
                 period=QuotePeriod.SECOND,
                 quotes=defaultdict(dict)
                 ):
        self._exchange = exchange
        self._dt = dt
        self._seq = seq
        self._status = status
        self._volume = volume
        self._amount = amount
        self._timestamp = timestamp
        self._period = period
        self._quotes = quotes

    @property
    def exchange(self):
        return self._exchange

    @property
    def dt(self):
        return self._dt

    @property
    def seq(self):
        return self._seq

    @property
    def status(self):
        return self._status

    @property
    def volume(self):
        return self._volume

    @property
    def amount(self):
        return self._amount

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def quotes(self):
        return self._quotes
