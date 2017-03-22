# -*- coding: UTF-8 -*-

from receivers.quoteReceiver import ExchangeQuote, TransCalendar, TransPeriod
from receivers.quoteReceiver import ExchangeProtocol, ExchangePort
import datetime
from multiprocessing import Queue


def test_trans_period():
    t1 = datetime.time(hour=9, minute=30)
    t2 = datetime.time(hour=11, minute=30)

    tc1 = TransPeriod(t1, t2)
    assert tc1
    assert tc1.time_delta() == datetime.timedelta(hours=2)

    try:
        TransPeriod(t2, t1)
    except ValueError as e:
        assert e


def test_exchange_protocol():
    protocol = ExchangeProtocol()
    protocol.value = ExchangeProtocol.FILE
    assert protocol.value == 1
    protocol.value = ExchangeProtocol.TCP
    assert protocol.value == 0
    try:
        protocol.name = 'james'
    except AttributeError as e:
        assert e


def test_exchange_port():
    exchange_port = ExchangePort()
    exchange_port.value = 'james'
    assert exchange_port.value == 'james'
    try:
        exchange_port.name = 12345
    except AttributeError as e:
        assert e


def test_trans_calendar():
    t1 = datetime.time(hour=9, minute=30)
    t2 = datetime.time(hour=11, minute=30)
    t3 = datetime.time(hour=13, minute=30)
    t4 = datetime.time(hour=15, minute=30)

    periods = [TransPeriod(t1, t2), TransPeriod(t3, t4)]
    trans_calendar = TransCalendar(periods)
    now = datetime.datetime.now()
    assert trans_calendar
    assert trans_calendar.is_trans_day(now)
    # assert trans_calendar.is_trans_time(now)
    assert trans_calendar.next_trans_day(now) == now

    off_dt1 = datetime.datetime(2017, 3, 21, 13, 29)
    off_dt2 = datetime.datetime(2017, 3, 21, 15, 31)
    assert not trans_calendar.is_trans_time(off_dt1)
    assert not trans_calendar.is_trans_time(off_dt2)

    dt3 = datetime.datetime(2017, 3, 19, 13, 29)
    dt4 = datetime.datetime(2017, 5, 31, 15, 31)
    assert not trans_calendar.is_trans_day(dt3)
    assert trans_calendar.is_trans_day(dt4)

    assert datetime.date(2017, 1, 1) in trans_calendar._holidays[2017]
    assert datetime.date(2017, 10, 1) in trans_calendar._holidays[2017]
    assert datetime.date(2017, 10, 8) in trans_calendar._holidays[2017]
    assert datetime.date(2017, 4, 4) in trans_calendar._holidays[2017]
    assert datetime.date(2017, 1, 27) in trans_calendar._holidays[2017]


def test_exchange_quote():
    protocol = ExchangeProtocol.FILE
    port = '../datas/mktdt00.txt'
    timeout = 3
    interval = 6

    t1 = datetime.time(hour=9, minute=30)
    t2 = datetime.time(hour=11, minute=30)
    t3 = datetime.time(hour=13, minute=30)
    t4 = datetime.time(hour=15, minute=30)

    periods = [TransPeriod(t1, t2), TransPeriod(t3, t4)]
    trans_calendar = TransCalendar(periods)
    queue = Queue(10)

    exchange_quote = ExchangeQuote(protocol=protocol, port=port, timeout=timeout,
                                   interval=interval, trans_calendar=trans_calendar,
                                   queue=queue)
    assert exchange_quote
    # assert exchange_quote.is_open()
    assert not exchange_quote.is_close()

    exchange_quote.run()

    i = 0
    while exchange_quote.is_open():
        quote = exchange_quote.read_quote()
        if quote is not None:
            print quote
            assert quote == 'Hello: ' + str(i)
            i += 1
            if i >= 5:
                break

    exchange_quote.end()
