# -*- coding: utf-8 -*-
"""A program to simulate quote receiver receiving message from Exchange Server"""

import calendar
from datetime import timedelta, datetime, date
from multiprocessing import Process
from collections import defaultdict
import os.path
import time


class ExchangeProtocol(object):
    __slots__ = ['value']
    TCP = 0
    FILE = 1
    SQLSERVER = 2


class ExchangePort(object):
    __slots__ = ['value']


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
        return timedelta(hours=h, seconds=s)


class TransCalendar(calendar.Calendar):
    """
    The Exchange Transaction Calendar.
    Constructor parameters:
    day_periods: list of instance of Period,start_time, end_time
    first_week_day: the first day of a week, e.g. calendar.SUNDAY
    """
    Holidays_2017 = {2017: [(2017, 1, 1), (2017, 1, 2), (2017, 1, 27), (2017, 1, 28),
                            (2017, 1, 29), (2017, 1, 30), (2017, 1, 31), (2017, 2, 1),
                            (2017, 2, 2), (2017, 4, 2), (2017, 4, 3), (2017, 4, 4),
                            (2017, 5, 1), (2017, 5, 28), (2017, 5, 29), (2017, 5, 30),
                            (2017, 10, 1), (2017, 10, 2), (2017, 10, 3), (2017, 10, 4),
                            (2017, 10, 5), (2017, 10, 6), (2017, 10, 7), (2017, 10, 8)]}

    def __init__(self, day_periods, first_week_day=calendar.SUNDAY):
        super(TransCalendar, self).__init__(firstweekday=first_week_day)
        self._day_periods = day_periods
        self._holidays = defaultdict(list)
        self.set_holiday(TransCalendar.Holidays_2017)

    def set_holiday(self, holidays):
        for year, holiday_list in holidays.items():
            self._holidays[year] = [date(*holiday) for holiday in holiday_list]

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


class ExchangeQuote(object):
    """Exchange quote service to provide real time quote of all its market"""

    def __init__(self, protocol, port, timeout, interval, trans_calendar, queue):
        self._protocol = protocol
        self._port = port
        self._last_msg_time = None
        self._timeout = timeout
        self._interval = interval
        self._state = None
        self._calendar = trans_calendar
        self._quote = None
        self._queue = queue
        self._write_process = Process(target=self._write_quote, args=(self._queue,))

    def _write_quote(self, q):
        i = 0
        while self.is_open():
            if self.has_msg():
                self._last_msg_time = os.path.getmtime(self._port)
                q.put('Hello: ' + str(i))
                i += 1
            time.sleep(0.1)

    def run(self):
        self._write_process.start()

    def end(self):
        self._write_process.terminate()

    def is_open(self, dt=None):
        if dt is None:
            dt = datetime.now()
        if self._calendar.is_trans_day(dt) and self._calendar.is_trans_time(dt):
            return True
        else:
            return False

    @staticmethod
    def is_close(dt=None):
        if dt is None:
            dt = datetime.now()
        return dt is None

    def has_msg(self):
        if self._protocol == ExchangeProtocol.FILE:
            msg_time = os.path.getmtime(self._port)
            if msg_time > self._last_msg_time:
                # self._last_msg_time = msg_time
                return True
            else:
                return False
        else:
            return True

    def read_quote(self):
        if not self._queue.empty():
            self._quote = self._queue.get()
            return self._quote
        else:
            return None