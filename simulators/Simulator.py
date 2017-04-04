# -*- coding: UTF-8 -*-
"""Simulator publish quote at some interval through ports by protocol.
exchange_server: protocol, pub_port, ret_port, trans_calendar."""

from multiprocessing import Process
import os
import time
import datetime
import fcntl
from apscheduler.schedulers.blocking import BlockingScheduler
from utils import Protocol, Exchange
from receivers.Receiver import ExchangeServer
from receivers.Calender import TransPeriod, TransCalendar


PUB_FILE = '../datas/mktdt00.txt'
HEAD_FILE = '../datas/head_data.txt'
INDEX_FILE = '../datas/index_data.txt'
STOCK_FILE = '../datas/stock_data.txt'
BOND_FILE = '../datas/bond_data.txt'
FUND_FILE = '../datas/fund_data.txt'
TAIL_FILE = '../datas/tail_data.txt'


class Simulator(object):
    def __init__(self, exchange_server):
        super(Simulator, self).__init__()
        self._exchange_server = exchange_server

    def pub_quotes(self):
        pass

    @staticmethod
    def get_data(source_file):
        if not os.path.exists(source_file):
            print('Data File is not exist!')
            return None

        with open(source_file, 'r') as f:
            msg = f.read()

        return msg

    @staticmethod
    def set_seq(seq, line, part):
        items = line.split('|')
        if part == 'Head':
            items[4] = ' ' * (8 - len(str(seq))) + str(seq)
        elif part == 'Equity':
            items[1] = '0' * (6 - len(str(seq))) + str(seq)
        msg = '|'.join(items)

        return msg

    @staticmethod
    def quote_seq(seq, head, index, stock, bond, fund, tail, m=1000, k=5):
        msg = Simulator.set_seq(seq, head, 'Head')
        msg += index
        for j in range(k, m + k):
            msg += Simulator.set_seq(j, stock, 'Equity')
        for j in range(m + k, 2 * m + k):
            msg += Simulator.set_seq(j, bond, 'Equity')
        for j in range(2 * m + k, 3 * m + k):
            msg += Simulator.set_seq(j, fund, 'Equity')
        msg += tail
        return msg

    def quotes(self):
        equity_num = 2
        seq = 0
        head = Simulator.get_data(HEAD_FILE)
        index = Simulator.get_data(INDEX_FILE)
        stock = Simulator.get_data(STOCK_FILE)
        bond = Simulator.get_data(BOND_FILE)
        fund = Simulator.get_data(FUND_FILE)
        tail = Simulator.get_data(TAIL_FILE)

        while self._exchange_server.is_open():
            seq += 1
            yield Simulator.quote_seq(seq,
                                      head,
                                      index,
                                      stock,
                                      bond,
                                      fund,
                                      tail,
                                      equity_num)


class TextSimulator(Simulator):
    def __init__(self, exchange_server):
        super(TextSimulator, self).__init__(exchange_server)

    def pub_quotes(self):
        pub_file = self._exchange_server.pub_port
        i = 0
        for data in self.quotes():
            i += 1
            print('Publish Msg: ' + str(i))
            with open(pub_file, 'w+') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                f.write(data)
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            time.sleep(1)


def text_simulator():
    protocol = Protocol.FILE
    pub_port = '../datas/mktdt00.txt'
    ret_port = None
    timeout = 6

    t1 = datetime.time(hour=9, minute=00)
    t2 = datetime.time(hour=11, minute=30)
    t3 = datetime.time(hour=13, minute=00)
    t4 = datetime.time(hour=23, minute=30)
    periods = [TransPeriod(t1, t2), TransPeriod(t3, t4)]

    ex = Exchange.SH
    trans_cal = TransCalendar(ex, periods)
    exchange_server = ExchangeServer(ex, protocol, pub_port, ret_port, timeout, trans_cal)
    ts = TextSimulator(exchange_server)
    ts.pub_quotes()

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    start = reduce(lambda x, y: str(x) + ',' + str(y), range(0, 59, 10))
    scheduler.add_job(text_simulator, 'cron', second=start)
    scheduler.start()
