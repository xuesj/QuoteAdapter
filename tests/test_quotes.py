# -*- coding: UTF-8 -*-

import datetime
import time

from parsers.Quotes import Quotes, QuoteSnapshot


def test_quotes():
    exchange_id = 'SH'
    market_id = 'A'
    equity_id = '000001'
    equity_symbol = '001'
    equity_status = '1'
    quote_date = datetime.date.today()
    quote_time = time.time()
    quote_period = 1
    last_close = 10.01
    open_price = 11.01
    high_price = 12.01
    low_price = 9.01
    close_price = 11.01

    a_quote = Quotes(exchange_id,
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
                     close_price)

    assert a_quote.exchange_id == 'SH'
    assert a_quote.market_id == 'A'
    assert a_quote.equity_id == '000001'
    assert a_quote.equity_symbol == '001'
    assert a_quote.equity_status == '1'
    assert a_quote.quote_date == datetime.date.today()
    assert a_quote.quote_time == quote_time
    assert a_quote.quote_period == 1
    assert a_quote.last_close == 10.01
    assert a_quote.open_price == 11.01
    assert a_quote.high_price == 12.01
    assert a_quote.low_price == 9.01
    assert a_quote.close_price == 11.01

    a_quote.exchange_id = 'SZ'
    a_quote.market_id = 'B'
    a_quote.equity_id = '000002'
    a_quote.equity_symbol = '002'
    a_quote.equity_status = '2'
    a_quote.quote_date = datetime.date.today()
    a_quote.quote_time = time.time()
    a_quote.quote_period = 2
    a_quote.last_close = 10.02
    a_quote.open_price = 11.02
    a_quote.high_price = 12.02
    a_quote.low_price = 9.02
    a_quote.close_price = 11.02

    assert a_quote.exchange_id == 'SZ'
    assert a_quote.market_id == 'B'
    assert a_quote.equity_id == '000002'
    assert a_quote.equity_symbol == '002'
    assert a_quote.equity_status == '2'
    assert a_quote.quote_date == datetime.date.today()
    assert a_quote.quote_time <= time.time()
    assert a_quote.quote_period == 2
    assert a_quote.last_close == 10.02
    assert a_quote.open_price == 11.02
    assert a_quote.high_price == 12.02
    assert a_quote.low_price == 9.02
    assert a_quote.close_price == 11.02


def test_quote_snapshot():
    exchange_id = 'SH_EX'
    quote_date = datetime.date.today()
    quote_time = time.time()
    exchange_status = '0'
    num_equity = 1000
    quotes = {}

    market_id = 'A'
    equity_id = '000001'
    equity_symbol = '001'
    equity_status = '1'
    # quote_date = date.today()
    # quote_time = time.time()
    quote_period = 1
    last_close = 10.01
    open_price = 11.01
    high_price = 12.01
    low_price = 9.01
    close_price = 11.01

    a_quote = Quotes(exchange_id,
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
                     close_price)

    quotes[equity_id] = a_quote

    quote_snapshot = QuoteSnapshot(exchange_id,
                                   quote_date,
                                   quote_time,
                                   exchange_status,
                                   num_equity,
                                   quotes)
    assert quote_snapshot
    assert quote_snapshot.quotes[equity_id].close_price == 11.01

    assert quote_snapshot.exchange_id == exchange_id
    assert quote_snapshot.quote_date == quote_date
    assert quote_snapshot.quote_time == quote_time
    assert quote_snapshot.exchange_status == exchange_status
    assert quote_snapshot.num_equity == num_equity
    assert quote_snapshot.quotes == quotes

    quote_snapshot.exchange_id = exchange_id
    quote_snapshot.quote_date = quote_date
    quote_snapshot.quote_time = quote_time
    quote_snapshot.exchange_status = exchange_status
    quote_snapshot.num_equity = num_equity
    quote_snapshot.quotes = quotes

    assert quote_snapshot.exchange_id == exchange_id
    assert quote_snapshot.quote_date == quote_date
    assert quote_snapshot.quote_time == quote_time
    assert quote_snapshot.exchange_status == exchange_status
    assert quote_snapshot.num_equity == num_equity
    assert quote_snapshot.quotes == quotes

