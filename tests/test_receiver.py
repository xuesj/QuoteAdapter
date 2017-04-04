# -*- coding: UTF-8 -*-

from receivers.Receiver import QuoteReceiver, ExchangeServer
from receivers.Calender import TransCalendar, TransPeriod
from utils import Protocol, Port, EquityCategory, Exchange
import datetime
import time
from multiprocessing import Queue
from test_parsers import get_snapshot_parser


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


def test_exchange_server():
    protocol = Protocol.TCP
    pub_port = 9129
    ret_port = 9130
    timeout = 10

    t1 = datetime.time(hour=9, minute=00)
    t2 = datetime.time(hour=11, minute=30)
    t3 = datetime.time(hour=13, minute=00)
    t4 = datetime.time(hour=23, minute=30)

    periods = [TransPeriod(t1, t2), TransPeriod(t3, t4)]
    ex = Exchange.SH
    trans_cal = TransCalendar(ex, periods)

    exchange_server = ExchangeServer(ex, protocol, pub_port, ret_port, timeout, trans_cal)
    assert exchange_server

    dt = datetime.datetime.today()
    # assert exchange_server.is_open(dt)


def test_text_receiver():
    protocol = Protocol.FILE
    pub_port = '../datas/mktdt00.txt'
    ret_port = None
    timeout = 6

    t1 = datetime.time(hour=9, minute=30)
    t2 = datetime.time(hour=11, minute=30)
    t3 = datetime.time(hour=13, minute=00)
    t4 = datetime.time(hour=23, minute=30)
    periods = [TransPeriod(t1, t2), TransPeriod(t3, t4)]

    ex = Exchange.SH
    trans_cal = TransCalendar(ex, periods)
    exchange_server = ExchangeServer(ex, protocol, pub_port, ret_port, timeout, trans_cal)
    queue = Queue(100)
    quote_receiver = QuoteReceiver(exchange_server, queue)
    assert quote_receiver

    quote_receiver.start()

    i = 0
    j = 0
    snapshot_parser = get_snapshot_parser()
    while True:
        if not quote_receiver.queue.empty():
            msg = quote_receiver.queue.get(timeout=0.5)
            if msg is not None and msg != '':
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

        else:
            i += 1
        if i >= 500000 or j >= 30:
            break

    quote_receiver.terminate()
