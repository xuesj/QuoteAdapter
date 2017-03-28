# -*- coding: UTF-8 -*-

from receivers.Receiver import QuoteReceiver, TransCalendar, TransPeriod
from utils import Protocol, Port, EquityCategory
import datetime
import time
from multiprocessing import Queue
from test_parsers import get_snapshot_parser


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
    protocol = Protocol()
    protocol.value = Protocol.FILE
    assert protocol.value == 1
    protocol.value = Protocol.TCP
    assert protocol.value == 0
    try:
        protocol.name = 'james'
    except AttributeError as e:
        assert e


def test_exchange_port():
    exchange_port = Port()
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
    # assert trans_calendar.is_trans_day(now)
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

    assert not trans_calendar.is_trans_day(datetime.datetime(2017, 1, 1))
    assert not trans_calendar.is_trans_day(datetime.datetime(2017, 10, 1))
    assert not trans_calendar.is_trans_day(datetime.datetime(2017, 10, 8))
    assert not trans_calendar.is_trans_day(datetime.datetime(2017, 4, 4))
    assert not trans_calendar.is_trans_day(datetime.datetime(2017, 1, 27))


def test_receiver():
    protocol = Protocol.FILE
    port = '../datas/mktdt00.txt'
    timeout = 3
    interval = 6

    t1 = datetime.time(hour=8, minute=00)
    t2 = datetime.time(hour=11, minute=30)
    t3 = datetime.time(hour=13, minute=00)
    t4 = datetime.time(hour=23, minute=59)

    periods = [TransPeriod(t1, t2), TransPeriod(t3, t4)]
    trans_calendar = TransCalendar(periods)
    queue = Queue(30)

    quote_receiver = QuoteReceiver(protocol=protocol, port=port, timeout=timeout,
                                   interval=interval, trans_calendar=trans_calendar,
                                   queue=queue)
    assert quote_receiver
    assert quote_receiver.is_open()
    assert not quote_receiver.is_close()
    assert quote_receiver.has_msg()

    quote_receiver.run()

    i = 0
    j = 0
    snapshot_parser = get_snapshot_parser()
    while True:
        msg = quote_receiver.get_msg()
        # assert quote_receiver.has_msg()
        if msg is not None:
            t1 = time.time()
            snapshot = snapshot_parser.parse(msg)
            t2 = time.time()
            # print('Message line: ' + str(len(msg.split('\n'))))
            print('Parse time: ' + str(t2 - t1))
            assert snapshot.quotes['000001'].equity == '000001'
            assert snapshot.quotes['000001'].category == EquityCategory.INDEX
            assert snapshot.quotes['000002'].equity == '000002'
            assert snapshot.quotes['000002'].category == EquityCategory.STOCK
            assert snapshot.quotes['000003'].equity == '000003'
            assert snapshot.quotes['000003'].category == EquityCategory.BOND
            assert snapshot.quotes['000004'].equity == '000004'
            assert snapshot.quotes['000004'].category == EquityCategory.FUND
            j = snapshot.seq
            print('receive message: ' + str(snapshot.seq))
        i += 1
        if i >= 5000000 or j >= 30:
            break

    quote_receiver.end()
