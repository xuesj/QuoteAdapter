# -*- coding: UTF-8 -*-

import datetime
from parsers.Quotes import Quote, QuoteSnapshot
from utils import Exchange, Market, EquityStatus, MarketStatus, EquityCategory, QuotePeriod
from collections import defaultdict
import time


def get_quote():
    exchange = Exchange.SH
    market = Market.A
    equity = '000001'
    symbol = 'AAPL'
    category = EquityCategory.STOCK
    status = EquityStatus.TRADE
    dt = datetime.datetime.now()
    volume = 10000
    amount = 100000.23
    last = 10.01
    open_price = 11.01
    high = 12.01
    low = 9.01
    price = 9.99
    close_price = 11.01
    timestamp = time.time()
    period = QuotePeriod.SECOND

    quote = Quote(exchange,
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
                  period
                  )
    return quote


def get_snapshot():
    exchange = Exchange.SH
    dt = datetime.datetime.now()
    status = MarketStatus.OPEN
    seq = 1
    volume = 1000
    amount = 10000.23
    timestamp = time.time()
    period = QuotePeriod.SECOND

    snapshot = QuoteSnapshot(exchange,
                             dt,
                             status,
                             seq,
                             volume,
                             amount,
                             timestamp,
                             period
                             )
    return snapshot


def test_quotes():

    quote = get_quote()
    assert quote.exchange == Exchange.SH
    assert quote.market == Market.A
    assert quote.equity == '000001'
    assert quote.symbol == 'AAPL'
    assert quote.category == EquityCategory.STOCK
    assert quote.status == EquityStatus.TRADE
    assert quote.dt <= datetime.datetime.now()
    assert quote.period == 3
    assert quote.last == 10.01
    assert quote.open == 11.01
    assert quote.high == 12.01
    assert quote.low == 9.01
    assert quote.close == 11.01

    quote.category = EquityCategory.INDEX
    assert quote.category == EquityCategory.INDEX


def test_quote_snapshot():
    snapshot = get_snapshot()

    assert snapshot

    assert snapshot.exchange == Exchange.SH
    assert snapshot.dt <= datetime.datetime.now()
    assert snapshot.status == MarketStatus.OPEN
    assert snapshot.volume == 1000
    assert snapshot.amount == 10000.23
