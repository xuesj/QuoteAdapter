# -*- coding: UTF-8 -*-
"""Define the data structure of quotes."""


class Quotes(object):
    """Base class of Quotes"""

    def __init__(self,
                 exchange,
                 market_id,
                 equity_id,
                 equity_symbol,
                 equity_status,
                 quote_datetime,
                 quote_period,
                 last_close,
                 open_price,
                 high_price,
                 low_price,
                 close_price
                 ):
        self._exchange = exchange
        self._market_id = market_id
        self._equity_id = equity_id
        self._equity_symbol = equity_symbol
        self._equity_status = equity_status
        self._quote_date = quote_datetime
        self._quote_period = quote_period
        self._last_close = last_close
        self._open_price = open_price
        self._high_price = high_price
        self._low_price = low_price
        self._close_price = close_price

    @property
    def exchange(self):
        return self._exchange

    @exchange.setter
    def exchange(self, val):
        self._exchange = val

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
    def quote_datetime(self):
        return self._quote_date

    @quote_datetime.setter
    def quote_datetime(self, val):
        self._quote_date = val

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
                 exchange,
                 quote_datetime,
                 exchange_status,
                 num_equity,
                 quotes):
        self._exchange = exchange
        self._quote_date = quote_datetime
        self._exchange_status = exchange_status
        self._num_equity = num_equity
        self._quotes = quotes

    @property
    def exchange(self):
        return self._exchange

    @exchange.setter
    def exchange(self, val):
        self._exchange = val

    @property
    def quote_datetime(self):
        return self._quote_date

    @quote_datetime.setter
    def quote_date(self, val):
        self._quote_date = val

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
