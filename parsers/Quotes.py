# -*- coding: UTF-8 -*-
"""Define the data structure of quotes."""


class Quotes(object):
    """Base class of Quotes"""

    def __init__(self,
                 exchange_id,
                 market_id,
                 equity_id,
                 equity_symbol,
                 equity_status,
                 quote_date,
                 quote_time,
                 quote_period,
                 last_close,
                 open_price,
                 high_price,
                 low_price,
                 close_price
                 ):
        self._exchange_id = exchange_id
        self._market_id = market_id
        self._equity_id = equity_id
        self._equity_symbol = equity_symbol
        self._equity_status = equity_status
        self._quote_date = quote_date
        self._quote_time = quote_time
        self._quote_period = quote_period
        self._last_close = last_close
        self._open_price = open_price
        self._high_price = high_price
        self._low_price = low_price
        self._close_price = close_price

    @property
    def exchange_id(self):
        return self._exchange_id

    @exchange_id.setter
    def exchange_id(self, val):
        self._exchange_id = val

    @property
    def market_id(self):
        return self._market_id

    @market_id.setter
    def market_id(self, val):
        self._market_id = val

    @property
    def equity_id(self):
        return self._equity_id

    @equity_id.setter
    def equity_id(self, val):
        self._equity_id = val

    @property
    def equity_symbol(self):
        return self._equity_symbol

    @equity_symbol.setter
    def equity_symbol(self, val):
        self._equity_symbol = val

    @property
    def equity_status(self):
        return self._equity_status

    @equity_status.setter
    def equity_status(self, val):
        self._equity_status = val

    @property
    def quote_date(self):
        return self._quote_date

    @quote_date.setter
    def quote_date(self, val):
        self._quote_date = val

    @property
    def quote_time(self):
        return self._quote_time

    @quote_time.setter
    def quote_time(self, val):
        self._quote_time = val

    @property
    def quote_period(self):
        return self._quote_period

    @quote_period.setter
    def quote_period(self, val):
        self._quote_period = val

    @property
    def last_close(self):
        return self._last_close

    @last_close.setter
    def last_close(self, val):
        self._last_close = val

    @property
    def open_price(self):
        return self._open_price

    @open_price.setter
    def open_price(self, val):
        self._open_price = val

    @property
    def high_price(self):
        return self._high_price

    @high_price.setter
    def high_price(self, val):
        self._high_price = val

    @property
    def low_price(self):
        return self._low_price

    @low_price.setter
    def low_price(self, val):
        self._low_price = val

    @property
    def close_price(self):
        return self._close_price

    @close_price.setter
    def close_price(self, val):
        self._close_price = val


class QuoteSnapshot(object):
    """A quote snapshot of a exchange including all it's market's equity"""

    def __init__(self,
                 exchange_id,
                 quote_date,
                 quote_time,
                 exchange_status,
                 num_equity,
                 quotes):
        self._exchange_id = exchange_id
        self._quote_date = quote_date
        self._quote_time = quote_time
        self._exchange_status = exchange_status
        self._num_equity = num_equity
        self._quotes = quotes

    @property
    def exchange_id(self):
        return self._exchange_id

    @exchange_id.setter
    def exchange_id(self, val):
        self._exchange_id = val

    @property
    def quote_date(self):
        return self._quote_date

    @quote_date.setter
    def quote_date(self, val):
        self._quote_date = val

    @property
    def quote_time(self):
        return self._quote_time

    @quote_time.setter
    def quote_time(self, val):
        self._quote_time = val

    @property
    def exchange_status(self):
        return self._exchange_status

    @exchange_status.setter
    def exchange_status(self, val):
        self._exchange_status = val

    @property
    def num_equity(self):
        return self._num_equity

    @num_equity.setter
    def num_equity(self, val):
        self._num_equity = val

    @property
    def quotes(self):
        return self._quotes

    @quotes.setter
    def quotes(self, val):
        self._quotes = val
