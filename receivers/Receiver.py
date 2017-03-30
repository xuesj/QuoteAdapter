# -*- coding: utf-8 -*-
"""A program to simulate quote receiver receiving message from Exchange Server"""

import calendar
import datetime
from multiprocessing import Process, Queue
from collections import defaultdict
import os.path
import time
from utils import Protocol, Exchange
from utils.observer import Event
import fcntl


class TransPeriod(object):
    """
    The period of exchange transaction time, e.g. start_time, end_time of a day.
    """
    def __init__(self, start_time, end_time):
        self._start_time = None
        self._end_time = None
        if end_time > start_time:
            self._start_time = start_time
            self._end_time = end_time
        else:
            raise ValueError('Time Error')

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    def time_delta(self):
        h = self._end_time.hour - self._start_time.hour
        m = self._end_time.minute - self._start_time.minute
        s = m * 60 + self._end_time.second - self._start_time.second
        return datetime.timedelta(hours=h, seconds=s)


class TransCalendar(calendar.Calendar):
    """
    The Exchange Transaction Calendar.
    Constructor parameters:
    day_periods: list of instance of Period,start_time, end_time
    first_week_day: the first day of a week, e.g. calendar.SUNDAY
    """
    SH_2017 = {2017: [(2017, 1, 1), (2017, 1, 2), (2017, 1, 27), (2017, 1, 28),
                      (2017, 1, 29), (2017, 1, 30), (2017, 1, 31), (2017, 2, 1),
                      (2017, 2, 2), (2017, 4, 2), (2017, 4, 3), (2017, 4, 4),
                      (2017, 5, 1), (2017, 5, 28), (2017, 5, 29), (2017, 5, 30),
                      (2017, 10, 1), (2017, 10, 2), (2017, 10, 3), (2017, 10, 4),
                      (2017, 10, 5), (2017, 10, 6), (2017, 10, 7), (2017, 10, 8)]}

    Holidays_2017 = {Exchange.SH: SH_2017, Exchange.SZ: SH_2017}

    def __init__(self, ex, day_periods, first_week_day=calendar.SUNDAY):
        super(TransCalendar, self).__init__(firstweekday=first_week_day)
        self._exchange = ex
        self._day_periods = day_periods
        self._holidays = defaultdict(list)
        self.set_holiday(TransCalendar.Holidays_2017[self._exchange])

    def set_holiday(self, holidays):
        for year, holiday_list in holidays.items():
            self._holidays[year] = [datetime.date(*holiday) for holiday in holiday_list]

    def is_trans_day(self, dt):
        if ((dt.date().weekday() == calendar.SATURDAY) or
                (dt.date().weekday() == calendar.SUNDAY) or
                (dt.date() in self._holidays[dt.year])):
            return False
        else:
            return True

    def is_trans_time(self, dt):
        dt_time = dt.time()
        for transPeriod in self._day_periods:
            if (dt_time >= transPeriod.start_time) and (dt_time <= transPeriod.end_time):
                return True
        return False

    @staticmethod
    def next_trans_day(dt):
        return dt


class ExchangeServer(object):
    def __init__(self,
                 exchange,
                 protocol,
                 pub_port,
                 ret_port,
                 timeout,
                 trans_cal):
        self._exchange = exchange
        self._protocol = protocol
        self._pub_port = pub_port
        self._last_msg_time = None
        self._ret_port = ret_port
        self._timeout = timeout
        self._trans_cal = trans_cal

    @property
    def exchange(self):
        return self._exchange

    @property
    def pub_port(self):
        return self._pub_port

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, val):
        self._timeout = val

    @property
    def last_msg_time(self):
        return self._last_msg_time

    @last_msg_time.setter
    def last_msg_time(self, val):
        self._last_msg_time = val

    def is_open(self, dt=None):
        if dt is None:
            dt = datetime.datetime.now()
        if self._trans_cal.is_trans_day(dt) and self._trans_cal.is_trans_time(dt):
            return True
        else:
            return False

    @staticmethod
    def is_close(dt=None):
        pass

    def has_msg(self):
        if self._protocol == Protocol.FILE:
            msg_time = os.path.getmtime(self._pub_port)
            if msg_time > self._last_msg_time:
                return True
            else:
                return False
        else:
            return True


class QuoteReceiver(Process):
    """Exchange quote service to provide real time quote of all its market"""

    def __init__(self, exchange_server):
        super(QuoteReceiver, self).__init__()
        self._exchange_server = exchange_server
        self._port = self._exchange_server.pub_port
        # self._quote = None
        self._queue = Queue(100)
        self._msg_event = Event()
        self._msg_event.subscribe(self.on_msg)

    @property
    def queue(self):
        return self._queue

    def get_msg(self):
        with open(self._port, 'r') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            msg = f.read()
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        return msg

    def login(self):
        pass

    def logout(self):
        pass

    def dispatch(self):
        waiting_time = 0
        start_time = time.time()
        while waiting_time < self._exchange_server.timeout:
            if self._exchange_server.has_msg():
                self._exchange_server.last_msg_time = os.path.getmtime(self._port)
                msg = self.get_msg()
                self._msg_event.emit(msg)
                waiting_time = 0
                start_time = time.time()
            else:
                waiting_time += time.time() - start_time

    def run(self):
        while self._exchange_server.is_open():
            self.login()
            self.dispatch()
            self.logout()

    def on_msg(self, msg):
        self._queue.put(msg)
