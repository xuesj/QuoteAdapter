# -*- coding: UTF-8 -*-
import datetime
from receivers.Calender import TransPeriod, TransCalendar
from utils import Exchange


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


def test_trans_calendar():
    t1 = datetime.time(hour=9, minute=30)
    t2 = datetime.time(hour=11, minute=30)
    t3 = datetime.time(hour=13, minute=30)
    t4 = datetime.time(hour=15, minute=30)

    periods = [TransPeriod(t1, t2), TransPeriod(t3, t4)]
    ex = Exchange.SH
    trans_calendar = TransCalendar(ex, periods)
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
